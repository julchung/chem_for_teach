import { useState, useCallback } from 'react';
import { v4 as uuidv4 } from 'uuid';
import type {
  MoleculeState,
  PlacedBlock,
  Connection,
  PortDir,
} from '../types/molecule';
import type { Rotation } from '../utils/rotation';
import { getTemplate } from '../data/blockTemplates';
import { getGroupTemplate } from '../data/groupTemplates';
export function useMolecule() {
  const [state, setState] = useState<MoleculeState>({ blocks: [], connections: [] });

  // ── Helper: Update CHx Text ──────────────────────────────────────────────
  const updateCollapsedText = (blocks: PlacedBlock[], connections: Connection[]): PlacedBlock[] => {
    return blocks.map(b => {
      if (b.templateId !== 'elem_C') return b;
      
      // Count hidden hydrogens connected to this carbon
      const hiddenHCount = connections.filter(c => {
        const isFrom = c.fromInstance === b.instanceId;
        const isTo = c.toInstance === b.instanceId;
        if (!isFrom && !isTo) return false;
        
        const partnerId = isFrom ? c.toInstance : c.fromInstance;
        const partner = blocks.find(pb => pb.instanceId === partnerId);
        return partner?.templateId === 'elem_H' && partner.isHidden;
      }).length;

      let text = undefined;
      if (hiddenHCount === 1) text = 'CH';
      else if (hiddenHCount === 2) text = 'CH₂';
      else if (hiddenHCount === 3) text = 'CH₃';
      else if (hiddenHCount === 4) text = 'CH₄';

      return { ...b, collapsedText: text };
    });
  };

  // ── Single block ────────────────────────────────────────────────────────
  const addBlock = useCallback((templateId: string, gridX: number, gridY: number): string => {
    const tpl = getTemplate(templateId);
    if (!tpl) return '';
    const instanceId = uuidv4();
    const newBlock: PlacedBlock = {
      instanceId,
      templateId,
      gridX,
      gridY,
      rotation: 0,
      ports: tpl.ports.map((p) => ({ ...p, connectedTo: undefined })),
    };
    setState((prev) => ({ ...prev, blocks: [...prev.blocks, newBlock] }));
    return instanceId;
  }, []);

  // ── Compound group (multi-block) ────────────────────────────────────────
  const addGroup = useCallback((groupId: string, gridX: number, gridY: number): string => {
    const grp = getGroupTemplate(groupId);
    if (!grp) return '';

    const idMap: Record<string, string> = {};
    const newBlocks: PlacedBlock[] = [];

    for (const atomDef of grp.atoms) {
      const instanceId = uuidv4();
      idMap[atomDef.localId] = instanceId;
      const tpl = getTemplate(atomDef.templateId);
      if (!tpl) continue;
      newBlocks.push({
        instanceId,
        templateId: atomDef.templateId,
        gridX: gridX + atomDef.relX,
        gridY: gridY + atomDef.relY,
        rotation: 0,
        ports: tpl.ports.map((p) => ({ ...p, connectedTo: undefined })),
      });
    }

    const newConnections: Connection[] = [];
    for (const bondDef of grp.bonds) {
      const fromInstanceId = idMap[bondDef.fromLocalId];
      const toInstanceId   = idMap[bondDef.toLocalId];
      const fromBlock = newBlocks.find((b) => b.instanceId === fromInstanceId);
      const toBlock   = newBlocks.find((b) => b.instanceId === toInstanceId);
      if (!fromBlock || !toBlock) continue;

      const fromPort = fromBlock.ports.find((p) => p.id === bondDef.fromPortId);
      if (!fromPort) continue;

      fromBlock.ports = fromBlock.ports.map((p) =>
        p.id === bondDef.fromPortId ? { ...p, connectedTo: `${toInstanceId}:${bondDef.toPortId}` } : p
      );
      toBlock.ports = toBlock.ports.map((p) =>
        p.id === bondDef.toPortId ? { ...p, connectedTo: `${fromInstanceId}:${bondDef.fromPortId}` } : p
      );

      newConnections.push({
        fromInstance: fromInstanceId,
        fromPort:     bondDef.fromPortId,
        toInstance:   toInstanceId,
        toPort:       bondDef.toPortId,
        bondType:     fromPort.bondType,
      });
    }

    setState((prev) => ({
      blocks:      [...prev.blocks, ...newBlocks],
      connections: [...prev.connections, ...newConnections],
    }));

    return idMap[grp.headId] ?? '';
  }, []);

  // ── Move ────────────────────────────────────────────────────────────────
  const moveBlock = useCallback((instanceId: string, gridX: number, gridY: number) => {
    setState((prev) => {
      // Update position first
      let newBlocks = prev.blocks.map((b) =>
        b.instanceId === instanceId ? { ...b, gridX, gridY } : b
      );

      // After moving, re-compute rotation for this block and its bonded neighbors
      const movedBlock = newBlocks.find(b => b.instanceId === instanceId);
      if (movedBlock) {
        for (const conn of prev.connections) {
          const isFrom = conn.fromInstance === instanceId;
          const isTo   = conn.toInstance   === instanceId;
          if (!isFrom && !isTo) continue;

          const myPortId  = isFrom ? conn.fromPort : conn.toPort;
          const partnerId = isFrom ? conn.toInstance : conn.fromInstance;
          const partnerPortId = isFrom ? conn.toPort : conn.fromPort;
          const partner = newBlocks.find(b => b.instanceId === partnerId);
          if (!partner) continue;

          const dx = partner.gridX - gridX;
          const dy = partner.gridY - gridY;
          let bondDir: PortDir = 'right';
          if (Math.abs(dx) >= Math.abs(dy)) {
            bondDir = dx >= 0 ? 'right' : 'left';
          } else {
            bondDir = dy >= 0 ? 'down' : 'up';
          }
          const oppDir: PortDir = bondDir === 'right' ? 'left' : bondDir === 'left' ? 'right' : bondDir === 'up' ? 'down' : 'up';

          const DIRS: PortDir[] = ['right', 'down', 'left', 'up'];
          const myTpl = getTemplate(movedBlock.templateId);
          const myPortBase = myTpl?.ports.find(p => p.id === myPortId);
          if (myPortBase) {
            const myConnCount = prev.connections.filter(c => c.fromInstance === instanceId || c.toInstance === instanceId).length;
            if (myConnCount <= 1) {
              const baseIdx = DIRS.indexOf(myPortBase.dir as PortDir);
              const reqIdx  = DIRS.indexOf(bondDir);
              const steps = (reqIdx - baseIdx + 4) % 4;
              const newRot = (steps * 90) as 0|90|180|270;
              newBlocks = newBlocks.map(b => b.instanceId === instanceId ? { ...b, rotation: newRot } : b);
            }
          }

          const partnerTpl = getTemplate(partner.templateId);
          const partnerPortBase = partnerTpl?.ports.find(p => p.id === partnerPortId);
          if (partnerPortBase) {
            const partnerConnCount = prev.connections.filter(c => c.fromInstance === partnerId || c.toInstance === partnerId).length;
            if (partnerConnCount <= 1) {
              const baseIdx = DIRS.indexOf(partnerPortBase.dir as PortDir);
              const reqIdx  = DIRS.indexOf(oppDir);
              const steps = (reqIdx - baseIdx + 4) % 4;
              const newRot = (steps * 90) as 0|90|180|270;
              newBlocks = newBlocks.map(b => b.instanceId === partnerId ? { ...b, rotation: newRot } : b);
            }
          }
        }
      }

      return { ...prev, blocks: newBlocks };
    });
  }, []);

  const moveBlocks = useCallback((ids: string[], dx: number, dy: number) => {
    const idSet = new Set(ids);
    setState((prev) => ({
      ...prev,
      blocks: prev.blocks.map((b) =>
        idSet.has(b.instanceId)
          ? { ...b, gridX: b.gridX + dx, gridY: b.gridY + dy }
          : b
      ),
    }));
  }, []);

  // ── Rotation ────────────────────────────────────────────────────────────
  const setBlockRotation = useCallback((instanceId: string, rotation: Rotation) => {
    setState((prev) => {
      const block = prev.blocks.find((b) => b.instanceId === instanceId);
      if (!block || block.rotation === rotation) return prev;
      return {
        ...prev,
        blocks: prev.blocks.map((b) =>
          b.instanceId === instanceId ? { ...b, rotation } : b
        ),
      };
    });
  }, []);

  // ── Remove single block ─────────────────────────────────────────────────
  const removeBlock = useCallback((instanceId: string) => {
    setState((prev) => {
      const newConnections = prev.connections.filter(
        (c) => c.fromInstance !== instanceId && c.toInstance !== instanceId
      );
      const removedConns = prev.connections.filter(
        (c) => c.fromInstance === instanceId || c.toInstance === instanceId
      );
      // Track which OTHER blocks lose all their connections
      const affectedPartnerIds = new Set<string>();
      const affectedPortKeys = new Set<string>();
      for (const rc of removedConns) {
        affectedPortKeys.add(`${rc.fromInstance}:${rc.fromPort}`);
        affectedPortKeys.add(`${rc.toInstance}:${rc.toPort}`);
        const partnerId = rc.fromInstance === instanceId ? rc.toInstance : rc.fromInstance;
        affectedPartnerIds.add(partnerId);
      }
      let newBlocks = prev.blocks
        .filter((b) => b.instanceId !== instanceId)
        .map((b) => {
          const isAffected = affectedPartnerIds.has(b.instanceId);
          const stillConnected = newConnections.some(c => c.fromInstance === b.instanceId || c.toInstance === b.instanceId);
          return {
            ...b,
            rotation: (isAffected && !stillConnected ? 0 : b.rotation) as 0|90|180|270,
            ports: b.ports.map((p) => {
              if (affectedPortKeys.has(`${b.instanceId}:${p.id}`) || p.connectedTo === `consumed_by_${instanceId}`) {
                return { ...p, connectedTo: undefined, bondType: 'single' as const };
              }
              return p;
            }),
          };
        });
      
      newBlocks = updateCollapsedText(newBlocks, newConnections);
      return { blocks: newBlocks, connections: newConnections };
    });
  }, []);

  // ── Remove multiple blocks ───────────────────────────────────────────────
  const removeBlocks = useCallback((ids: string[]) => {
    if (ids.length === 0) return;
    const idSet = new Set(ids);
    setState((prev) => {
      const newConnections = prev.connections.filter(
        (c) => !idSet.has(c.fromInstance) && !idSet.has(c.toInstance)
      );
      const removedConns = prev.connections.filter(
        (c) => idSet.has(c.fromInstance) || idSet.has(c.toInstance)
      );
      const affectedPartnerIds = new Set<string>();
      const affectedPortKeys = new Set<string>();
      for (const rc of removedConns) {
        affectedPortKeys.add(`${rc.fromInstance}:${rc.fromPort}`);
        affectedPortKeys.add(`${rc.toInstance}:${rc.toPort}`);
        if (!idSet.has(rc.fromInstance)) affectedPartnerIds.add(rc.fromInstance);
        if (!idSet.has(rc.toInstance))   affectedPartnerIds.add(rc.toInstance);
      }
      let newBlocks = prev.blocks
        .filter((b) => !idSet.has(b.instanceId))
        .map((b) => {
          const isAffected = affectedPartnerIds.has(b.instanceId);
          const stillConnected = newConnections.some(c => c.fromInstance === b.instanceId || c.toInstance === b.instanceId);
          return {
            ...b,
            rotation: (isAffected && !stillConnected ? 0 : b.rotation) as 0|90|180|270,
            ports: b.ports.map((p) => {
              let isConsumedByRemoved = false;
              if (p.connectedTo && p.connectedTo.startsWith('consumed_by_')) {
                const targetId = p.connectedTo.replace('consumed_by_', '');
                if (idSet.has(targetId)) isConsumedByRemoved = true;
              }
              
              if (affectedPortKeys.has(`${b.instanceId}:${p.id}`) || isConsumedByRemoved) {
                return { ...p, connectedTo: undefined, bondType: 'single' as const };
              }
              return p;
            }),
          };
        });
      
      newBlocks = updateCollapsedText(newBlocks, newConnections);
      return { blocks: newBlocks, connections: newConnections };
    });
  }, []);

  // ── Connect Ports ───────────────────────────────────────────────────────
  const connectPorts = useCallback((fromInstanceId: string, fromPortId: string, toInstanceId: string, toPortId: string) => {
    setState((prev) => {
      const fromBlock = prev.blocks.find((b) => b.instanceId === fromInstanceId);
      const toBlock   = prev.blocks.find((b) => b.instanceId === toInstanceId);
      if (!fromBlock || !toBlock) return prev;

      const fromPortDef = fromBlock.ports.find((p) => p.id === fromPortId);
      const toPortDef   = toBlock.ports.find((p)   => p.id === toPortId);
      if (!fromPortDef || !toPortDef || fromPortDef.connectedTo || toPortDef.connectedTo) return prev;

      // Prevent multiple connections between the same two blocks automatically
      const alreadyConnected = prev.connections.some(
        c => (c.fromInstance === fromInstanceId && c.toInstance === toInstanceId) ||
             (c.fromInstance === toInstanceId && c.toInstance === fromInstanceId)
      );
      if (alreadyConnected) return prev;

      const conn: Connection = {
        fromInstance: fromInstanceId,
        fromPort:     fromPortId,
        toInstance:   toInstanceId,
        toPort:       toPortId,
        bondType:     'single',
      };

      // Determine the direction from fromBlock to toBlock
      const dx = toBlock.gridX - fromBlock.gridX;
      const dy = toBlock.gridY - fromBlock.gridY;
      let bondDir: PortDir = 'right';
      if (Math.abs(dx) >= Math.abs(dy)) {
        bondDir = dx >= 0 ? 'right' : 'left';
      } else {
        bondDir = dy >= 0 ? 'down' : 'up';
      }

      // Compute correct rotation for fromBlock so that fromPortId points toward toBlock
      const fromTpl = getTemplate(fromBlock.templateId);
      const fromPortBase = fromTpl?.ports.find(p => p.id === fromPortId);
      let fromRotation = fromBlock.rotation;
      const isFromConnected = prev.connections.some(c => c.fromInstance === fromInstanceId || c.toInstance === fromInstanceId);
      if (fromPortBase && !isFromConnected) {
        const DIRS: PortDir[] = ['right', 'down', 'left', 'up'];
        const baseIdx = DIRS.indexOf(fromPortBase.dir as PortDir);
        const reqIdx  = DIRS.indexOf(bondDir);
        const steps = (reqIdx - baseIdx + 4) % 4;
        fromRotation = (steps * 90) as 0|90|180|270;
      }

      // Compute correct rotation for toBlock so that toPortId points back
      const oppDir: PortDir = bondDir === 'right' ? 'left' : bondDir === 'left' ? 'right' : bondDir === 'up' ? 'down' : 'up';
      const toTpl = getTemplate(toBlock.templateId);
      const toPortBase = toTpl?.ports.find(p => p.id === toPortId);
      let toRotation = toBlock.rotation;
      const isToConnected = prev.connections.some(c => c.fromInstance === toInstanceId || c.toInstance === toInstanceId);
      if (toPortBase && !isToConnected) {
        const DIRS: PortDir[] = ['right', 'down', 'left', 'up'];
        const baseIdx = DIRS.indexOf(toPortBase.dir as PortDir);
        const reqIdx  = DIRS.indexOf(oppDir);
        const steps = (reqIdx - baseIdx + 4) % 4;
        toRotation = (steps * 90) as 0|90|180|270;
      }

      let newBlocks = prev.blocks.map((b) => {
        if (b.instanceId === fromInstanceId) {
          return {
            ...b,
            rotation: fromRotation,
            ports: b.ports.map((p) => p.id === fromPortId ? { ...p, connectedTo: `${toInstanceId}:${toPortId}` } : p),
          };
        }
        if (b.instanceId === toInstanceId) {
          return {
            ...b,
            rotation: toRotation,
            ports: b.ports.map((p) => p.id === toPortId ? { ...p, connectedTo: `${fromInstanceId}:${fromPortId}` } : p),
          };
        }
        return b;
      });

      // Handle CHx collapsing
      if (fromBlock.templateId === 'elem_C' && toBlock.templateId === 'elem_H') {
        newBlocks = newBlocks.map(b => b.instanceId === toInstanceId ? { ...b, isHidden: true } : b);
      } else if (fromBlock.templateId === 'elem_H' && toBlock.templateId === 'elem_C') {
        newBlocks = newBlocks.map(b => b.instanceId === fromInstanceId ? { ...b, isHidden: true } : b);
      }

      newBlocks = updateCollapsedText(newBlocks, [...prev.connections, conn]);

      return { blocks: newBlocks, connections: [...prev.connections, conn] };
    });
  }, []);

  // ── Disconnect a block ──────────────────────────────────────────────────
  const disconnectBlock = useCallback((instanceId: string) => {
    setState((prev) => {
      const newConnections = prev.connections.filter(
        (c) => c.fromInstance !== instanceId && c.toInstance !== instanceId
      );
      const removedConns = prev.connections.filter(
        (c) => c.fromInstance === instanceId || c.toInstance === instanceId
      );
      const affectedPartnerIds = new Set<string>();
      for (const rc of removedConns) {
        const partnerId = rc.fromInstance === instanceId ? rc.toInstance : rc.fromInstance;
        affectedPartnerIds.add(partnerId);
      }
      
      let newBlocks = prev.blocks.map((b) => {
        if (b.instanceId === instanceId) {
          return { ...b, rotation: 0 as const, ports: b.ports.map((p) => ({ ...p, connectedTo: undefined, bondType: 'single' as const })) };
        }
        if (affectedPartnerIds.has(b.instanceId)) {
          const stillConnected = newConnections.some(c => c.fromInstance === b.instanceId || c.toInstance === b.instanceId);
          return {
            ...b,
            rotation: (stillConnected ? b.rotation : 0) as 0|90|180|270,
            ports: b.ports.map((p) => {
              if (p.connectedTo && (p.connectedTo.split(':')[0] === instanceId || p.connectedTo === `consumed_by_${instanceId}`)) {
                return { ...p, connectedTo: undefined, bondType: 'single' as const };
              }
              return p;
            }),
          };
        }
        return b;
      });
      newBlocks = updateCollapsedText(newBlocks, newConnections);
      return { blocks: newBlocks, connections: newConnections };
    });
  }, []);

  // ── Uncollapse CHx ──────────────────────────────────────────────────────
  const uncollapseHydrogens = useCallback((instanceId: string) => {
    setState((prev) => {
      const block = prev.blocks.find(b => b.instanceId === instanceId);
      if (!block || block.templateId !== 'elem_C') return prev;

      // Find all connected hidden hydrogens
      const connectedHiddenH = prev.connections
        .filter(c => c.fromInstance === instanceId || c.toInstance === instanceId)
        .map(c => {
          const partnerId = c.fromInstance === instanceId ? c.toInstance : c.fromInstance;
          return prev.blocks.find(b => b.instanceId === partnerId);
        })
        .filter(b => b && b.templateId === 'elem_H' && b.isHidden);

      if (connectedHiddenH.length === 0) return prev;

      let newBlocks = prev.blocks.map(b => {
        if (connectedHiddenH.some(h => h!.instanceId === b.instanceId)) {
          return { ...b, isHidden: false }; // Unhide
        }
        return b;
      });

      newBlocks = updateCollapsedText(newBlocks, prev.connections);
      return { blocks: newBlocks, connections: prev.connections };
    });
  }, []);

  // ── Upgrade bond ────────────────────────────────────────────────────────
  const upgradeBond = useCallback((fromInstanceId: string, toInstanceId: string) => {
    setState((prev) => {
      const conn = prev.connections.find(
        (c) =>
          (c.fromInstance === fromInstanceId && c.toInstance === toInstanceId) ||
          (c.fromInstance === toInstanceId   && c.toInstance === fromInstanceId)
      );
      if (!conn) return prev;

      const fromBlock = prev.blocks.find(b => b.instanceId === conn.fromInstance);
      const toBlock = prev.blocks.find(b => b.instanceId === conn.toInstance);
      if (!fromBlock || !toBlock) return prev;

      const nextBond: 'single' | 'double' | 'triple' | 'break' =
        conn.bondType === 'single' ? 'double' :
        conn.bondType === 'double' ? 'triple' : 'break';

      const fromFree = fromBlock.ports.filter(p => !p.connectedTo).length;
      const toFree = toBlock.ports.filter(p => !p.connectedTo).length;

      let finalBond = nextBond;
      if (nextBond !== 'break') {
        if (fromFree < 1 || toFree < 1) {
          finalBond = 'break'; // Not enough radicals, break immediately
        }
      }

      if (finalBond === 'break') {
        // Disconnect completely and reset rotations for now-isolated atoms
        // Must also clear consumed_by_ ports created by double/triple bonds
        const newConnections = prev.connections.filter(c => c !== conn);
        const newBlocks = prev.blocks.map(b => {
          const isFrom = b.instanceId === conn.fromInstance;
          const isTo   = b.instanceId === conn.toInstance;
          if (isFrom || isTo) {
            const stillConnected = newConnections.some(c => c.fromInstance === b.instanceId || c.toInstance === b.instanceId);
            const partnerId = isFrom ? conn.toInstance : conn.fromInstance;
            return {
              ...b,
              rotation: (stillConnected ? b.rotation : 0) as 0|90|180|270,
              ports: b.ports.map(p => {
                // Clear direct bond port: connectedTo = "partnerId:portId"
                if (p.connectedTo && p.connectedTo.split(':')[0] === partnerId) {
                  return { ...p, connectedTo: undefined, bondType: 'single' as const };
                }
                // Clear consumed port: connectedTo = "consumed_by_partnerId"
                if (p.connectedTo && p.connectedTo === `consumed_by_${partnerId}`) {
                  return { ...p, connectedTo: undefined, bondType: 'single' as const };
                }
                return p;
              })
            };
          }
          return b;
        });
        return { blocks: updateCollapsedText(newBlocks, newConnections), connections: newConnections };
      }

      const newConnections = prev.connections.map((c) =>
        c === conn ? { ...c, bondType: finalBond as 'single'|'double'|'triple' } : c
      );

      const newBlocks = prev.blocks.map((b) => {
        if (b.instanceId === conn.fromInstance) {
          let consumed = 0;
          return {
            ...b,
            ports: b.ports.map((p) => {
              if (p.id === conn.fromPort) return { ...p, bondType: finalBond as 'single'|'double'|'triple' };
              if (!p.connectedTo && consumed < 1) {
                consumed++;
                return { ...p, connectedTo: `consumed_by_${conn.toInstance}` };
              }
              return p;
            }),
          };
        }
        if (b.instanceId === conn.toInstance) {
          let consumed = 0;
          return {
            ...b,
            ports: b.ports.map((p) => {
              if (p.id === conn.toPort) return { ...p, bondType: finalBond as 'single'|'double'|'triple' };
              if (!p.connectedTo && consumed < 1) {
                consumed++;
                return { ...p, connectedTo: `consumed_by_${conn.fromInstance}` };
              }
              return p;
            }),
          };
        }
        return b;
      });

      return { blocks: newBlocks, connections: newConnections };
    });
  }, []);

  // ── Clear all ───────────────────────────────────────────────────────────
  const clearAll = useCallback(() => {
    setState({ blocks: [], connections: [] });
  }, []);

  return {
    state,
    addBlock,
    addGroup,
    moveBlock,
    moveBlocks,
    setBlockRotation,
    removeBlock,
    removeBlocks,
    disconnectBlock,
    connectPorts,
    upgradeBond,
    uncollapseHydrogens,
    clearAll,
  };
}
