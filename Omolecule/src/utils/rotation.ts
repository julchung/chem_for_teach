import type { PortDir } from '../types/molecule';

export type Rotation = 0 | 90 | 180 | 270;

const DIRS: PortDir[] = ['right', 'down', 'left', 'up'];

/** Rotate a port direction clockwise by `rotation` degrees */
export function rotateDir(dir: PortDir, rotation: Rotation): PortDir {
  const idx = DIRS.indexOf(dir);
  const steps = rotation / 90;
  return DIRS[(idx + steps) % 4];
}

/** Return the opposite direction */
export function oppositeDir(dir: PortDir): PortDir {
  const opp: Record<PortDir, PortDir> = {
    left: 'right', right: 'left', up: 'down', down: 'up',
  };
  return opp[dir];
}

/**
 * Given a block template's ports (with their original directions),
 * find the rotation (0/90/180/270) that puts a port of matching `bondType`
 * as close as possible to `wantedDir`.
 */
export function findBestRotation(
  ports: Array<{ dir: PortDir; bondType: string }>,
  wantedDir: PortDir,
  wantedBondType: string,
): Rotation {
  let bestRot: Rotation = 0;
  let bestScore = -1;

  for (const rot of [0, 90, 180, 270] as Rotation[]) {
    for (const p of ports) {
      if (p.bondType !== wantedBondType) continue;
      const rotated = rotateDir(p.dir, rot);
      // Score: exact match = 2, adjacent = 1
      const score = rotated === wantedDir ? 2 : 1;
      if (score > bestScore) {
        bestScore = score;
        bestRot = rot;
      }
      if (bestScore === 2) break;
    }
    if (bestScore === 2) break;
  }
  return bestRot;
}

/**
 * Dominant axis direction from point A to point B.
 * Returns the cardinal direction (left/right/up/down) of the larger component.
 */
export function dominantDir(ax: number, ay: number, bx: number, by: number): PortDir {
  const dx = bx - ax;
  const dy = by - ay;
  if (Math.abs(dx) >= Math.abs(dy)) return dx >= 0 ? 'right' : 'left';
  return dy >= 0 ? 'down' : 'up';
}

/**
 * Given the rotation and a port direction, return the pixel offset
 * from the block's top-left corner for that port.
 */
export function portOffset(
  dir: PortDir,
  rotation: Rotation,
  blockPx: number,
  armRatio = 0.34,
): { px: number; py: number } {
  const arm = blockPx * armRatio;
  const cx = blockPx / 2;
  const cy = blockPx / 2;
  const rotated = rotateDir(dir, rotation);
  switch (rotated) {
    case 'right': return { px: cx + arm, py: cy };
    case 'left':  return { px: cx - arm, py: cy };
    case 'up':    return { px: cx,       py: cy - arm };
    case 'down':  return { px: cx,       py: cy + arm };
  }
}

/**
 * Compute where a block's top-left should be so that its `connectingPortDir`
 * (after rotation) aligns with world point (tx, ty).
 */
export function snapBlockPosition(
  connectingPortDir: PortDir,
  rotation: Rotation,
  tx: number,
  ty: number,
  blockPx: number,
  armRatio = 0.34,
): { x: number; y: number } {
  const { px, py } = portOffset(connectingPortDir, rotation, blockPx, armRatio);
  return { x: tx - px, y: ty - py };
}
