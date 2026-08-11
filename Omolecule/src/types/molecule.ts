// Types for the Organic Molecule Builder

export type BondType = 'single' | 'double' | 'triple' | 'none';
export type PortDir = 'left' | 'right' | 'up' | 'down';
export type DisplayMode = 'lewis' | 'structure';
export type BlockCategory = 'element' | 'group';

export interface Port {
  id: string;          // e.g. "left", "right", "up", "down"
  dir: PortDir;
  bondType: BondType;
  connectedTo?: string; // id of the port on the other block it connects to
}

export interface BlockTemplate {
  id: string;
  label: string;
  element: string;
  description: string;
  ports: Omit<Port, 'connectedTo'>[];
  smilesAtom: string;
  color: string;
  category: BlockCategory;
  displayMode: DisplayMode;
  lonePairs: PortDir[];      // lone-pair (non-bonding) electron pair directions
  paletteHidden?: boolean;   // internal-use templates not shown in palette
}

export interface PlacedBlock {
  instanceId: string;
  templateId: string;
  gridX: number; // Grid column (integer)
  gridY: number; // Grid row (integer)
  rotation: 0 | 90 | 180 | 270;
  ports: Port[];
  collapsedText?: string; // e.g. "CH3", "CH2", "CH"
  isHidden?: boolean; // For collapsed H blocks
}

export interface Connection {
  fromInstance: string;
  fromPort: string;
  toInstance: string;
  toPort: string;
  bondType: BondType;
  stretchOffset?: { dx: number, dy: number }; // For visual stretching on the grid
}

export interface MoleculeState {
  blocks: PlacedBlock[];
  connections: Connection[];
}

// ── Group template types ───────────────────────────────────────────────────

export interface GroupAtomDef {
  localId: string;    // e.g. "C", "O1", "O2"
  templateId: string; // reference to BlockTemplate.id
  relX: number;       // relative to drop point (px)
  relY: number;
}

export interface GroupBondDef {
  fromLocalId: string;
  fromPortId: string;
  toLocalId: string;
  toPortId: string;
}

export interface GroupTemplate {
  id: string;
  label: string;
  description: string;
  color: string;
  headId: string;          // localId of the exposed-port atom
  atoms: GroupAtomDef[];
  bonds: GroupBondDef[];
}
