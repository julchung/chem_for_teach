import { useState } from 'react';
import type { BlockTemplate } from '../types/molecule';
import type { GroupTemplate } from '../types/molecule';
import { LEWIS_TEMPLATES } from '../data/blockTemplates';
import { GROUP_TEMPLATES } from '../data/groupTemplates';
import { BlockSVG } from './BlockSVG';
import './Palette.css';

// ── palette card for a Lewis atom ─────────────────────────────────────────

function AtomCard({ template, onAdd }: {
  template: BlockTemplate;
  onAdd: (id: string, isGroup: boolean) => void;
}) {
  return (
    <div
      className="palette-card lewis-card"
      draggable
      onDragStart={(e) => {
        e.dataTransfer.effectAllowed = 'copy';
        e.dataTransfer.setData('application/omolecule', JSON.stringify({ id: template.id, type: 'block' }));
        e.dataTransfer.setData('text/plain', JSON.stringify({ id: template.id, type: 'block' }));
      }}
      onClick={() => onAdd(template.id, false)}
      title={`${template.description} — 點擊或拖曳加入`}
    >
      <div className="palette-card-svg">
        <BlockSVG template={template} size={80} rotation={0 as any} connectedPorts={[]} />
      </div>
      <div className="palette-card-label lewis-label">{template.element}</div>
      <div className="palette-card-desc">{template.description}</div>
    </div>
  );
}

// ── palette card for a compound group ────────────────────────────────────

function GroupCompoundCard({ group, onAdd }: {
  group: GroupTemplate;
  onAdd: (id: string, isGroup: boolean) => void;
}) {
  return (
    <div
      className="palette-card group-card compound-card"
      draggable
      onDragStart={(e) => {
        e.dataTransfer.effectAllowed = 'copy';
        e.dataTransfer.setData('application/omolecule', JSON.stringify({ id: group.id, type: 'group' }));
        e.dataTransfer.setData('text/plain', JSON.stringify({ id: group.id, type: 'group' }));
      }}
      onClick={() => onAdd(group.id, true)}
      title={`${group.description} — 點擊或拖曳加入`}
    >
      <div
        className="compound-icon"
        style={{ borderColor: group.color, color: group.color }}
      >
        {group.label}
      </div>
      <div className="palette-card-desc compound-desc">{group.description}</div>
    </div>
  );
}

// ── main palette ──────────────────────────────────────────────────────────

interface PaletteProps {
  onAdd: (id: string, isGroup: boolean) => void;
}

type Tab = 'atoms' | 'groups';

// ── palette card for a small atom pill (Row 1) ──────────────────────────
function AtomPillCard({ template, onAdd }: {
  template: BlockTemplate;
  onAdd: (id: string, isGroup: boolean) => void;
}) {
  return (
    <div
      className="palette-card group-card"
      style={{ padding: '4px' }}
      draggable
      onDragStart={(e) => {
        e.dataTransfer.effectAllowed = 'copy';
        e.dataTransfer.setData('application/omolecule', JSON.stringify({ id: template.id, type: 'block' }));
        e.dataTransfer.setData('text/plain', JSON.stringify({ id: template.id, type: 'block' }));
      }}
      onClick={() => onAdd(template.id, false)}
      title={`${template.description} — 點擊或拖曳加入`}
    >
      <div
        className="compound-icon"
        style={{ borderColor: template.color, color: template.color, minWidth: 'unset', width: '100%', padding: '4px 0' }}
      >
        {template.element}
      </div>
    </div>
  );
}

export function Palette({ onAdd }: PaletteProps) {
  const [tab, setTab] = useState<Tab>('atoms');

  const row1Atoms = ['H', 'F', 'Cl', 'Br', 'I'].map(el => LEWIS_TEMPLATES.find(t => t.element === el)!);
  const methylGroup = GROUP_TEMPLATES.find(g => g.id === 'grp_methyl') || GROUP_TEMPLATES[0]; // will add grp_methyl shortly
  const ethylGroup = GROUP_TEMPLATES.find(g => g.id === 'grp_ethyl');
  const phenylGroup = GROUP_TEMPLATES.find(g => g.id === 'grp_phenyl');
  const aminoGroup = GROUP_TEMPLATES.find(g => g.id === 'grp_amino');
  const hydroxylGroup = GROUP_TEMPLATES.find(g => g.id === 'grp_hydroxyl');
  const ketoneGroup = GROUP_TEMPLATES.find(g => g.id === 'grp_ketone');
  const carboxylGroup = GROUP_TEMPLATES.find(g => g.id === 'grp_carboxyl');
  const esterGroup = GROUP_TEMPLATES.find(g => g.id === 'grp_ester');
  const amideGroup = GROUP_TEMPLATES.find(g => g.id === 'grp_amide');

  return (
    <aside className="palette">
      {/* ── tab bar ── */}
      <div className="palette-tabs">
        <button
          className={`palette-tab ${tab === 'atoms' ? 'active' : ''}`}
          onClick={() => setTab('atoms')}
        >
          ⚛ 原子
        </button>
        <button
          className={`palette-tab ${tab === 'groups' ? 'active' : ''}`}
          onClick={() => setTab('groups')}
        >
          🧩 官能基
        </button>
      </div>

      {/* ── section: Lewis atoms ── */}
      {tab === 'atoms' && (
        <div className="palette-section">
          <div className="palette-section-header">路易士電子點結構</div>
          <div className="palette-section-hint">
            點擊原子加入作圖區，或拖曳至畫布指定位置
          </div>
          <div className="palette-grid">
            {LEWIS_TEMPLATES.map((tpl) => (
              <AtomCard key={tpl.id} template={tpl} onAdd={onAdd} />
            ))}
          </div>
        </div>
      )}

      {/* ── section: Functional groups ── */}
      {tab === 'groups' && (
        <div className="palette-section">
          <div className="palette-section-hint">點擊或拖曳加入</div>
          
          {/* Row 1: H, F, Cl, Br, I */}
          <div className="palette-grid" style={{ gridTemplateColumns: 'repeat(5, 1fr)', gap: '4px', marginBottom: '8px' }}>
            {row1Atoms.map(tpl => (
              <AtomPillCard key={tpl.id} template={tpl} onAdd={onAdd} />
            ))}
          </div>

          {/* Rows 2-10 (Groups) */}
          <div className="palette-grid" style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {methylGroup && <GroupCompoundCard key={methylGroup.id} group={methylGroup} onAdd={onAdd} />}
            {ethylGroup && <GroupCompoundCard key={ethylGroup.id} group={ethylGroup} onAdd={onAdd} />}
            {phenylGroup && <GroupCompoundCard key={phenylGroup.id} group={phenylGroup} onAdd={onAdd} />}
            {aminoGroup && <GroupCompoundCard key={aminoGroup.id} group={aminoGroup} onAdd={onAdd} />}
            {hydroxylGroup && <GroupCompoundCard key={hydroxylGroup.id} group={hydroxylGroup} onAdd={onAdd} />}
            {ketoneGroup && <GroupCompoundCard key={ketoneGroup.id} group={ketoneGroup} onAdd={onAdd} />}
            {carboxylGroup && <GroupCompoundCard key={carboxylGroup.id} group={carboxylGroup} onAdd={onAdd} />}
            {esterGroup && <GroupCompoundCard key={esterGroup.id} group={esterGroup} onAdd={onAdd} />}
            {amideGroup && <GroupCompoundCard key={amideGroup.id} group={amideGroup} onAdd={onAdd} />}
          </div>
        </div>
      )}

      {/* ── bottom hint ── */}
      <div className="palette-footer">
        雙擊積木可刪除<br />
        懸停右上角 × 也可刪除
      </div>
    </aside>
  );
}
