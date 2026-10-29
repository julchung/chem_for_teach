import os
import re

def update_diy_spec():
    base_dir = "多元課程/DIY_spec"

    # 1. Update style.css
    with open(f"{base_dir}/style.css", "r", encoding="utf-8") as f:
        style_content = f.read()

    css_addition = """
/* ====================================================
   全螢幕大分頁 (Full-Screen Tab Pages) & 專用導航系統
   ==================================================== */

.tab-page {
    display: none;
    opacity: 0;
    transition: opacity 0.25s ease-in-out;
}

.tab-page.active {
    display: block;
    opacity: 1;
    animation: fadeInTab 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes fadeInTab {
    from {
        opacity: 0;
        transform: translateY(8px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* 頂部導航下拉選單 */
.nav-dropdown {
    position: relative;
}

.nav-dropdown-btn {
    background: transparent;
    border: none;
    cursor: pointer;
    font-family: inherit;
    font-size: 0.95rem;
    color: var(--text-secondary);
    font-weight: 600;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    display: flex;
    align-items: center;
    gap: 0.35rem;
    transition: all 0.2s ease;
}

.nav-dropdown-btn:hover,
.nav-dropdown.active .nav-dropdown-btn {
    color: #60a5fa;
    background: rgba(59, 130, 246, 0.15);
}

.nav-dropdown-menu {
    display: none;
    position: absolute;
    top: calc(100% + 6px);
    left: 0;
    min-width: 210px;
    background: rgba(15, 23, 42, 0.96);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 14px;
    padding: 0.5rem;
    box-shadow: 0 16px 36px rgba(0, 0, 0, 0.6), 0 0 20px rgba(59, 130, 246, 0.2);
    z-index: 1000;
}

.nav-dropdown:hover .nav-dropdown-menu,
.nav-dropdown:focus-within .nav-dropdown-menu,
.nav-dropdown.open .nav-dropdown-menu {
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
}

.dropdown-item {
    padding: 0.65rem 0.95rem;
    border-radius: 8px;
    color: #cbd5e1;
    text-decoration: none;
    font-size: 0.88rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.6rem;
    transition: all 0.2s ease;
}

.dropdown-item:hover,
.dropdown-item.active {
    background: rgba(59, 130, 246, 0.22);
    color: #60a5fa;
}

.pill-dot {
    width: 9px;
    height: 9px;
    border-radius: 50%;
    flex-shrink: 0;
}

.pill-dot.dvd { background: #ec4899; box-shadow: 0 0 8px rgba(236, 72, 153, 0.6); }
.pill-dot.g1000 { background: #3b82f6; box-shadow: 0 0 8px rgba(59, 130, 246, 0.6); }
.pill-dot.cd { background: #10b981; box-shadow: 0 0 8px rgba(16, 185, 129, 0.6); }

/* 光柵膠囊切換列 (Grating Switcher Pill Bar) */
.grating-pill-bar {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
    margin: 1.5rem auto 0;
    flex-wrap: wrap;
    padding: 0.5rem 1rem;
    background: rgba(15, 23, 42, 0.6);
    border-radius: 9999px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    max-width: fit-content;
}

.pill-bar-label {
    font-size: 0.85rem;
    color: #94a3b8;
    font-weight: 600;
}

.grating-pill {
    padding: 0.45rem 1.15rem;
    border-radius: 9999px;
    font-size: 0.88rem;
    font-weight: 600;
    text-decoration: none;
    color: #cbd5e1;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.12);
    transition: all 0.2s ease;
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
}

.grating-pill:hover {
    background: rgba(255, 255, 255, 0.12);
    color: #fff;
    transform: translateY(-1px);
}

.grating-pill.active {
    background: rgba(59, 130, 246, 0.25);
    border-color: #60a5fa;
    color: #93c5fd;
    box-shadow: 0 0 14px rgba(59, 130, 246, 0.35);
}

/* 全螢幕大分頁儀表板兩欄佈局 */
.grating-dashboard-grid {
    display: grid;
    grid-template-columns: 1.22fr 0.98fr;
    gap: 2rem;
    margin-top: 1.5rem;
    margin-bottom: 2.5rem;
    align-items: start;
}

@media (max-width: 1080px) {
    .grating-dashboard-grid {
        grid-template-columns: 1fr;
    }
}

.grating-visual-col {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.grating-stage-card {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 20px;
    padding: 1.5rem;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.35);
}

.stage-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.2rem;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.stage-card-header h4 {
    font-size: 1.15rem;
    color: #f8fafc;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 700;
}

.stage-status-pill {
    font-size: 0.8rem;
    padding: 0.25rem 0.8rem;
    border-radius: 20px;
    font-weight: 700;
    background: rgba(245, 158, 11, 0.2);
    color: #fbbf24;
    border: 1px solid rgba(245, 158, 11, 0.4);
}

.large-svg-container {
    width: 100%;
    min-height: 400px;
    background: rgba(10, 15, 28, 0.75);
    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.06);
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    padding: 0.5rem;
}

.large-svg-container svg {
    width: 100%;
    height: auto;
    display: block;
}

.cmos-preview-box {
    margin-top: 1.25rem;
    background: rgba(10, 15, 28, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 1.2rem;
}

.cmos-header {
    display: flex;
    justify-content: space-between;
    font-size: 0.88rem;
    font-weight: 600;
    color: #cbd5e1;
    margin-bottom: 0.6rem;
}

.cmos-tag {
    font-size: 0.75rem;
    padding: 0.15rem 0.6rem;
    border-radius: 6px;
    background: rgba(168, 85, 247, 0.2);
    color: #c084fc;
    border: 1px solid rgba(168, 85, 247, 0.4);
}

.cmos-canvas {
    width: 100%;
    height: 56px;
    border-radius: 8px;
    display: block;
    background: #030712;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.cmos-scale {
    display: flex;
    justify-content: space-between;
    font-size: 0.75rem;
    color: #64748b;
    margin-top: 0.45rem;
    padding: 0 4px;
}

.grating-info-col {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.info-card {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 18px;
    padding: 1.5rem;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
}

.info-card h4 {
    font-size: 1.15rem;
    font-weight: 700;
    color: #93c5fd;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    padding-bottom: 0.6rem;
}

.info-card ul, .info-card ol {
    padding-left: 1.3rem;
    color: #cbd5e1;
    font-size: 0.92rem;
    line-height: 1.7;
}

.info-card li {
    margin-bottom: 0.6rem;
}

.info-card strong {
    color: #f8fafc;
}

.math-step {
    background: rgba(15, 23, 42, 0.65);
    border-radius: 10px;
    padding: 1.1rem;
    margin-bottom: 0.9rem;
    border-left: 3px solid #60a5fa;
    font-size: 0.92rem;
    color: #e2e8f0;
}

.math-step:last-child {
    margin-bottom: 0;
}

.math-step h5 {
    color: #93c5fd;
    font-size: 0.95rem;
    margin-bottom: 0.5rem;
    font-weight: 700;
}

.grating-page-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem 0 3rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    flex-wrap: wrap;
    gap: 1rem;
    margin-top: 2rem;
}

.btn-outline {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.15);
    color: #cbd5e1;
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.65rem 1.25rem;
    border-radius: 10px;
    text-decoration: none;
    font-weight: 600;
    transition: all 0.2s ease;
}

.btn-outline:hover {
    background: rgba(255, 255, 255, 0.12);
    color: #fff;
    border-color: rgba(255, 255, 255, 0.3);
}

.hero-badge-row {
    display: flex;
    justify-content: center;
    gap: 0.6rem;
    margin-bottom: 1rem;
    flex-wrap: wrap;
}

.hero-badge {
    font-size: 0.8rem;
    padding: 0.25rem 0.8rem;
    border-radius: 20px;
    font-weight: 700;
}

.badge-reflect {
    background: rgba(168, 85, 247, 0.2);
    color: #c084fc;
    border: 1px solid rgba(168, 85, 247, 0.4);
}

.badge-trans {
    background: rgba(236, 72, 153, 0.2);
    color: #f472b6;
    border: 1px solid rgba(236, 72, 153, 0.4);
}

.badge-grating {
    background: rgba(59, 130, 246, 0.2);
    color: #93c5fd;
    border: 1px solid rgba(59, 130, 246, 0.4);
}

.hero-title-grating {
    font-size: 2.5rem;
    font-weight: 900;
    margin-bottom: 0.8rem;
    background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 50%, #93c5fd 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
"""
    if "全螢幕大分頁" not in style_content:
        with open(f"{base_dir}/style.css", "a", encoding="utf-8") as f:
            f.write("\n" + css_addition)
        print("Updated style.css with full-screen tab styles.")
    else:
        print("style.css already has full-screen tab styles.")

update_diy_spec()

