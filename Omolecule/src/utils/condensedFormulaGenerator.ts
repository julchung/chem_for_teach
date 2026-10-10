import type { MoleculeState, Connection } from '../types/molecule';
import { getTemplate } from '../data/blockTemplates';

export function generateCondensedFormula(state: MoleculeState): string {
  if (state.blocks.length === 0) return '';

  const { blocks, connections } = state;

  // Build adjacency list
  const adj = new Map<string, { id: string; bond: Connection }[]>();
  for (const b of blocks) adj.set(b.instanceId, []);
  for (const c of connections) {
    adj.get(c.fromInstance)!.push({ id: c.toInstance, bond: c });
    adj.get(c.toInstance)!.push({ id: c.fromInstance, bond: c });
  }

  // Precompute collapsed text for heavy atoms
  const heavyAtoms = new Set<string>();
  const collapsedText = new Map<string, string>();

  for (const block of blocks) {
    const tpl = getTemplate(block.templateId);
    if (!tpl) continue;
    
    // If it's a hydrogen, skip (we count it on its heavy neighbor)
    if (tpl.element === 'H') continue;

    heavyAtoms.add(block.instanceId);

    // If it already has collapsedText (like "CH3"), use it.
    if (block.collapsedText) {
      collapsedText.set(block.instanceId, block.collapsedText);
      continue;
    }

    let hCount = 0;
    const neighbors = adj.get(block.instanceId) || [];
    for (const n of neighbors) {
      const neighborBlock = blocks.find(b => b.instanceId === n.id);
      const nTpl = neighborBlock ? getTemplate(neighborBlock.templateId) : null;
      if (nTpl && nTpl.element === 'H') {
        hCount++;
      }
    }

    let text = tpl.label || tpl.element || '';
    // Replace subscript digits if any
    text = text.replace(/₂/g, '2').replace(/₃/g, '3');

    if (hCount === 1) text += 'H';
    else if (hCount > 1) text += `H${hCount}`;
    
    // Some basic heuristics for common groups formatting
    if (text === 'OH') text = '(OH)'; // E.g., for alcohol
    else if (text === 'NH2') text = '(NH2)';

    collapsedText.set(block.instanceId, text);
  }

  if (heavyAtoms.size === 0) {
    // Maybe it's just H2?
    if (blocks.length === 2 && getTemplate(blocks[0].templateId)?.element === 'H') return 'H2';
    return '';
  }

  // Find the leftmost terminal heavy atom as the starting point
  let startNode = Array.from(heavyAtoms)[0];
  let minGridX = Infinity;
  for (const id of heavyAtoms) {
    const heavyNeighbors = (adj.get(id) || []).filter(n => heavyAtoms.has(n.id));
    if (heavyNeighbors.length <= 1) {
      const block = blocks.find(b => b.instanceId === id);
      if (block && block.gridX < minGridX) {
        minGridX = block.gridX;
        startNode = id;
      }
    }
  }

  let ringCounter = 1;
  const backEdges = new Map<string, { ringId: number, bond: Connection }[]>();

  // Pass 1: DFS to find back-edges (rings)
  const ringVisited = new Set<string>();
  function findBackEdges(instanceId: string, parentId: string | null) {
    ringVisited.add(instanceId);
    const neighbors = adj.get(instanceId) ?? [];
    for (const { id: neighborId, bond } of neighbors) {
      if (!heavyAtoms.has(neighborId)) continue;
      if (neighborId === parentId) continue;
      if (ringVisited.has(neighborId)) {
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

  if (heavyAtoms.size > 0) {
    findBackEdges(startNode, null);
  }

  const visited = new Set<string>();
  const ringClosuresUsed = new Set<number>();

  function bondChar(c: Connection) {
    switch (c.bondType) {
      case 'double': return '=';
      case 'triple': return '≡';
      default: return '';
    }
  }

  function dfs(instanceId: string, parentId: string | null): string {
    visited.add(instanceId);
    let str = collapsedText.get(instanceId) || '';

    // Append ring numbers
    const myBackEdges = backEdges.get(instanceId) || [];
    for (const { ringId, bond } of myBackEdges) {
      if (ringClosuresUsed.has(ringId)) {
         const bChar = bondChar(bond);
         str += `${bChar}${ringId}`;
      } else {
         ringClosuresUsed.add(ringId);
         str += `${ringId}`;
      }
    }

    // Sort heavy neighbors left-to-right based on their block's gridX
    let heavyNeighbors = (adj.get(instanceId) || []).filter(n => heavyAtoms.has(n.id));
    heavyNeighbors.sort((a, b) => {
      const blockA = blocks.find(blk => blk.instanceId === a.id);
      const blockB = blocks.find(blk => blk.instanceId === b.id);
      return (blockA?.gridX || 0) - (blockB?.gridX || 0);
    });

    const children: string[] = [];

    for (const { id: neighborId, bond } of heavyNeighbors) {
      if (neighborId === parentId) continue;
      const isBackEdge = myBackEdges.some(be => be.bond === bond);
      if (isBackEdge) continue;

      if (!visited.has(neighborId)) {
        const bChar = bondChar(bond);
        const childStr = dfs(neighborId, instanceId);
        children.push(bChar + childStr);
      }
    }

    if (children.length === 1) {
      str += children[0];
    } else if (children.length > 1) {
      str += children.slice(0, -1).map(c => `(${c})`).join('');
      str += children[children.length - 1];
    }

    return str;
  }
  return dfs(startNode, null);
}
