import type { BlockTemplate, PortDir } from '../types/molecule';
import type { Rotation } from '../utils/rotation';
import { rotateDir } from '../utils/rotation';

const BLOCK_SIZE = 80;

export interface BlockSVGProps {
  template: BlockTemplate;
  size?: number;
  rotation: Rotation;
  connectedPorts: string[];
  bondedEdges?: PortDir[];
  glowPorts?: string[];
  collapsedText?: string;
}

// ── geometry helpers ───────────────────────────────────────────────────────
// Returns midpoint of the square block edge for a given direction
function edgeMidpoint(dir: PortDir, size: number): [number, number] {
  const half = size / 2;
  switch (dir) {
    case 'left':  return [0,    half];
    case 'right': return [size, half];
    case 'up':    return [half, 0   ];
    case 'down':  return [half, size];
  }
}

// ── Public component ───────────────────────────────────────────────────────
export function BlockSVG({
  template,
  size = BLOCK_SIZE,
  rotation = 0,
  glowPorts = [],
  connectedPorts = [],
  bondedEdges,
  collapsedText,
}: BlockSVGProps) {
  const cx = size / 2;
  const cy = size / 2;

  // Square frame inset
  const frameInset = size * 0.04;
  const frameSize = size - frameInset * 2;
  const frameRadius = Math.max(5, size * 0.1);

  // Inscribed atom circle
  const circleR = (frameSize / 2) * 0.84;

  // Dot sizes
  const dotR   = Math.max(3.5, size * 0.058); // radical
  const lpDotR = Math.max(2.5, size * 0.042); // lone pair

  // Text
  const displayText = collapsedText || template.label || template.element;
  const fontSize = displayText.length > 3
    ? size * 0.20
    : displayText.length > 2
    ? size * 0.24
    : displayText.length > 1
    ? size * 0.28
    : size * 0.34;

  return (
    <svg
      width={size}
      height={size}
      viewBox={`0 0 ${size} ${size}`}
      style={{ overflow: 'visible' }}
    >
      {/* ── Square frame ── */}
      <rect
        x={frameInset}
        y={frameInset}
        width={frameSize}
        height={frameSize}
        rx={frameRadius}
        ry={frameRadius}
        fill="transparent"
        stroke={`${template.color}66`}
        strokeWidth="1.5"
      />

      {/* ── Atom circle body ── */}
      <circle
        cx={cx}
        cy={cy}
        r={circleR}
        fill={template.color}
        stroke="#ffffff22"
        strokeWidth="1.5"
      />

      {/* ── Element label ── */}
      <text
        x={cx} y={cy}
        textAnchor="middle" dominantBaseline="central"
        fill="white"
        fontSize={fontSize}
        fontWeight="bold"
        fontFamily="'Courier New', monospace"
        style={{ userSelect: 'none' }}
      >
        {displayText}
      </text>

      {(() => {
        const ALL_EDGES: PortDir[] = ['up', 'down', 'left', 'right'];
        let lpEdges: PortDir[] = [];
        let radEdges: PortDir[] = [];
        
        if (bondedEdges) {
          const freeEdges = ALL_EDGES.filter(e => !bondedEdges.includes(e));
          const numConsumedRadicals = connectedPorts.length;
          const numRemainingRadicals = Math.max(0, template.ports.length - numConsumedRadicals);
          const numLonePairs = template.lonePairs?.length || 0;
          
          const naturalRadEdges = template.ports.map(p => rotateDir(p.dir as PortDir, rotation as Rotation));
          const naturalLPEdges = template.lonePairs?.map(lp => rotateDir(lp as PortDir, rotation as Rotation)) || [];
          
          // Allocate free edges to radicals, preferring natural directions
          for (const edge of naturalRadEdges) {
            if (freeEdges.includes(edge) && radEdges.length < numRemainingRadicals) {
              radEdges.push(edge);
              freeEdges.splice(freeEdges.indexOf(edge), 1);
            }
          }
          while(radEdges.length < numRemainingRadicals && freeEdges.length > 0) {
            radEdges.push(freeEdges.shift()!);
          }
          
          // Allocate free edges to lone pairs, preferring natural directions
          for (const edge of naturalLPEdges) {
            if (freeEdges.includes(edge) && lpEdges.length < numLonePairs) {
              lpEdges.push(edge);
              freeEdges.splice(freeEdges.indexOf(edge), 1);
            }
          }
          while(lpEdges.length < numLonePairs && freeEdges.length > 0) {
            lpEdges.push(freeEdges.shift()!);
          }
        } else {
          // Fallback for Palette rendering
          lpEdges = template.lonePairs?.map(lp => rotateDir(lp as PortDir, rotation as Rotation)) || [];
          radEdges = template.ports.filter(p => !connectedPorts.includes(p.id)).map(p => rotateDir(p.dir as PortDir, rotation as Rotation));
        }

        return (
          <>
            {/* ── Lone pair dots ── */}
            {lpEdges.map((dir, i) => {
              const [ex, ey] = edgeMidpoint(dir, size);
              const spacing = lpDotR * 2.0;
              let ox = 0, oy = 0;
              if (dir === 'left' || dir === 'right') oy = spacing;
              else ox = spacing;
              return (
                <g key={`lp-${dir}-${i}`}>
                  <circle cx={ex - ox} cy={ey - oy} r={lpDotR} fill="#d0d0d0" opacity={0.9} />
                  <circle cx={ex + ox} cy={ey + oy} r={lpDotR} fill="#d0d0d0" opacity={0.9} />
                </g>
              );
            })}

            {/* ── Radical dots ── */}
            {radEdges.map((dir, i) => {
              const [ex, ey] = edgeMidpoint(dir, size);
              const isGlowing = glowPorts && glowPorts.length > 0;
              const dotColor = isGlowing ? '#00ff88' : '#FFD600';
              const r = isGlowing ? dotR * 1.6 : dotR;
              const filterStr = isGlowing
                ? `drop-shadow(0 0 5px ${dotColor})`
                : `drop-shadow(0 0 2px #00000088)`;

              return (
                <circle
                  key={`rad-${dir}-${i}`}
                  cx={ex} cy={ey}
                  r={r}
                  fill={dotColor}
                  stroke="#00000044"
                  strokeWidth="1"
                  style={{ filter: filterStr, transition: 'r 0.15s, fill 0.15s' }}
                />
              );
            })}
          </>
        );
      })()}
    </svg>
  );
}
