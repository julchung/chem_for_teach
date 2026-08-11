import { useState } from 'react';
import type { BlockTemplate } from '../types/molecule';
import type { GroupTemplate } from '../types/molecule';
import { LEWIS_TEMPLATES, GROUP_SINGLE_TEMPLATES } from '../data/blockTemplates';
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

// ── palette card for a single-atom group block ───────────────────────────

function GroupSingleCard({ template, onAdd }: {
  template: BlockTemplate;
  onAdd: (id: string, isGroup: boolean) => void;
}) {
  return (
    <div
      className="palette-card group-card"
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
      <div className="palette-card-label">{template.label}</div>
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

export function Palette({ onAdd }: PaletteProps) {
  const [tab, setTab] = useState<Tab>('atoms');

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
          <div className="palette-section-header">單原子官能基</div>
          <div className="palette-section-hint">點擊或拖曳加入</div>
          <div className="palette-grid">
            {GROUP_SINGLE_TEMPLATES.map((tpl) => (
              <GroupSingleCard key={tpl.id} template={tpl} onAdd={onAdd} />
            ))}
          </div>

          <div className="palette-section-header" style={{ marginTop: '12px' }}>
            複合官能基 (預連)
          </div>
          <div className="palette-section-hint">點擊或拖曳即可加入</div>
          <div className="palette-grid">
            {GROUP_TEMPLATES.map((grp) => (
              <GroupCompoundCard key={grp.id} group={grp} onAdd={onAdd} />
            ))}
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
