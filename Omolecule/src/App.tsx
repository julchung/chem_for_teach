import React, { useCallback, useEffect, useRef, useState } from 'react';
import { Palette } from './components/Palette';
import { Canvas } from './components/Canvas';
import { MoleculeDisplay } from './components/MoleculeDisplay';
import { useMolecule } from './hooks/useMolecule';
import { generateSMILES, isMoleculeComplete } from './utils/smilesGenerator';
import { fetchMoleculeInfo } from './utils/pubchemApi';
import type { MoleculeInfo } from './utils/pubchemApi';
import './App.css';

const DEBOUNCE_MS = 1200;

export default function App() {
  const { state, addBlock, addGroup, moveBlock, moveBlocks, setBlockRotation, removeBlock, removeBlocks, disconnectBlock, connectPorts, upgradeBond, uncollapseHydrogens, clearAll } = useMolecule();
  const [moleculeInfo, setMoleculeInfo] = useState<MoleculeInfo | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const [leftWidth, setLeftWidth] = useState(260); // resizable splitter
  const resizing = useRef(false);

  const smiles = generateSMILES(state);
  const complete = isMoleculeComplete(state);


  // Fetch from PubChem when molecule changes
  useEffect(() => {
    if (debounceRef.current) clearTimeout(debounceRef.current);
    if (!smiles || state.blocks.length === 0) {
      setMoleculeInfo(null);
      setIsLoading(false);
      return;
    }
    if (complete) {
      setIsLoading(true);
      debounceRef.current = setTimeout(async () => {
        const info = await fetchMoleculeInfo(smiles);
        setMoleculeInfo(info);
        setIsLoading(false);
      }, DEBOUNCE_MS);
    } else {
      setMoleculeInfo(null);
      setIsLoading(false);
    }
    return () => { if (debounceRef.current) clearTimeout(debounceRef.current); };
  }, [smiles, complete, state.blocks.length]);



  const handleCanvasDrop = useCallback((
    templateId: string,
    x: number,
    y: number,
    itemType: 'block' | 'group',
  ) => {
    console.log('[App] handleCanvasDrop called:', templateId, x, y, itemType);
    if (itemType === 'group') {
      addGroup(templateId, x, y);
    } else {
      addBlock(templateId, x, y);
    }
  }, [addBlock, addGroup]);

  // Add item from palette to canvas
  const handleAdd = useCallback((templateId: string, isGroup: boolean) => {
    console.log('[App] handleAdd called:', templateId, isGroup);
    // Use grid coordinates for click-to-add
    const gridX = Math.floor(Math.random() * 5) + 3;
    const gridY = Math.floor(Math.random() * 5) + 2;
    if (isGroup) {
      addGroup(templateId, gridX, gridY);
    } else {
      addBlock(templateId, gridX, gridY);
    }
  }, [addBlock, addGroup]);

  // Resizable splitter
  const handleSplitterMouseDown = useCallback((e: React.MouseEvent) => {
    e.preventDefault();
    resizing.current = true;
    const startX = e.clientX;
    const startW = leftWidth;

    const onMove = (me: MouseEvent) => {
      if (!resizing.current) return;
      const delta = me.clientX - startX;
      setLeftWidth(Math.max(180, Math.min(420, startW + delta)));
    };
    const onUp = () => {
      resizing.current = false;
      window.removeEventListener('mousemove', onMove);
      window.removeEventListener('mouseup', onUp);
    };
    window.addEventListener('mousemove', onMove);
    window.addEventListener('mouseup', onUp);
  }, [leftWidth]);

  return (
    <div className="app">
      {/* Top bar */}
      <header className="topbar">
        <div className="topbar-left">
          <span className="logo">⚗ Omolecule</span>
          <span className="tagline">有機分子積木建構器</span>
        </div>
        <div className="topbar-right">
          <button className="btn-clear" onClick={clearAll} title="清除畫布">
            🗑 清除
          </button>
          <div className="status-indicator">
            {state.blocks.length === 0 && <span className="status-idle">等待積木</span>}
            {state.blocks.length > 0 && !complete && <span className="status-building">建構中…</span>}
            {complete && <span className="status-complete">✓ 分子完整</span>}
          </div>
        </div>
      </header>

      <div className="main-layout">
        {/* Left: Palette */}
        <div className="left-panel" style={{ width: leftWidth }}>
          <Palette onAdd={handleAdd} />
        </div>

        {/* Splitter */}
        <div className="splitter" onMouseDown={handleSplitterMouseDown} title="拖曳調整寬度" />

        {/* Center: Canvas */}
        <div className="center-panel">
          <div className="panel-title">
            <span>🎨 作圖區</span>
            <span className="panel-hint">雙擊積木可刪除</span>
          </div>
          <div className="panel-body">
            <Canvas
              state={state}
              onDrop={handleCanvasDrop}
              onMove={moveBlock}
              onMoveMany={moveBlocks}
              onRotate={setBlockRotation}
              onConnect={connectPorts}
              onDisconnect={disconnectBlock}
              onRemove={removeBlock}
              onRemoveMany={removeBlocks}
              onUpgradeBond={upgradeBond}
              onUncollapse={uncollapseHydrogens}
              onClearAll={clearAll}
            />
          </div>
        </div>

        {/* Right: Display */}
        <div className="right-panel">
          <div className="panel-title">
            <span>🔬 展示區</span>
            <span className="panel-hint">即時 3D 預覽</span>
          </div>
          <div className="panel-body">
            <MoleculeDisplay
              smiles={smiles}
              isComplete={complete}
              moleculeInfo={moleculeInfo}
              isLoading={isLoading}
              blockCount={state.blocks.length}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
