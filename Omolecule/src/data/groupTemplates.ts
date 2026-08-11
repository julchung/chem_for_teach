import type { GroupTemplate } from '../types/molecule';

/**
 * Compound functional groups that spawn multiple pre-connected atoms.
 * Positions (relX, relY) are relative to the drop point (top-left of head block).
 * The "headId" atom is the one with the exposed connection port.
 */
export const GROUP_TEMPLATES: GroupTemplate[] = [
  // ── Ethyl (—CH₂CH₃) ─────────────────────────────────────────
  {
    id: 'grp_ethyl',
    label: '—C₂H₅',
    description: '乙基 (Ethyl)',
    color: '#888888',
    headId: 'CH2',
    atoms: [
      { localId: 'CH2', templateId: '_C_mid',  relX: 0,  relY: 0 },
      { localId: 'CH3', templateId: '_C_tail', relX: 1, relY: 0 },
    ],
    bonds: [
      { fromLocalId: 'CH2', fromPortId: 'right', toLocalId: 'CH3', toPortId: 'left' },
    ],
  },

  // ── Aldehyde (—CHO) ──────────────────────────────────────────
  {
    id: 'grp_aldehyde',
    label: '—CHO',
    description: '醛基 (Aldehyde)',
    color: '#FF8844',
    headId: 'C',
    atoms: [
      { localId: 'C', templateId: '_C_aldehyde', relX: 0,   relY: 0   },
      { localId: 'O', templateId: '_O_keto',      relX: 0,   relY: -1 },
    ],
    bonds: [
      { fromLocalId: 'C', fromPortId: 'up', toLocalId: 'O', toPortId: 'down' },
    ],
  },

  // ── Ketone bridge (—CO—) ─────────────────────────────────────
  {
    id: 'grp_ketone',
    label: '—CO—',
    description: '酮基 (Ketone carbonyl)',
    color: '#FF8844',
    headId: 'C',
    atoms: [
      { localId: 'C', templateId: '_C_carbonyl', relX: 0,   relY: 0   },
      { localId: 'O', templateId: '_O_keto',      relX: 0,   relY: -1 },
    ],
    bonds: [
      { fromLocalId: 'C', fromPortId: 'up', toLocalId: 'O', toPortId: 'down' },
    ],
  },

  // ── Carboxyl (—COOH) ─────────────────────────────────────────
  {
    id: 'grp_carboxyl',
    label: '—COOH',
    description: '羧基 (Carboxyl)',
    color: '#FF4444',
    headId: 'C',
    atoms: [
      { localId: 'C',  templateId: '_C_carbonyl', relX: 0,   relY: 0   },
      { localId: 'O1', templateId: '_O_keto',      relX: 0,   relY: -1 },
      { localId: 'O2', templateId: '_O_hydroxyl',  relX: 1,  relY: 0   },
    ],
    bonds: [
      { fromLocalId: 'C',  fromPortId: 'up',    toLocalId: 'O1', toPortId: 'down' },
      { fromLocalId: 'C',  fromPortId: 'right', toLocalId: 'O2', toPortId: 'left' },
    ],
  },

  // ── Amide (—CONH₂) ───────────────────────────────────────────
  {
    id: 'grp_amide',
    label: '—CONH₂',
    description: '醯胺基 (Amide)',
    color: '#4488FF',
    headId: 'C',
    atoms: [
      { localId: 'C', templateId: '_C_carbonyl', relX: 0,   relY: 0   },
      { localId: 'O', templateId: '_O_keto',      relX: 0,   relY: -1 },
      { localId: 'N', templateId: '_N_amide',     relX: 1,  relY: 0   },
    ],
    bonds: [
      { fromLocalId: 'C', fromPortId: 'up',    toLocalId: 'O', toPortId: 'down' },
      { fromLocalId: 'C', fromPortId: 'right', toLocalId: 'N', toPortId: 'left' },
    ],
  },

  // ── Ester carbonyl (—COO—) ───────────────────────────────────
  {
    id: 'grp_ester',
    label: '—COO—',
    description: '酯基 (Ester)',
    color: '#FF6699',
    headId: 'C',
    atoms: [
      { localId: 'C',  templateId: '_C_carbonyl', relX: 0,   relY: 0   },
      { localId: 'O1', templateId: '_O_keto',      relX: 0,   relY: -1 },
      { localId: 'O2', templateId: '_C_mid',       relX: 1,  relY: 0   },
    ],
    bonds: [
      { fromLocalId: 'C',  fromPortId: 'up',    toLocalId: 'O1', toPortId: 'down' },
      { fromLocalId: 'C',  fromPortId: 'right', toLocalId: 'O2', toPortId: 'left' },
    ],
  },
];

export const getGroupTemplate = (id: string): GroupTemplate | undefined =>
  GROUP_TEMPLATES.find((g) => g.id === id);

// IDs prefixed with 'grp_' that are COMPOUND (multi-atom)
export const COMPOUND_GROUP_IDS = new Set(GROUP_TEMPLATES.map((g) => g.id));
