import type { MoleculeState, Connection, PlacedBlock } from '../types/molecule';
import { getTemplate } from '../data/blockTemplates';

/**
 * Converts the molecule graph (blocks + connections) into a SMILES string.
 * Uses a DFS traversal starting from the first block.
 */
export function generateSMILES(state: MoleculeState): string {
  if (state.blocks.length === 0) return '';

  const { blocks, connections } = state;

  // Build adjacency list: instanceId -> [{neighborId, bond, fromPort, toPort}]
  const adj = new Map<string, { id: string; bond: Connection }[]>();
  for (const b of blocks) adj.set(b.instanceId, []);
  for (const c of connections) {
    adj.get(c.fromInstance)!.push({ id: c.toInstance, bond: c });
    adj.get(c.toInstance)!.push({ id: c.fromInstance, bond: c });
  }

  const bondChar = (c: Connection) => {
    switch (c.bondType) {
      case 'double': return '=';
      case 'triple': return '#';
      default: return '';
    }
  };

  const visited = new Set<string>();

  function dfs(instanceId: string): string {
    visited.add(instanceId);
    const block = blocks.find((b) => b.instanceId === instanceId)!;
    const tpl = getTemplate(block.templateId);
    if (!tpl) return '?';

    let smiles = tpl.smilesAtom;
    const neighbors = adj.get(instanceId) ?? [];
    const children: string[] = [];

    for (const { id: neighborId, bond } of neighbors) {
      if (visited.has(neighborId)) continue;
      const childSmiles = bondChar(bond) + dfs(neighborId);
      children.push(childSmiles);
    }

    if (children.length === 1) smiles += children[0];
    else if (children.length > 1) {
      smiles += children.slice(0, -1).map((c) => `(${c})`).join('');
      smiles += children[children.length - 1];
    }

    return smiles;
  }

  // Start from first block
  return dfs(blocks[0].instanceId);
}

/**
 * Checks whether all ports on all blocks are connected.
 * If so, the molecule is "complete".
 */
export function isMoleculeComplete(state: MoleculeState): boolean {
  if (state.blocks.length === 0) return false;
  for (const block of state.blocks) {
    for (const port of block.ports) {
      if (!port.connectedTo) return false;
    }
  }
  return true;
}

/**
 * Returns a list of blocks with at least one unconnected port.
 */
export function getOpenBlocks(state: MoleculeState): PlacedBlock[] {
  return state.blocks.filter((b) => b.ports.some((p) => !p.connectedTo));
}
