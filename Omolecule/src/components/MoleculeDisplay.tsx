import { useEffect, useRef, useState } from 'react';
import type { MoleculeInfo } from '../utils/pubchemApi';
import './MoleculeDisplay.css';

interface MoleculeDisplayProps {
  smiles: string;
  isComplete: boolean;
  moleculeInfo: MoleculeInfo | null;
  isLoading: boolean;
  blockCount: number;
}

declare global {
  interface Window {
    $3Dmol: any;
  }
}

export function MoleculeDisplay({
  smiles,
  isComplete,
  moleculeInfo,
  isLoading,
  blockCount,
}: MoleculeDisplayProps) {
  const viewerRef      = useRef<HTMLDivElement>(null);
  const viewerInstance = useRef<any>(null);
  const [viewerReady, setViewerReady] = useState(false);

  // ── 3Dmol.js ─────────────────────────────────────────────────────────────
  useEffect(() => {
    if (window.$3Dmol) { setViewerReady(true); return; }
    const script = document.createElement('script');
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/3Dmol/2.4.2/3Dmol-min.js';
    script.async = true;
    script.onload = () => setViewerReady(true);
    document.head.appendChild(script);
  }, []);

  useEffect(() => {
    if (!viewerReady || !viewerRef.current || viewerInstance.current) return;
    try {
      viewerInstance.current = window.$3Dmol.createViewer(viewerRef.current, {
        backgroundColor: 'transparent',
        antialias: true,
      });
    } catch (e) { console.error('3Dmol init error', e); }
  }, [viewerReady]);

  useEffect(() => {
    const viewer = viewerInstance.current;
    if (!viewer) return;
    viewer.clear();
    
    if (moleculeInfo?.sdf) {
      try {
        viewer.addModel(moleculeInfo.sdf, 'sdf');
        viewer.setStyle({}, { stick: { radius: 0.15, colorscheme: 'Jmol' }, sphere: { scale: 0.3, colorscheme: 'Jmol' } });
        viewer.zoomTo(); 
        viewer.spin('y', 0.5); 
        viewer.render();
      } catch (e) { console.error('3Dmol render error', e); }
    } else {
      viewer.render(); // empty
    }
  }, [moleculeInfo, blockCount]);

  // Construct PubChem 2D Image URL
  // We use the SMILES to fetch the image directly, ensuring standard IUPAC (left-to-right, explicit atoms)
  const pubchemImageUrl = smiles 
    ? `https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/${encodeURIComponent(smiles)}/PNG?record_type=2d&image_size=large`
    : '';

  // ── Render ────────────────────────────────────────────────────────────────
  return (
    <div className="molecule-display">
      {/* Header: molecule name */}
      <div className={`name-banner ${moleculeInfo ? 'has-name' : ''}`}>
        {isLoading && (
          <div className="name-loading"><span className="spinner" /><span>辨識分子中…</span></div>
        )}
        {!isLoading && moleculeInfo && (
          <>
            <div className="molecule-name-iupac">{moleculeInfo.iupacName}</div>
            <div className="molecule-name-zh">{moleculeInfo.chineseName}</div>
          </>
        )}
        {!isLoading && !moleculeInfo && blockCount > 0 && !isComplete && (
          <div className="name-hint">連接所有接點後顯示學名</div>
        )}
        {!isLoading && !moleculeInfo && blockCount === 0 && (
          <div className="name-hint">拖曳積木開始建構分子</div>
        )}
      </div>

      {/* SMILES readout */}
      {smiles && (
        <div className="smiles-bar">
          <span className="smiles-label">SMILES：</span>
          <span className="smiles-value">{smiles}</span>
          {isComplete && <span className="complete-badge">✓ 完整</span>}
        </div>
      )}

      {/* 2D structural formula — rendered via PubChem Image API */}
      {smiles && (
        <div className="viewer-2d">
          <div className="viewer-2d-title">2D 結構式</div>
          <div className="viewer-2d-content">
            <img 
              src={pubchemImageUrl} 
              alt="2D Structure" 
              className="pubchem-2d-image"
              onError={(e) => {
                // If PubChem can't generate the image for a partial smiles, hide it temporarily
                (e.target as HTMLImageElement).style.display = 'none';
              }}
              onLoad={(e) => {
                (e.target as HTMLImageElement).style.display = 'block';
              }}
            />
          </div>
        </div>
      )}

      {/* 3D Viewer */}
      <div className="viewer-wrap">
        <div ref={viewerRef} className="viewer-3d" />
        
        {/* Placeholder for empty canvas */}
        {blockCount === 0 && (
          <div className="viewer-overlay">
            <div className="viewer-placeholder">
              <div className="atom-icon">⚛</div>
              <p>3D 分子結構將在此顯示</p>
            </div>
          </div>
        )}
        
        {/* Placeholder while building but not matched yet */}
        {blockCount > 0 && !moleculeInfo?.sdf && (
          <div className="viewer-overlay">
            <div className="viewer-placeholder">
              <span className="spinner" style={{marginBottom: '10px', display: 'inline-block'}}/>
              <p>請將積木組合完整</p>
              <p style={{fontSize: '0.8em', opacity: 0.7}}>等待生成 3D 結構...</p>
            </div>
          </div>
        )}

        {!viewerReady && (
          <div className="viewer-overlay">
            <span className="spinner" /> 載入 3D 引擎…
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="display-footer">
        <div className="footer-stat">積木數：<b>{blockCount}</b></div>
        {moleculeInfo?.cid && (
          <a className="footer-link"
             href={`https://pubchem.ncbi.nlm.nih.gov/compound/${moleculeInfo.cid}`}
             target="_blank" rel="noreferrer">
            PubChem ↗
          </a>
        )}
      </div>
    </div>
  );
}
