import React, { useRef, useCallback, useState, useEffect } from 'react';
import type { MoleculeState, PlacedBlock, PortDir } from '../types/molecule';
import type { Rotation } from '../utils/rotation';
import { oppositeDir, rotateDir } from '../utils/rotation';
import { getTemplate } from '../data/blockTemplates';
import { BlockSVG } from './BlockSVG';
import './Canvas.css';

const BLOCK_PX = 80;
const CELL_GAP = 40;
const GRID_STEP = BLOCK_PX + CELL_GAP;

// ── Bond endpoint helper ───────────────────────────────────────────────────
// Returns the pixel coordinate of the square-edge midpoint facing dir
function squareEdgePoint(gridX: number, gridY: number, dir: PortDir): [number, number] {
  const cx = gridX * GRID_STEP + CELL_GAP + BLOCK_PX / 2;
  const cy = gridY * GRID_STEP + CELL_GAP + BLOCK_PX / 2;
  const half = BLOCK_PX / 2;
  switch (dir) {
    case 'left':  return [cx - half, cy];
    case 'right': return [cx + half, cy];
    case 'up':    return [cx, cy - half];
    case 'down':  return [cx, cy + half];
    default:      return [cx, cy];
  }
}

interface CanvasProps {
  state: MoleculeState;
  onDrop:         (templateId: string, gridX: number, gridY: number, itemType: 'block' | 'group') => void;
  onMove:         (instanceId: string, gridX: number, gridY: number) => void;
  onMoveMany:     (ids: string[], dx: number, dy: number) => void;
  onRotate:       (instanceId: string, rotation: Rotation) => void;
  onConnect:      (fromId: string, fromPort: string, toId: string, toPort: string) => void;
  onDisconnect:   (instanceId: string) => void;
  onRemove:       (instanceId: string) => void;
  onRemoveMany:   (ids: string[]) => void;
  onUpgradeBond:  (fromId: string, toId: string) => void;
  onUncollapse:   (instanceId: string) => void;
  onClearAll:     () => void;
}

// ── Selection Box Helpers ──────────────────────────────────────────────────
interface SelectionBox {
  startX: number;
  startY: number;
  endX:   number;
  endY:   number;
}

function boxIntersectsBlock(box: SelectionBox, block: PlacedBlock): boolean {
  const minX = Math.min(box.startX, box.endX);
  const maxX = Math.max(box.startX, box.endX);
  const minY = Math.min(box.startY, box.endY);
  const maxY = Math.max(box.startY, box.endY);
  const bx = block.gridX * BLOCK_PX;
  const by = block.gridY * BLOCK_PX;
  return bx < maxX && bx + BLOCK_PX > minX && by < maxY && by + BLOCK_PX > minY;
}

// ── Public component ───────────────────────────────────────────────────────
export function Canvas({
  state,
  onDrop,
  onMove,
  onRotate,
  onConnect,
  onDisconnect,
  onRemove,
  onRemoveMany,
  onUpgradeBond,
  onUncollapse,
  onClearAll,
}: CanvasProps) {
  const paletteDropRef = useRef<HTMLDivElement | null>(null);
  const canvasRef = useRef<HTMLDivElement>(null);

  // ── Interaction states ──
  const [draggingId, setDraggingId] = useState<string | null>(null);
  const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 }); // offset in pixels
  const [dragCurrentGrid, setDragCurrentGrid] = useState<{ x: number, y: number } | null>(null);
  const [dragClientPos, setDragClientPos] = useState<{ x: number, y: number } | null>(null);
  const [hoveredId, setHoveredId] = useState<string | null>(null);

  const [groupDragActive, setGroupDragActive] = useState(false);

  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());
  const [selBox, setSelBox] = useState<SelectionBox | null>(null);
  const isDrawingSelBox = useRef(false);

  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [zoom, setZoom] = useState(1);
  const [tool, setTool] = useState<'select' | 'pan'>('select');
  const [isPanning, setIsPanning] = useState(false);
  const [lastPanPos, setLastPanPos] = useState({ x: 0, y: 0 });

  const panRef = useRef(pan);
  const zoomRef = useRef(zoom);
  panRef.current = pan;
  zoomRef.current = zoom;

  // Track palette element for drag-to-delete detection
  useEffect(() => {
    paletteDropRef.current = document.querySelector('.palette') as HTMLDivElement;
  }, []);

  // ── Helper: coords ───────────────────────────────────────────────────────
  const getCanvasCoords = useCallback((clientX: number, clientY: number) => {
    if (!canvasRef.current) return { x: 0, y: 0 };
    const rect = canvasRef.current.getBoundingClientRect();
    return {
      x: (clientX - rect.left - panRef.current.x) / zoomRef.current,
      y: (clientY - rect.top - panRef.current.y) / zoomRef.current,
    };
  }, [pan, zoom]);

  const getGridCoords = useCallback((px: number, py: number) => {
    return {
      gridX: Math.floor(px / GRID_STEP),
      gridY: Math.floor(py / GRID_STEP),
    };
  }, []);

  // ── Keyboard ─────────────────────────────────────────────────────────────
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if ((e.key === 'Delete' || e.key === 'Backspace') && selectedIds.size > 0) {
        if ((e.target as HTMLElement).tagName === 'INPUT') return;
        onRemoveMany([...selectedIds]);
        setSelectedIds(new Set());
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [selectedIds, onRemoveMany]);

  // ── Drag & Drop from Palette ──────────────────────────────────────────────
  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'copy';
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    const data = e.dataTransfer.getData('application/omolecule');
    if (!data) return;
    try {
      const parsed = JSON.parse(data);
      const { x, y } = getCanvasCoords(e.clientX, e.clientY);
      // Offset by half block so it centers on mouse
      const { gridX, gridY } = getGridCoords(x - BLOCK_PX / 2, y - BLOCK_PX / 2);
      
      // Check if grid is occupied
      if (state.blocks.some(b => !b.isHidden && b.gridX === gridX && b.gridY === gridY)) {
        return; // Cell occupied
      }
      
      onDrop(parsed.id, gridX, gridY, parsed.type);
    } catch (err) {
      console.error(err);
    }
  }, [getCanvasCoords, getGridCoords, state.blocks, onDrop]);

  // ── Adjacency Bonding Logic ──────────────────────────────────────────────
  const tryAutoBond = useCallback((instanceId: string, overridePos?: {x: number, y: number}) => {
    const block = state.blocks.find(b => b.instanceId === instanceId);
    if (!block || block.isHidden) return;

    const tpl = getTemplate(block.templateId);
    if (!tpl) return;

    const neighbors = [
      { dir: 'up' as PortDir,    dx: 0,  dy: -1 },
      { dir: 'down' as PortDir,  dx: 0,  dy: 1 },
      { dir: 'left' as PortDir,  dx: -1, dy: 0 },
      { dir: 'right' as PortDir, dx: 1,  dy: 0 },
    ];

    const currentGridX = overridePos ? overridePos.x : block.gridX;
    const currentGridY = overridePos ? overridePos.y : block.gridY;

    for (const n of neighbors) {
      const nx = currentGridX + n.dx;
      const ny = currentGridY + n.dy;
      const neighborBlock = state.blocks.find(b => !b.isHidden && b.gridX === nx && b.gridY === ny && b.instanceId !== instanceId);
      if (!neighborBlock) continue;

      // Ensure block has an unconnected port in the direction of the neighbor
      let blockPort = block.ports.find(p => !p.connectedTo && rotateDir(p.dir as PortDir, block.rotation) === n.dir);
      
      // Auto-rotate block if needed
      if (!blockPort) {
        const rotations: Rotation[] = [0, 90, 180, 270];
        for (const r of rotations) {
          const p = block.ports.find(p => !p.connectedTo && rotateDir(p.dir as PortDir, r) === n.dir);
          if (p) {
            blockPort = p;
            onRotate(instanceId, r);
            break;
          }
        }
      }

      if (!blockPort) continue;

      // Check neighbor's port facing us
      const opposingDir = oppositeDir(n.dir);
      let neighborPort = neighborBlock.ports.find(p => !p.connectedTo && rotateDir(p.dir as PortDir, neighborBlock.rotation) === opposingDir);

      // Auto-rotate neighbor if needed
      if (!neighborPort) {
        const rotations: Rotation[] = [0, 90, 180, 270];
        for (const r of rotations) {
          const p = neighborBlock.ports.find(p => !p.connectedTo && rotateDir(p.dir as PortDir, r) === opposingDir);
          if (p) {
            neighborPort = p;
            onRotate(neighborBlock.instanceId, r);
            break;
          }
        }
      }

      if (neighborPort) {
        onConnect(instanceId, blockPort.id, neighborBlock.instanceId, neighborPort.id);
        break; // Only bond one per drop to prevent cascaded unexpected states
      }
    }
  }, [state.blocks, onConnect, onRotate]);

  // ── Canvas background ───────────────────────────────────────────────────
  const handleCanvasMouseDown = useCallback((e: React.MouseEvent) => {
    if (e.button === 1 || tool === 'pan') {
      setIsPanning(true);
      setLastPanPos({ x: e.clientX, y: e.clientY });
      e.preventDefault();
      return;
    }
    if (e.button === 0 && tool === 'select') {
      const { x, y } = getCanvasCoords(e.clientX, e.clientY);
      isDrawingSelBox.current = true;
      setSelBox({ startX: x, startY: y, endX: x, endY: y });
      if (!e.shiftKey) setSelectedIds(new Set());
    }
  }, [tool, getCanvasCoords]);

  const handleWheel = useCallback((e: React.WheelEvent) => {
    const zoomDelta = Math.exp(-e.deltaY * 0.005);
    let newZoom = zoom * zoomDelta;
    newZoom = Math.max(0.2, Math.min(newZoom, 5));
    const scaleChange = newZoom - zoom;
    const rect = canvasRef.current!.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;
    const newPanX = pan.x - ((mouseX - pan.x) * scaleChange) / zoom;
    const newPanY = pan.y - ((mouseY - pan.y) * scaleChange) / zoom;
    setZoom(newZoom);
    setPan({ x: newPanX, y: newPanY });
  }, [zoom, pan]);

  // ── Block Interactions ──────────────────────────────────────────────────
  const handleBlockMouseDown = useCallback((e: React.MouseEvent, instanceId: string) => {
    if (tool === 'pan' || e.button !== 0) return;
    e.stopPropagation();
    const block = state.blocks.find(b => b.instanceId === instanceId);
    if (!block) return;

    if (selectedIds.has(instanceId)) {
      setGroupDragActive(true);
      return;
    }

    if (e.shiftKey) {
      setSelectedIds(prev => {
        const next = new Set(prev);
        if (next.has(instanceId)) next.delete(instanceId);
        else next.add(instanceId);
        return next;
      });
      return;
    }

    setSelectedIds(new Set([instanceId]));
    setDraggingId(instanceId);
    setDragClientPos({ x: e.clientX, y: e.clientY });

    const { x, y } = getCanvasCoords(e.clientX, e.clientY);
    const blockX = block.gridX * GRID_STEP;
    const blockY = block.gridY * GRID_STEP;
    setDragOffset({ x: x - blockX, y: y - blockY });
    setDragCurrentGrid({ x: block.gridX, y: block.gridY });
  }, [tool, state.blocks, selectedIds, getCanvasCoords]);

  const handleMouseMove = useCallback((e: React.MouseEvent) => {
    if (isPanning) {
      setPan(prev => ({ x: prev.x + (e.clientX - lastPanPos.x), y: prev.y + (e.clientY - lastPanPos.y) }));
      setLastPanPos({ x: e.clientX, y: e.clientY });
      return;
    }

    if (groupDragActive) {
      return;
    }

    if (isDrawingSelBox.current && selBox) {
      const { x, y } = getCanvasCoords(e.clientX, e.clientY);
      const newBox = { ...selBox, endX: x, endY: y };
      setSelBox(newBox);
      const newSel = new Set<string>();
      for (const block of state.blocks) {
        if (!block.isHidden && boxIntersectsBlock(newBox, block)) newSel.add(block.instanceId);
      }
      setSelectedIds(newSel);
      return;
    }

    if (draggingId) {
      setDragClientPos({ x: e.clientX, y: e.clientY });
      const { x, y } = getCanvasCoords(e.clientX, e.clientY);
      const { gridX, gridY } = getGridCoords(x - dragOffset.x, y - dragOffset.y);
      if (!dragCurrentGrid || dragCurrentGrid.x !== gridX || dragCurrentGrid.y !== gridY) {
        setDragCurrentGrid({ x: gridX, y: gridY });
        tryAutoBond(draggingId, { x: gridX, y: gridY });
      }
    }
  }, [isPanning, lastPanPos, groupDragActive, isDrawingSelBox, selBox, draggingId, getCanvasCoords, getGridCoords, dragOffset, state.blocks, tryAutoBond, dragCurrentGrid]);

  const handleMouseUp = useCallback(() => {
    if (isPanning) setIsPanning(false);
    if (groupDragActive) {
      setGroupDragActive(false);
    }
    if (isDrawingSelBox.current) {
      isDrawingSelBox.current = false;
      setSelBox(null);
    }
    if (draggingId) {
      // ── Drag to palette to delete ──────────────────────────
      const paletteEl = paletteDropRef.current;
      if (paletteEl && dragClientPos) {
        const paletteRect = paletteEl.getBoundingClientRect();
        const inPalette =
          dragClientPos.x >= paletteRect.left &&
          dragClientPos.x <= paletteRect.right &&
          dragClientPos.y >= paletteRect.top &&
          dragClientPos.y <= paletteRect.bottom;
        if (inPalette) {
          onDisconnect(draggingId);
          onRemove(draggingId);
          setSelectedIds(prev => { const n = new Set(prev); n.delete(draggingId); return n; });
          setDraggingId(null);
          setDragCurrentGrid(null);
          setDragClientPos(null);
          return;
        }
      }

      if (dragCurrentGrid) {
        // Verify cell is empty (ignoring self)
        const occupied = state.blocks.some(b =>
          !b.isHidden &&
          b.instanceId !== draggingId &&
          b.gridX === dragCurrentGrid.x &&
          b.gridY === dragCurrentGrid.y
        );
        if (!occupied) {
          onMove(draggingId, dragCurrentGrid.x, dragCurrentGrid.y);
        }
      }
    }
    setDraggingId(null);
    setDragCurrentGrid(null);
    setDragClientPos(null);
  }, [isPanning, groupDragActive, draggingId, dragCurrentGrid, dragClientPos, state.blocks, onMove, onDisconnect, onRemove]);

  // ── Rendering ────────────────────────────────────────────────────────────
  // Visible blocks
  const visibleBlocks = state.blocks.filter(b => !b.isHidden);

  // Grid background pattern
  const gridPatternSize = GRID_STEP * zoom;

  return (
    <div
      ref={canvasRef}
      className={`canvas tool-${tool}`}
      onMouseDown={handleCanvasMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
      onMouseLeave={handleMouseUp}
      onWheel={handleWheel}
      onDragOver={handleDragOver}
      onDrop={handleDrop}
      style={{
        backgroundSize: `${gridPatternSize}px ${gridPatternSize}px`,
        backgroundPosition: `${pan.x % gridPatternSize}px ${pan.y % gridPatternSize}px`,
        backgroundImage: `
          radial-gradient(circle, rgba(255,255,255,0.1) ${2 * zoom}px, transparent ${2 * zoom}px)
        `
      }}
    >
      <div className="canvas-toolbar" onMouseDown={e => e.stopPropagation()}>
        <button className={tool === 'select' ? 'active' : ''} onClick={() => setTool('select')} title="選取 (S)">👆</button>
        <button className={tool === 'pan' ? 'active' : ''} onClick={() => setTool('pan')} title="移動畫布 (P)">✋</button>
        <div className="toolbar-divider" />
        <button onClick={() => { setPan({ x: 0, y: 0 }); setZoom(1); }} className="toolbar-btn-text" title="重置視角">⊙</button>
        <div className="toolbar-divider" />
        <button onClick={() => setSelectedIds(new Set(visibleBlocks.map(b => b.instanceId)))} className="toolbar-btn-text">全選</button>
        <button
          onClick={() => { onRemoveMany([...selectedIds]); setSelectedIds(new Set()); }}
          className={`toolbar-btn-text toolbar-btn-danger ${selectedIds.size > 0 ? 'has-selection' : ''}`}
        >
          {selectedIds.size > 0 ? `刪除 (${selectedIds.size})` : '刪除'}
        </button>
        <div className="toolbar-divider" />
        <button onClick={onClearAll} className="toolbar-btn-text toolbar-btn-danger">清除全部</button>
      </div>

      <div className="canvas-transform-layer" style={{ transform: `translate(${pan.x}px, ${pan.y}px) scale(${zoom})` }}>
        {visibleBlocks.length === 0 && (
          <div className="canvas-empty">
            <div className="canvas-empty-icon">⚛</div>
            <div className="canvas-empty-text">從左側拖曳積木到此處</div>
            <div className="canvas-empty-sub">放置在相鄰的格子自動形成鍵結</div>
          </div>
        )}

        {/* Connections SVG Layer */}
        <svg className="canvas-svg">
          {state.connections.map((conn) => {
            const b1 = state.blocks.find(b => b.instanceId === conn.fromInstance);
            const b2 = state.blocks.find(b => b.instanceId === conn.toInstance);
            if (!b1 || !b2 || b1.isHidden || b2.isHidden) return null;

            const b1Dragging = b1.instanceId === draggingId && dragCurrentGrid;
            const b2Dragging = b2.instanceId === draggingId && dragCurrentGrid;

            const g1x = b1Dragging ? dragCurrentGrid.x : b1.gridX;
            const g1y = b1Dragging ? dragCurrentGrid.y : b1.gridY;
            const g2x = b2Dragging ? dragCurrentGrid.x : b2.gridX;
            const g2y = b2Dragging ? dragCurrentGrid.y : b2.gridY;

            // Determine bond direction (which edge the line exits from)
            const dx = g2x - g1x;
            const dy = g2y - g1y;
            let b1ExitDir: PortDir;
            let b2ExitDir: PortDir;
            if (Math.abs(dx) >= Math.abs(dy)) {
              b1ExitDir = dx >= 0 ? 'right' : 'left';
              b2ExitDir = dx >= 0 ? 'left'  : 'right';
            } else {
              b1ExitDir = dy >= 0 ? 'down' : 'up';
              b2ExitDir = dy >= 0 ? 'up'   : 'down';
            }

            // Always use the physical exit direction for drawing the bond, so bonds don't become diagonal
            const b1Dir: PortDir = b1ExitDir;
            const b2Dir: PortDir = b2ExitDir;

            const [x1, y1] = squareEdgePoint(g1x, g1y, b1Dir);
            const [x2, y2] = squareEdgePoint(g2x, g2y, b2Dir);

            // Perpendicular vector for double/triple bond offset
            const bdx = x2 - x1;
            const bdy = y2 - y1;
            const len = Math.sqrt(bdx * bdx + bdy * bdy) || 1;
            // slightly larger offset to prevent lines from visually merging
            const nx = (-bdy / len) * 7;
            const ny = (bdx / len) * 7;

            const color = conn.bondType === 'double' ? '#FFD700' : conn.bondType === 'triple' ? '#FF6B6B' : '#4DD0E1';

            return (
              <g
                key={`${conn.fromInstance}-${conn.toInstance}`}
                style={{ cursor: 'pointer', pointerEvents: 'stroke' }}
                onClick={(e) => { e.stopPropagation(); onUpgradeBond(conn.fromInstance, conn.toInstance); }}
              >
                {/* Invisible wide hit target */}
                <line x1={x1} y1={y1} x2={x2} y2={y2} stroke="transparent" strokeWidth="20" />
                {conn.bondType === 'single' && (
                  <line x1={x1} y1={y1} x2={x2} y2={y2} stroke={color} strokeWidth="3" strokeLinecap="round" />
                )}
                {conn.bondType === 'double' && (
                  <>
                    <line x1={x1 + nx} y1={y1 + ny} x2={x2 + nx} y2={y2 + ny} stroke={color} strokeWidth="3" strokeLinecap="round" />
                    <line x1={x1 - nx} y1={y1 - ny} x2={x2 - nx} y2={y2 - ny} stroke={color} strokeWidth="3" strokeLinecap="round" />
                  </>
                )}
                {conn.bondType === 'triple' && (
                  <>
                    <line x1={x1} y1={y1} x2={x2} y2={y2} stroke={color} strokeWidth="2.5" strokeLinecap="round" />
                    <line x1={x1 + nx * 1.5} y1={y1 + ny * 1.5} x2={x2 + nx * 1.5} y2={y2 + ny * 1.5} stroke={color} strokeWidth="2.5" strokeLinecap="round" />
                    <line x1={x1 - nx * 1.5} y1={y1 - ny * 1.5} x2={x2 - nx * 1.5} y2={y2 - ny * 1.5} stroke={color} strokeWidth="2.5" strokeLinecap="round" />
                  </>
                )}
              </g>
            );
          })}
          {selBox && (
            <rect
              x={Math.min(selBox.startX, selBox.endX)}
              y={Math.min(selBox.startY, selBox.endY)}
              width={Math.abs(selBox.endX - selBox.startX)}
              height={Math.abs(selBox.endY - selBox.startY)}
              fill="rgba(59,130,246,0.08)" stroke="#3b82f6" strokeWidth={1 / zoom} strokeDasharray="4,4"
            />
          )}
        </svg>

        {/* Blocks Layer */}
        {visibleBlocks.map((block) => {
          const tpl = getTemplate(block.templateId);
          if (!tpl) return null;
          const isDragging = draggingId === block.instanceId;
          const isHovered = hoveredId === block.instanceId;
          const isSelected = selectedIds.has(block.instanceId);

          const renderX = (isDragging && dragCurrentGrid ? dragCurrentGrid.x : block.gridX) * GRID_STEP + CELL_GAP;
          const renderY = (isDragging && dragCurrentGrid ? dragCurrentGrid.y : block.gridY) * GRID_STEP + CELL_GAP;

          // Compute physical bonded edges for dynamic lone pair/radical placement
          const getGridPos = (bId: string) => {
             const b = state.blocks.find(x => x.instanceId === bId);
             if (!b) return null;
             if (bId === draggingId && dragCurrentGrid) return dragCurrentGrid;
             return { x: b.gridX, y: b.gridY };
          };
          const bPos = getGridPos(block.instanceId);
          const bondedEdges: PortDir[] = [];
          if (bPos) {
             for (const conn of state.connections) {
               if (conn.fromInstance === block.instanceId) {
                  const tPos = getGridPos(conn.toInstance);
                  if (tPos) {
                     const dx = tPos.x - bPos.x;
                     const dy = tPos.y - bPos.y;
                     if (Math.abs(dx) >= Math.abs(dy)) bondedEdges.push(dx >= 0 ? 'right' : 'left');
                     else bondedEdges.push(dy >= 0 ? 'down' : 'up');
                  }
               } else if (conn.toInstance === block.instanceId) {
                  const fPos = getGridPos(conn.fromInstance);
                  if (fPos) {
                     const dx = fPos.x - bPos.x;
                     const dy = fPos.y - bPos.y;
                     if (Math.abs(dx) >= Math.abs(dy)) bondedEdges.push(dx >= 0 ? 'right' : 'left');
                     else bondedEdges.push(dy >= 0 ? 'down' : 'up');
                  }
               }
             }
          }

          // Include consumed ports so their dots are hidden too
          const connectedPortIds = block.ports
            .filter(p => !!p.connectedTo)
            .map(p => p.id);

          return (
            <div
              key={block.instanceId}
              className={`canvas-block ${isDragging ? 'is-dragging' : ''} ${isSelected ? 'is-selected' : ''}`}
              style={{ left: renderX, top: renderY, width: BLOCK_PX, height: BLOCK_PX }}
              onMouseDown={e => handleBlockMouseDown(e, block.instanceId)}
              onMouseEnter={() => setHoveredId(block.instanceId)}
              onMouseLeave={() => setHoveredId(null)}
              onDoubleClick={e => {
                e.stopPropagation();
                if (block.collapsedText) {
                  onUncollapse(block.instanceId);
                } else if (isSelected && selectedIds.size > 1) {
                  onRemoveMany([...selectedIds]);
                  setSelectedIds(new Set());
                } else {
                  onRemove(block.instanceId);
                  setSelectedIds(prev => { const n = new Set(prev); n.delete(block.instanceId); return n; });
                }
              }}
              title={block.collapsedText ? '雙擊展開氫原子' : '雙擊刪除'}
            >
              <BlockSVG
                template={tpl}
                size={BLOCK_PX}
                rotation={block.rotation as any}
                connectedPorts={connectedPortIds}
                bondedEdges={bondedEdges}
                glowPorts={[]}
                collapsedText={block.collapsedText}
              />
              {isHovered && !isDragging && tool === 'select' && !isSelected && !block.collapsedText && (
                <button className="block-delete-btn" onMouseDown={e => e.stopPropagation()} onClick={e => { e.stopPropagation(); onRemove(block.instanceId); }}>×</button>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
