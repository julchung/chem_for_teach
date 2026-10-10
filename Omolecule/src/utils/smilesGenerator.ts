import type { MoleculeState, Connection, PlacedBlock } from '../types/molecule';
import { getTemplate } from '../data/blockTemplates';

/**
 * Converts the molecule graph (blocks + connections) into a SMILES string.
 * Uses a DFS traversal starting from the first block.
 */
export function generateSMILES(state: MoleculeState): string {
  if (state.blocks.length === 0) return '';

  const { blocks, connections } = state;

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
  let ringCounter = 1;
  const backEdges = new Map<string, { ringId: number, bond: Connection }[]>();

  // Pass 1: DFS to find spanning tree and back-edges
  function findBackEdges(instanceId: string, parentId: string | null) {
    visited.add(instanceId);
    const neighbors = adj.get(instanceId) ?? [];
    for (const { id: neighborId, bond } of neighbors) {
      if (neighborId === parentId) continue;
      if (visited.has(neighborId)) {
        // Back-edge found! Only assign ringId once per edge (e.g., when reaching the already-visited node)
        // To avoid duplicate assignment, we check if the reverse edge is already recorded.
        let alreadyRecorded = false;
        const targetEdges = backEdges.get(neighborId) || [];
        for (const te of targetEdges) {
          if (te.bond === bond) alreadyRecorded = true;
        }
        
        if (!alreadyRecorded) {
          const ringId = ringCounter++;
          if (!backEdges.has(instanceId)) backEdges.set(instanceId, []);
          if (!backEdges.has(neighborId)) backEdges.set(neighborId, []);
          backEdges.get(instanceId)!.push({ ringId, bond });
          backEdges.get(neighborId)!.push({ ringId, bond });
        }
      } else {
        findBackEdges(neighborId, instanceId);
      }
    }
  }

  findBackEdges(blocks[0].instanceId, null);

  visited.clear();
  const ringClosuresUsed = new Set<number>();

  // Pass 2: DFS to build SMILES
  function dfs(instanceId: string, parentId: string | null): string {
    visited.add(instanceId);
    const block = blocks.find((b) => b.instanceId === instanceId)!;
    const tpl = getTemplate(block.templateId);
    if (!tpl) return '?';

    let smiles = tpl.smilesAtom;
    
    // Add ring numbers for back-edges connected to this atom
    const myBackEdges = backEdges.get(instanceId) || [];
    for (const { ringId, bond } of myBackEdges) {
      // If it's the second time we see the ring closure, we can prefix the bond symbol
      if (ringClosuresUsed.has(ringId)) {
         // Second visitation: append bond type before the ring number if needed
         // However, standard SMILES often allows just repeating the ring number and it infers single.
         // Actually, appending bondChar(bond) + ringId works (e.g. C=1)
         const bChar = bondChar(bond);
         smiles += `${bChar}${ringId}`;
      } else {
         ringClosuresUsed.add(ringId);
         smiles += `${ringId}`;
      }
    }

    const neighbors = adj.get(instanceId) ?? [];
    const children: string[] = [];

    for (const { id: neighborId, bond } of neighbors) {
      if (neighborId === parentId) continue;
      // Skip if this edge is a back-edge (already handled via ring numbers)
      const isBackEdge = myBackEdges.some(be => be.bond === bond);
      if (isBackEdge) continue;

      if (!visited.has(neighborId)) {
        const childSmiles = bondChar(bond) + dfs(neighborId, instanceId);
        children.push(childSmiles);
      }
    }

    if (children.length === 1) smiles += children[0];
    else if (children.length > 1) {
      smiles += children.slice(0, -1).map((c) => `(${c})`).join('');
      smiles += children[children.length - 1];
    }

    return smiles;
  }

  return dfs(blocks[0].instanceId, null);
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
