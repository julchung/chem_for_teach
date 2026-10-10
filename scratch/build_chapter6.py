#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_chapter6.py
自動化以公版規格一次完成第六章（01~05小節）的編修：
1. 備份原 index.html -> index_old.html
2. 拆解各內容 slide -> slidepage1.html ~ slidepageN.html
3. 生成現代化連連看通關檢核頁面 -> quiz.html
4. 生成符合公版規範的主框架頁面 -> index.html
註：06_秒錶反應 依照指示不作變動，並在 05_影響速率因素_催化劑 通關時直接解鎖 06 與下一章 (ch7_s1)。
"""

import os
import re
import shutil

BASE_DIR = '/Users/julchung/Library/CloudStorage/OneDrive-國立新化高級工業職業學校/玩具檔案/my_化學網/my_chem_006_反應速率'

CHAPTERS_CONFIG = [
    {
        'dir': '01_反應速率定律式',
        'unit': '6-1',
        'section_id': 'ch6_s1',
        'title': '化學反應速率與定律式',
        'full_title': '化學反應速率與定律式 · 互動教學',
        'badge': '選修化學二 · 化學反應速率',
        'topic_desc': '【化學反應速率定義、速率定律式與反應級數】請將左側核心概念連線至右側對應科學定義或數學關係，5 組配對全部正確即可通關解鎖下一單元。',
        'next_info': '🔓 6-2 碰撞學說與活化能 — 已解鎖',
        'is_special_unlock': False,
        'pool': [
            {'left': '反應速率定律式', 'right': 'R = k[A]ᵐ[B]ⁿ'},
            {'left': '零級反應濃度時間關係', 'right': '[A]t = [A]0 - kt'},
            {'left': '一級反應半生期', 'right': 't_1/2 = 0.693 / k'},
            {'left': '二級反應圖形關係', 'right': '1/[A] 對 t 成直線'},
            {'left': '零級反應速率常數單位', 'right': 'M·s⁻¹'},
            {'left': '一級反應圖形關係', 'right': 'log[A] 或 ln[A] 對 t 成直線'},
            {'left': '二級反應半生期', 'right': '與初濃度成反比 (1/k[A]0)'},
            {'left': '零級反應圖形關係', 'right': '[A] 對 t 成直線'},
            {'left': '反應速率常數 k 改變因素', 'right': '受反應物本性、溫度、催化劑影響'},
            {'left': '一級反應速率常數單位', 'right': 's⁻¹'},
            {'left': '二級反應濃度時間關係', 'right': '1/[A]t = 1/[A]0 + kt'},
            {'left': '反應速率基本單位', 'right': 'M / s 或 M·s⁻¹'},
            {'left': '一級反應半生期特性', 'right': '為定值，與初濃度無關'},
            {'left': '零級反應半生期', 'right': '與初濃度成正比 ([A]0/2k)'}
        ]
    },
    {
        'dir': '02_碰撞學說',
        'unit': '6-2',
        'section_id': 'ch6_s2',
        'title': '碰撞學說與活化能',
        'full_title': '碰撞學說與活化能 · 互動教學',
        'badge': '選修化學二 · 化學反應速率',
        'topic_desc': '【碰撞學說、有效碰撞條件與活化能位能圖】請將左側概念連線至右側對應科學成因與物理量描述，5 組配對全部正確即可通關解鎖下一單元。',
        'next_info': '🔓 6-3 影響反應速率的因素 — 已解鎖',
        'is_special_unlock': False,
        'pool': [
            {'left': '碰撞學說有效條件', 'right': '正確方位 + 能量超越低限能'},
            {'left': '低限能 (Threshold Energy)', 'right': '造成有效碰撞的最低動能'},
            {'left': '活化能 (Ea)', 'right': '反應物轉變為活化錯合物所需位能'},
            {'left': '活化錯合物', 'right': '有效碰撞時之暫時性產物，位能最高'},
            {'left': '反應熱 ΔH', 'right': 'Ea(正) - Ea(逆)，與活化能大小無關'},
            {'left': '放熱反應 (ΔH < 0)', 'right': '正反應活化能 < 逆反應活化能'},
            {'left': '吸熱反應 (ΔH > 0)', 'right': '正反應活化能 > 逆反應活化能'},
            {'left': '活化能的功用', 'right': '破壞原有化學鍵，克服相斥力'},
            {'left': '速率決定步驟 (瓶頸反應)', 'right': '多步驟反應中，反應速率最慢的步驟'},
            {'left': '活化能受何者影響', 'right': '反應物本性及催化劑'},
            {'left': '常溫氫氧混合不反應原因', 'right': '反應活化能太高'},
            {'left': '大多數化學反應', 'right': '經由連續性多步驟碰撞所完成'},
            {'left': '每次碰撞機率', 'right': '以兩個粒子相互碰撞機會最大'}
        ]
    },
    {
        'dir': '03_影響反應速率的因素',
        'unit': '6-3',
        'section_id': 'ch6_s3',
        'title': '影響反應速率的因素',
        'full_title': '影響反應速率的因素 · 互動教學',
        'badge': '選修化學二 · 化學反應速率',
        'topic_desc': '【影響反應速率之五大變因（本性、濃度、接觸面、溫度、催化劑）】請將左側概念連線至右側對應影響規律與現象，5 組配對全部正確即可通關解鎖下一單元。',
        'next_info': '🔓 6-4 溫度與阿瑞尼斯方程式 — 已解鎖',
        'is_special_unlock': False,
        'pool': [
            {'left': '速率常數 k', 'right': '與溫度及催化劑有關'},
            {'left': '反應級數 m、n', 'right': '由實驗測定決定，非計量係數'},
            {'left': '溫度上升 (T↑)', 'right': 'k 值增大，反應速率加快'},
            {'left': '催化劑的效果', 'right': '降低活化能 Ea，改變反應途徑'},
            {'left': '濃度增加（0級除外）', 'right': '單位體積粒子數增多，碰撞頻率增加'},
            {'left': 'Arrhenius 方程式', 'right': 'k = A·e^(-Ea/RT)'},
            {'left': '活化能 Ea 下降', 'right': '超過能障分子比例激增，速率加快'},
            {'left': '壓力對氣體反應', 'right': '等效於氣體濃度增加'},
            {'left': '正逆反應速率等量提升', 'right': '催化劑的特性'},
            {'left': '0 級反應速率特徵', 'right': 'R = k（與反應物濃度無關）'},
            {'left': '哈柏法鐵催化劑', 'right': '降低 Ea 加速合成氨反應'},
            {'left': '溫度每升高 10°C', 'right': '反應速率約增大為 2~3 倍'},
            {'left': '不影響 k 值的因素', 'right': '反應物濃度、容器體積、壓力'},
            {'left': '接觸面積增大（粉末化）', 'right': '異相反應中大幅提升碰撞頻率'},
            {'left': '離子水溶液沉澱反應', 'right': '不需斷鍵，反應速率極快'}
        ]
    },
    {
        'dir': '04_影響速率因素-溫度',
        'unit': '6-4',
        'section_id': 'ch6_s4',
        'title': '溫度與阿瑞尼斯方程式',
        'full_title': '溫度與阿瑞尼斯方程式 · 互動教學',
        'badge': '選修化學二 · 化學反應速率',
        'topic_desc': '【溫度效應、波茲曼動能分佈與阿瑞尼斯方程式】請將左側概念連線至右側對應科學機制與數學意涵，5 組配對全部正確即可通關解鎖下一單元。',
        'next_info': '🔓 6-5 催化劑與反應途徑改變 — 已解鎖',
        'is_special_unlock': False,
        'pool': [
            {'left': '溫度升高', 'right': '正逆反應速率皆加快'},
            {'left': '溫度對活化能影響', 'right': '無影響 (不改變活化能 Ea)'},
            {'left': '升溫加速之主要效應', 'right': '超越低限能的高動能分子數呈指數激增'},
            {'left': '低限能 Ea', 'right': '引發有效碰撞的動能門檻'},
            {'left': '反應熱 ΔH', 'right': '決定吸放熱，但不決定反應速率快慢'},
            {'left': '活化能高 (Ea 大) 的反應', 'right': '對溫度變化較敏感 (升溫增幅大)'},
            {'left': '活化能低 (Ea 小) 的反應', 'right': '常溫下速率相對較快'},
            {'left': '放熱反應升溫', 'right': '逆反應速率增加幅度大於正反應'},
            {'left': '室溫附近每升 10°C', 'right': '反應速率約增為原本的 2~3 倍'},
            {'left': '波茲曼能量分佈向右平移', 'right': '粒子平均動能增加且分佈變寬'},
            {'left': '吸熱反應升溫', 'right': '正反應速率增加幅度大於逆反應'},
            {'left': '阿瑞尼士方程式', 'right': 'lnk = -Ea/(RT) + lnA'},
            {'left': '升溫之次要效應', 'right': '粒子碰撞總次數微幅增加 (約增2%)'},
            {'left': '溫度與速率常數 k', 'right': '升溫顯著放大 k 值'},
            {'left': '整體平衡移動趨勢', 'right': '升溫時朝吸熱反應方向移動'}
        ]
    },
    {
        'dir': '05_影響速率因素-催化劑',
        'unit': '6-5',
        'section_id': 'ch6_s5',
        'title': '催化劑與反應途徑改變',
        'full_title': '催化劑與反應途徑改變 · 互動教學',
        'badge': '選修化學二 · 化學反應速率',
        'topic_desc': '【催化劑加速機制、反應途徑活化能改變與催化劑分類】請將左側概念連線至右側對應性質或實例，全部答對後將直接解鎖「6-6 秒錶反應」與「第 7 章化學平衡」！',
        'next_info': '🔓 6-6 秒錶反應 — 已解鎖 ＆ 🔓 7-1 化學平衡與平衡常數 — 已解鎖',
        'is_special_unlock': True,
        'pool': [
            {'left': '勻相催化', 'right': '催化劑與反應物處於同相（均為液相或氣相）'},
            {'left': '非均相催化', 'right': '催化劑通常為固體粉末以增大表面積'},
            {'left': '正催化劑', 'right': '降低活化能，提供新路徑加速反應'},
            {'left': '負催化劑 (抑制劑)', 'right': '提高活化能或中斷鏈反應，減緩速率'},
            {'left': '助催化劑', 'right': '自身無催化活性，但能顯著提升催化劑效能'},
            {'left': '催化劑毒劑', 'right': '佔據活性位置使催化劑失去活性'},
            {'left': '生物酶 (Enzyme)', 'right': '高專一性、高催化效率之生物體蛋白質催化劑'},
            {'left': '反應熱 ΔH 與平衡常數 K', 'right': '加入催化劑前後皆完全保持不變'},
            {'left': '可逆反應加入催化劑', 'right': '正逆反應速率等倍率提升，產率不變'},
            {'left': '阿瑞尼士方程式解釋', 'right': 'Ea 降低使速率常數 k 呈指數級增大'},
            {'left': '哈柏法製氨催化劑', 'right': '以固體鐵粉為非均相催化劑'},
            {'left': '汽車觸媒轉換器', 'right': '使用 Pt、Pd、Rh 催化氧化 CO 與碳氫化合物'}
        ]
    }
]

def extract_slides(container_inner):
    """精確提取 container 內所有頂層 slide div 及其後緊隨的專屬 script"""
    slides = []
    pattern = re.compile(r'<div\s+class=\"slide\b', re.IGNORECASE)
    div_open = re.compile(r'<div\b', re.IGNORECASE)
    div_close = re.compile(r'</div\s*>', re.IGNORECASE)
    
    pos = 0
    while True:
        m = pattern.search(container_inner, pos)
        if not m:
            break
        start = m.start()
        depth = 0
        cur = start
        end = -1
        while cur < len(container_inner):
            o = div_open.search(container_inner, cur)
            c = div_close.search(container_inner, cur)
            if o is None and c is None:
                break
            if o is None:
                next_is_open = False
                cur = c.end()
            elif c is None:
                next_is_open = True
                cur = o.end()
            elif o.start() < c.start():
                next_is_open = True
                cur = o.end()
            else:
                next_is_open = False
                cur = c.end()
            
            if next_is_open:
                depth += 1
            else:
                depth -= 1
                if depth == 0:
                    end = cur
                    break
        if end != -1:
            slide_html = container_inner[start:end]
            after = container_inner[end:]
            next_slide = pattern.search(after)
            lim = next_slide.start() if next_slide else len(after)
            segment = after[:lim]
            scripts = re.findall(r'<script\b[^>]*>.*?</script>', segment, re.DOTALL | re.IGNORECASE)
            extra_js = '\n'.join(scripts)
            if extra_js:
                slide_html += '\n' + extra_js
            slides.append(slide_html)
            pos = end
        else:
            pos = start + 1
    return slides


def generate_quiz_html(cfg):
    """產生標準公版連連看 quiz.html"""
    pool_json = str(cfg['pool']).replace("'", '"')
    
    special_badges = ''
    if cfg['is_special_unlock']:
        special_badges = f"""
                <div class="banner-badge-item" style="background:rgba(52,211,153,0.15); border:1px solid rgba(52,211,153,0.4); color:#34d399;">
                    ✅ {cfg['unit']} {cfg['title']} — 通關
                </div>
                <div class="banner-badge-item" style="background:rgba(56,189,248,0.15); border:1px solid rgba(56,189,248,0.4); color:#38bdf8;">
                    🔓 6-6 秒錶反應 — 已解鎖
                </div>
                <div class="banner-badge-item" style="background:rgba(167,139,250,0.15); border:1px solid rgba(167,139,250,0.4); color:#a78bfa;">
                    🔓 7-1 化學平衡與平衡常數 — 已解鎖
                </div>
        """
        banner_msg = f"恭喜你 5 組配對全數答對！已完成 {cfg['title']} 核心檢核 🎉<br><span style='color:#38bdf8;font-weight:700;'>已直接解鎖 6-6 秒錶反應 與 第 7 章化學平衡！</span>"
    else:
        special_badges = f"""
                <div class="banner-badge-item" style="background:rgba(52,211,153,0.15); border:1px solid rgba(52,211,153,0.4); color:#34d399;">
                    ✅ {cfg['unit']} {cfg['title']} — 通關
                </div>
                <div class="banner-badge-item" style="background:rgba(56,189,248,0.15); border:1px solid rgba(56,189,248,0.4); color:#38bdf8;">
                    {cfg['next_info']}
                </div>
        """
        banner_msg = f"恭喜你 5 組配對全數答對！已完成 {cfg['title']} 核心檢核 🎉"

    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>{cfg['unit']} {cfg['title']} · 核心通關檢核</title>
    <meta name="description" content="選修化學二：{cfg['title']}核心觀念連連看通關檢核與章節解鎖">
    <style>
        :root {{
            --bg-dark: #0f172a;
            --text-main: #f8fafc;
            --text-sub: #94a3b8;
            --accent-blue: #38bdf8;
            --accent-green: #34d399;
            --accent-red: #f87171;
            --accent-yellow: #fbbf24;
            --accent-purple: #a78bfa;
            --accent-cyan: #22d3ee;
            --glass: rgba(255, 255, 255, 0.04);
            --glass-border: rgba(255, 255, 255, 0.12);
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}

        html, body {{
            width: 100%;
            min-height: 100vh;
            background: var(--bg-dark);
            color: var(--text-main);
            font-family: 'Segoe UI', 'Microsoft JhengHei', 'PingFang TC', sans-serif;
            overflow-x: hidden;
            overflow-y: auto;
            scroll-behavior: smooth;
            background-image: radial-gradient(rgba(56,189,248,0.08) 1.2px, transparent 1.2px);
            background-size: 30px 30px;
        }}

        #app {{
            position: relative;
            width: 100%;
            min-height: 100vh;
            padding: 1.5rem 1rem 3rem;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}

        .quiz-container-full {{
            width: 100%;
            max-width: 980px;
            display: flex;
            flex-direction: column;
            gap: 14px;
        }}

        .text-cyan {{ color: var(--accent-cyan); }}

        /* ── 標頭情境框 (公版標準格式) ── */
        .quiz-scenario-box {{
            background: rgba(30, 41, 59, 0.7);
            border: 1.5px solid rgba(255, 255, 255, 0.12);
            border-radius: 16px;
            padding: 1.2rem 1.6rem;
            backdrop-filter: blur(12px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.35);
        }}

        .problem-badge {{
            font-size: 0.85rem;
            padding: 0.25rem 0.9rem;
            border-radius: 30px;
            font-weight: 700;
            border: 1px solid;
            letter-spacing: 0.05em;
            display: inline-block;
        }}

        /* ── 測驗卡片外框 (quiz-card) ── */
        .quiz-card {{
            background: rgba(30, 41, 59, 0.6);
            border: 1.5px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 1.2rem 1.5rem;
            backdrop-filter: blur(12px);
            box-shadow: 0 8px 28px rgba(0,0,0,0.35);
        }}

        .quiz-q {{
            font-size: 1.05rem;
            font-weight: 700;
            color: #f8fafc;
            line-height: 1.5;
        }}

        /* ── 連連看互動區 CSS ── */
        .match-game-wrapper {{
            position: relative;
            width: 100%;
            margin-top: 10px;
            background: rgba(15, 23, 42, 0.5);
            border-radius: 12px;
            padding: 14px 18px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            overflow: hidden;
            touch-action: none;
        }}

        .match-game-cols {{
            display: flex;
            justify-content: space-between;
            position: relative;
            gap: 28px;
            z-index: 2;
        }}

        .match-col {{
            display: flex;
            flex-direction: column;
            gap: 10px;
            width: 44%;
        }}

        .match-item {{
            background: rgba(30, 41, 59, 0.7);
            border: 1.5px solid rgba(255, 255, 255, 0.12);
            border-radius: 10px;
            padding: 9px 14px;
            display: flex;
            align-items: center;
            position: relative;
            cursor: pointer;
            transition: all 0.2s ease;
            user-select: none;
            touch-action: none;
            font-size: 0.92rem;
            color: #f1f5f9;
            min-height: 48px;
        }}

        .match-item:hover {{
            border-color: #38bdf8;
            background: rgba(56, 189, 248, 0.12);
        }}

        .match-item.selected {{
            border-color: #38bdf8;
            background: rgba(56, 189, 248, 0.22);
            box-shadow: 0 0 12px rgba(56, 189, 248, 0.35);
        }}

        .match-item.connected {{
            border-color: rgba(56, 189, 248, 0.65);
            background: rgba(56, 189, 248, 0.12);
        }}

        .match-item.match-correct {{
            border-color: #34d399 !important;
            background: rgba(52, 211, 153, 0.18) !important;
            color: #6ee7b7 !important;
            box-shadow: 0 0 12px rgba(52, 211, 153, 0.3) !important;
        }}

        .match-item.match-wrong {{
            border-color: #f87171 !important;
            background: rgba(248, 113, 113, 0.18) !important;
            color: #fca5a5 !important;
            box-shadow: 0 0 12px rgba(248, 113, 113, 0.3) !important;
        }}

        .match-item-text {{
            flex: 1;
            pointer-events: none;
            line-height: 1.4;
        }}

        .match-item-badge {{
            font-size: 0.95rem;
            font-weight: 800;
            margin: 0 4px;
            pointer-events: none;
        }}

        .match-dot {{
            width: 16px;
            height: 16px;
            background: #38bdf8;
            border: 2px solid white;
            border-radius: 50%;
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            transition: all 0.2s;
            z-index: 5;
            box-shadow: 0 0 6px rgba(56, 189, 248, 0.6);
            pointer-events: none;
        }}

        .match-item[data-side="left"] .match-dot {{
            right: -8px;
        }}

        .match-item[data-side="right"] .match-dot {{
            left: -8px;
        }}

        .match-dot.active {{
            transform: translateY(-50%) scale(1.3);
            background: #fbbf24;
            box-shadow: 0 0 12px #fbbf24;
        }}

        .match-svg {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
        }}

        /* ── 操作反饋列與提交按鈕 (quiz-action-bar) ── */
        .quiz-action-bar {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 12px;
            margin-top: 4px;
        }}

        .quiz-feedback-msg {{
            flex: 1;
            min-width: 260px;
            font-size: 0.92rem;
            line-height: 1.5;
            color: #94a3b8;
            padding: 8px 14px;
            border-radius: 10px;
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.08);
            transition: all 0.25s ease;
        }}

        .quiz-feedback-msg.success {{
            background: rgba(52, 211, 153, 0.12);
            color: #34d399;
            border: 1px solid rgba(52, 211, 153, 0.35);
        }}

        .quiz-feedback-msg.fail {{
            background: rgba(248, 113, 113, 0.12);
            color: #f87171;
            border: 1px solid rgba(248, 113, 113, 0.35);
        }}

        .btn-submit-exam {{
            flex-shrink: 0;
            padding: 10px 24px;
            background: linear-gradient(135deg, #38bdf8, #34d399);
            color: #0b1120;
            font-size: 0.97rem;
            font-weight: 700;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            transition: opacity 0.2s, transform 0.1s;
            white-space: nowrap;
            box-shadow: 0 4px 14px rgba(56, 189, 248, 0.35);
        }}

        .btn-submit-exam:hover {{ opacity: 0.92; transform: translateY(-1px); }}
        .btn-submit-exam:disabled {{ opacity: 0.55; cursor: default; transform: none; box-shadow: none; }}

        .btn-retry-exam {{
            flex-shrink: 0;
            padding: 10px 22px;
            background: linear-gradient(135deg, #f59e0b, #ef4444);
            color: white;
            font-size: 0.97rem;
            font-weight: 700;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            transition: opacity 0.2s, transform 0.1s;
            white-space: nowrap;
            display: none;
            align-items: center;
            gap: 6px;
            box-shadow: 0 4px 14px rgba(239, 68, 68, 0.35);
        }}

        .btn-retry-exam:hover {{ opacity: 0.92; transform: translateY(-1px); }}

        /* ── 通關完成橫幅 ── */
        #section-complete-banner {{
            display: none;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            min-height: 40vh;
            padding: 3rem 2rem;
            background: radial-gradient(ellipse at center, rgba(52,211,153,0.18) 0%, rgba(11,17,32,0.85) 70%);
            border-top: 1px solid rgba(52,211,153,0.25);
            margin-top: 1.5rem;
            border-radius: 20px;
            box-shadow: 0 16px 40px rgba(0,0,0,0.5);
            animation: fadeInBanner 0.6s ease forwards;
        }}

        @keyframes fadeInBanner {{
            from {{ opacity: 0; transform: translateY(15px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        @keyframes pulse-trophy {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.15); }}
        }}

        .banner-badge-item {{
            padding: 12px 22px;
            border-radius: 12px;
            font-weight: 700;
            font-size: 0.95rem;
        }}

        @media (max-width: 768px) {{
            .match-game-cols {{ gap: 14px; }}
            .match-col {{ width: 48%; }}
            .match-item {{ font-size: 0.82rem; padding: 7px 10px; min-height: 44px; }}
        }}
    </style>
</head>
<body>

<div id="app">
    <div class="quiz-container-full">
        <!-- 標頭情境框 -->
        <div class="quiz-scenario-box">
            <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:6px; flex-wrap:wrap; gap:8px;">
                <span class="problem-badge" style="background:rgba(52,211,153,0.2); border-color:rgba(52,211,153,0.4); color:#34d399;">
                    🏆 單元 {cfg['unit']} · 核心通關檢核
                </span>
                <span style="font-size:0.86rem; color:#38bdf8;">📌 請完成概念連連看配對，點擊右下角「確定作答」提交檢核</span>
            </div>
            <p style="font-size:0.94rem; line-height:1.6; color:#f8fafc; margin:0;">
                {cfg['topic_desc']}
            </p>
        </div>

        <!-- ★ 第(1)題：概念連連看（互動連線，橫跨全欄） -->
        <div class="quiz-card" id="quiz-matching-card" style="width:100%;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
                <div class="quiz-q" style="margin:0;">
                    <span class="text-cyan">(1) 概念配對連連看</span> 請將左側概念連線至右側對應科學描述（可拖曳或點選圓點任意連線）。
                </div>
                <div style="display:flex; gap:8px;">
                    <button type="button" id="btn-shuffle-match" style="background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.2); color:#38bdf8; font-size:0.8rem; padding:4px 12px; border-radius:8px; cursor:pointer; transition:all 0.2s;">
                        隨機抽題 🔀
                    </button>
                    <button type="button" id="btn-reset-match" style="background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.2); color:#94a3b8; font-size:0.8rem; padding:4px 12px; border-radius:8px; cursor:pointer; transition:all 0.2s;">
                        重設連線 ↺
                    </button>
                </div>
            </div>

            <!-- 連連看畫布與題目兩欄 -->
            <div class="match-game-wrapper" id="match-game-wrapper">
                <svg id="match-svg" class="match-svg"></svg>
                <div class="match-game-cols">
                    <div class="match-col" id="match-col-left"></div>
                    <div class="match-col" id="match-col-right"></div>
                </div>
            </div>

            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:6px;">
                <p style="font-size:0.8rem; color:#64748b; margin:0;">💡 操作說明：點擊左側再點擊右側，或直接按住拖曳連線。提交前可任意重連。</p>
                <span id="match-count-badge" style="font-size:0.82rem; color:#38bdf8; font-weight:600;">已連線：0 / 5</span>
            </div>
        </div>

        <!-- 底部操作列 (包含反饋訊息、再試一次按鈕、確定作答按鈕) -->
        <div class="quiz-action-bar">
            <div class="quiz-feedback-msg" id="quiz-feedback-msg">
                <span>💡 請完成 5 組概念配對連線，完成後點擊「確定作答」。</span>
            </div>
            <div style="display:flex; gap:10px; align-items:center;">
                <button type="button" id="btn-retry-exam" class="btn-retry-exam">
                    🔄 再試一次
                </button>
                <button type="button" id="btn-submit-exam" class="btn-submit-exam">
                    確定作答 🚀
                </button>
            </div>
        </div>

        <!-- 通關成功橫幅 -->
        <div id="section-complete-banner">
            <div style="font-size:4rem; margin-bottom:0.8rem; animation: pulse-trophy 1.5s ease-in-out infinite;">🏆</div>
            <h2 style="color:#34d399; font-size:clamp(1.8rem,3.2vw,2.4rem); font-weight:800; margin-bottom:0.5rem;">單元檢核通過！</h2>
            <p style="color:#6ee7b7; font-size:1.1rem; margin-bottom:0.3rem;">{banner_msg}</p>
            <p style="color:#94a3b8; font-size:0.95rem;">相關單元已自動解鎖，請從左側目錄切換繼續學習</p>
            <div style="margin-top:1.5rem; display:flex; gap:1rem; flex-wrap:wrap; justify-content:center;">
                {special_badges}
            </div>
        </div>
    </div>
</div>

<script>
// ── {cfg['unit']} {cfg['title']} 核心檢核系統 ──
(function initSectionCheckpoint() {{
    const FULL_QUESTION_POOL = {pool_json};

    let MATCH_DATA = [];
    const GAME_COUNT = 5;

    // 狀態變數
    let isPassed = false;
    let isVerified = false;
    let connections = [];
    let selectedItem = null;
    let isDraggingMatch = false;
    let dragStartItem = null;
    let tempMatchLine = null;

    // DOM 元素
    const leftCol = document.getElementById('match-col-left');
    const rightCol = document.getElementById('match-col-right');
    const matchSvg = document.getElementById('match-svg');
    const matchWrapper = document.getElementById('match-game-wrapper');
    const matchCountBadge = document.getElementById('match-count-badge');
    const submitBtn = document.getElementById('btn-submit-exam');
    const retryBtn = document.getElementById('btn-retry-exam');
    const feedbackMsg = document.getElementById('quiz-feedback-msg');
    const completeBanner = document.getElementById('section-complete-banner');
    const resetMatchBtn = document.getElementById('btn-reset-match');
    const shuffleMatchBtn = document.getElementById('btn-shuffle-match');

    function renderMatchGame() {{
        connections = [];
        selectedItem = null;
        isDraggingMatch = false;
        isVerified = false;
        if (tempMatchLine) {{ tempMatchLine.remove(); tempMatchLine = null; }}
        matchSvg.innerHTML = '';
        if (retryBtn) retryBtn.style.display = 'none';
        if (submitBtn) submitBtn.disabled = false;
        feedbackMsg.className = 'quiz-feedback-msg';
        feedbackMsg.innerHTML = '<span>💡 請完成 5 組概念配對連線，完成後點擊「確定作答」。</span>';

        // 隨機抽 5 題
        const shuffledPool = [...FULL_QUESTION_POOL].sort(() => Math.random() - 0.5);
        MATCH_DATA = shuffledPool.slice(0, GAME_COUNT).map((item, idx) => ({{
            id: idx,
            left: item.left,
            right: item.right
        }}));

        // 渲染左欄
        leftCol.innerHTML = '';
        MATCH_DATA.forEach(d => {{
            const div = document.createElement('div');
            div.className = 'match-item';
            div.dataset.id = d.id;
            div.dataset.side = 'left';
            div.innerHTML = `
                <span class="match-item-text">${{d.left}}</span>
                <span class="match-item-badge"></span>
                <div class="match-dot"></div>
            `;
            bindItemEvents(div);
            leftCol.appendChild(div);
        }});

        // 渲染右欄（隨機重洗右欄順序）
        rightCol.innerHTML = '';
        const shuffledRight = [...MATCH_DATA].sort(() => Math.random() - 0.5);
        shuffledRight.forEach(d => {{
            const div = document.createElement('div');
            div.className = 'match-item';
            div.dataset.id = d.id;
            div.dataset.side = 'right';
            div.innerHTML = `
                <div class="match-dot"></div>
                <span class="match-item-text">${{d.right}}</span>
                <span class="match-item-badge"></span>
            `;
            bindItemEvents(div);
            rightCol.appendChild(div);
        }});

        updateMatchBadge();
        reportIframeHeight();
    }}

    function bindItemEvents(el) {{
        // 點選模式
        el.addEventListener('click', (e) => {{
            if (isPassed || isVerified) return;
            handleItemClick(el);
        }});

        // 拖曳模式
        el.addEventListener('mousedown', (e) => {{
            if (isPassed || isVerified) return;
            startDrag(el, e.clientX, e.clientY);
        }});

        el.addEventListener('touchstart', (e) => {{
            if (isPassed || isVerified) return;
            const touch = e.touches[0];
            startDrag(el, touch.clientX, touch.clientY);
        }}, {{ passive: true }});
    }}

    function startDrag(el, clientX, clientY) {{
        isDraggingMatch = true;
        dragStartItem = el;
        el.querySelector('.match-dot')?.classList.add('active');

        const wrapRect = matchWrapper.getBoundingClientRect();
        const dotRect = el.querySelector('.match-dot').getBoundingClientRect();
        const startX = dotRect.left + dotRect.width / 2 - wrapRect.left;
        const startY = dotRect.top + dotRect.height / 2 - wrapRect.top;

        if (!tempMatchLine) {{
            tempMatchLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            tempMatchLine.setAttribute('stroke', '#38bdf8');
            tempMatchLine.setAttribute('stroke-width', '3');
            tempMatchLine.setAttribute('stroke-dasharray', '5,5');
            matchSvg.appendChild(tempMatchLine);
        }}
        tempMatchLine.setAttribute('x1', startX);
        tempMatchLine.setAttribute('y1', startY);
        tempMatchLine.setAttribute('x2', clientX - wrapRect.left);
        tempMatchLine.setAttribute('y2', clientY - wrapRect.top);
    }}

    window.addEventListener('mousemove', (e) => {{
        if (!isDraggingMatch || !tempMatchLine) return;
        const wrapRect = matchWrapper.getBoundingClientRect();
        tempMatchLine.setAttribute('x2', e.clientX - wrapRect.left);
        tempMatchLine.setAttribute('y2', e.clientY - wrapRect.top);
    }});

    window.addEventListener('touchmove', (e) => {{
        if (!isDraggingMatch || !tempMatchLine) return;
        const touch = e.touches[0];
        const wrapRect = matchWrapper.getBoundingClientRect();
        tempMatchLine.setAttribute('x2', touch.clientX - wrapRect.left);
        tempMatchLine.setAttribute('y2', touch.clientY - wrapRect.top);
    }}, {{ passive: true }});

    function endDrag(clientX, clientY) {{
        if (!isDraggingMatch) return;
        isDraggingMatch = false;
        if (dragStartItem) {{
            dragStartItem.querySelector('.match-dot')?.classList.remove('active');
        }}
        if (tempMatchLine) {{
            tempMatchLine.remove();
            tempMatchLine = null;
        }}

        const target = document.elementFromPoint(clientX, clientY);
        const targetItem = target?.closest('.match-item');
        if (targetItem && dragStartItem && targetItem !== dragStartItem) {{
            const startSide = dragStartItem.dataset.side;
            const targetSide = targetItem.dataset.side;
            if (startSide !== targetSide) {{
                const leftEl = startSide === 'left' ? dragStartItem : targetItem;
                const rightEl = startSide === 'right' ? dragStartItem : targetItem;
                connectPair(parseInt(leftEl.dataset.id, 10), parseInt(rightEl.dataset.id, 10));
            }}
        }}
        dragStartItem = null;
    }}

    window.addEventListener('mouseup', (e) => endDrag(e.clientX, e.clientY));
    window.addEventListener('touchend', (e) => {{
        const touch = e.changedTouches ? e.changedTouches[0] : null;
        if (touch) endDrag(touch.clientX, touch.clientY);
    }});

    function handleItemClick(el) {{
        const side = el.dataset.side;
        if (!selectedItem) {{
            selectedItem = el;
            el.classList.add('selected');
            el.querySelector('.match-dot')?.classList.add('active');
            return;
        }}

        if (selectedItem === el) {{
            selectedItem.classList.remove('selected');
            selectedItem.querySelector('.match-dot')?.classList.remove('active');
            selectedItem = null;
            return;
        }}

        if (selectedItem.dataset.side === side) {{
            selectedItem.classList.remove('selected');
            selectedItem.querySelector('.match-dot')?.classList.remove('active');
            selectedItem = el;
            el.classList.add('selected');
            el.querySelector('.match-dot')?.classList.add('active');
            return;
        }}

        const leftEl = side === 'left' ? el : selectedItem;
        const rightEl = side === 'right' ? el : selectedItem;
        connectPair(parseInt(leftEl.dataset.id, 10), parseInt(rightEl.dataset.id, 10));

        selectedItem.classList.remove('selected');
        selectedItem.querySelector('.match-dot')?.classList.remove('active');
        selectedItem = null;
    }}

    function connectPair(leftId, rightId) {{
        connections = connections.filter(c => c.leftId !== leftId && c.rightId !== rightId);
        connections.push({{ leftId, rightId, status: null }});

        matchWrapper.querySelectorAll('.match-item').forEach(el => {{
            const id = parseInt(el.dataset.id, 10);
            const side = el.dataset.side;
            const isConn = connections.some(c => (side === 'left' ? c.leftId === id : c.rightId === id));
            el.classList.toggle('connected', isConn);
        }});

        updateMatchBadge();
        drawAllConnections();
    }}

    function updateMatchBadge() {{
        matchCountBadge.textContent = `已連線：${{connections.length}} / ${{MATCH_DATA.length}}`;
        if (connections.length === MATCH_DATA.length) {{
            matchCountBadge.style.color = '#34d399';
        }} else {{
            matchCountBadge.style.color = '#38bdf8';
        }}
    }}

    function drawAllConnections() {{
        matchSvg.querySelectorAll('.perm-line').forEach(l => l.remove());
        const wrapRect = matchWrapper.getBoundingClientRect();

        connections.forEach(c => {{
            const leftEl = leftCol.querySelector(`.match-item[data-id="${{c.leftId}}"]`);
            const rightEl = rightCol.querySelector(`.match-item[data-id="${{c.rightId}}"]`);
            if (!leftEl || !rightEl) return;

            const lDot = leftEl.querySelector('.match-dot').getBoundingClientRect();
            const rDot = rightEl.querySelector('.match-dot').getBoundingClientRect();

            const x1 = lDot.left + lDot.width / 2 - wrapRect.left;
            const y1 = lDot.top + lDot.height / 2 - wrapRect.top;
            const x2 = rDot.left + rDot.width / 2 - wrapRect.left;
            const y2 = rDot.top + rDot.height / 2 - wrapRect.top;

            let strokeColor = '#38bdf8';
            if (c.status === 'correct') strokeColor = '#34d399';
            else if (c.status === 'wrong') strokeColor = '#f87171';

            const line = document.createElementNS('http://www.w3.org/2000/svg', 'path');
            const dx = (x2 - x1) * 0.45;
            const d = `M ${{x1}} ${{y1}} C ${{x1 + dx}} ${{y1}}, ${{x2 - dx}} ${{y2}}, ${{x2}} ${{y2}}`;
            line.setAttribute('d', d);
            line.setAttribute('fill', 'none');
            line.setAttribute('stroke', strokeColor);
            line.setAttribute('stroke-width', '3');
            line.setAttribute('class', 'perm-line');
            matchSvg.appendChild(line);
        }});
    }}

    window.addEventListener('resize', () => {{
        drawAllConnections();
        reportIframeHeight();
    }});
    window.addEventListener('scroll', drawAllConnections, {{ passive: true }});

    if (resetMatchBtn) {{
        resetMatchBtn.addEventListener('click', () => {{
            if (isPassed) return;
            isVerified = false;
            connections = [];
            selectedItem = null;
            const allItems = matchWrapper.querySelectorAll('.match-item');
            allItems.forEach(el => {{
                el.classList.remove('selected', 'connected', 'match-correct', 'match-wrong');
                el.querySelector('.match-item-badge').textContent = '';
            }});
            updateMatchBadge();
            drawAllConnections();
            if (retryBtn) retryBtn.style.display = 'none';
            if (submitBtn) submitBtn.disabled = false;
            feedbackMsg.className = 'quiz-feedback-msg';
            feedbackMsg.innerHTML = '<span>💡 已清空連線，請重新進行概念配對。</span>';
        }});
    }}

    if (shuffleMatchBtn) {{
        shuffleMatchBtn.addEventListener('click', () => {{
            if (isPassed) return;
            renderMatchGame();
        }});
    }}

    // 「確定作答」檢核按鈕 (核心通關判定)
    if (submitBtn) {{
        submitBtn.addEventListener('click', () => {{
            if (isPassed) return;

            if (connections.length < MATCH_DATA.length) {{
                feedbackMsg.className = 'quiz-feedback-msg fail';
                feedbackMsg.innerHTML = `<span>⚠️ 概念連連看尚有未配對項目（已完成 ${{connections.length}}/${{MATCH_DATA.length}} 組），請將 5 組概念全部連線！</span>`;
                return;
            }}

            isVerified = true;
            let allCorrect = true;

            connections.forEach(c => {{
                const isCorrect = (c.leftId === c.rightId);
                c.status = isCorrect ? 'correct' : 'wrong';
                if (!isCorrect) allCorrect = false;

                const leftEl = leftCol.querySelector(`.match-item[data-id="${{c.leftId}}"]`);
                const rightEl = rightCol.querySelector(`.match-item[data-id="${{c.rightId}}"]`);

                if (leftEl) {{
                    leftEl.classList.remove('match-correct', 'match-wrong');
                    leftEl.classList.add(isCorrect ? 'match-correct' : 'match-wrong');
                    leftEl.querySelector('.match-item-badge').textContent = isCorrect ? '✓' : '✗';
                    leftEl.querySelector('.match-item-badge').style.color = isCorrect ? '#34d399' : '#f87171';
                }}
                if (rightEl) {{
                    rightEl.classList.remove('match-correct', 'match-wrong');
                    rightEl.classList.add(isCorrect ? 'match-correct' : 'match-wrong');
                    rightEl.querySelector('.match-item-badge').textContent = isCorrect ? '✓' : '✗';
                    rightEl.querySelector('.match-item-badge').style.color = isCorrect ? '#34d399' : '#f87171';
                }}
            }});

            drawAllConnections();

            if (allCorrect) {{
                isPassed = true;
                submitBtn.disabled = true;
                submitBtn.textContent = '檢核通過 ✅';
                if (retryBtn) retryBtn.style.display = 'none';

                feedbackMsg.className = 'quiz-feedback-msg success';
                feedbackMsg.innerHTML = '<span>🎉 檢核通過！5 組概念配對全數答對，單元已成功解鎖通關！</span>';

                if (completeBanner) {{
                    completeBanner.style.display = 'flex';
                    reportIframeHeight();
                    setTimeout(() => {{
                        completeBanner.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                    }}, 250);
                }}

                notifySectionComplete();
            }} else {{
                feedbackMsg.className = 'quiz-feedback-msg fail';
                feedbackMsg.innerHTML = '<span>❌ 檢核未通過：已標示正確（綠色）與錯誤（紅色）部分，請點擊「再試一次」進行修正！</span>';

                submitBtn.disabled = true;
                if (retryBtn) {{
                    retryBtn.style.display = 'inline-flex';
                    retryBtn.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
                }}
            }}
        }});
    }}

    // 「再試一次」按鈕：保留答對連線，清除答錯連線供重試
    if (retryBtn) {{
        retryBtn.addEventListener('click', () => {{
            if (isPassed) return;
            isVerified = false;

            connections = connections.filter(c => {{
                if (c.status === 'correct') {{
                    return true;
                }} else {{
                    const leftEl = leftCol.querySelector(`.match-item[data-id="${{c.leftId}}"]`);
                    const rightEl = rightCol.querySelector(`.match-item[data-id="${{c.rightId}}"]`);
                    if (leftEl) {{
                        leftEl.classList.remove('match-wrong', 'connected');
                        leftEl.querySelector('.match-item-badge').textContent = '';
                    }}
                    if (rightEl) {{
                        rightEl.classList.remove('match-wrong', 'connected');
                        rightEl.querySelector('.match-item-badge').textContent = '';
                    }}
                    return false;
                }}
            }});

            updateMatchBadge();
            drawAllConnections();

            retryBtn.style.display = 'none';
            submitBtn.disabled = false;
            feedbackMsg.className = 'quiz-feedback-msg';
            feedbackMsg.innerHTML = '<span>✏️ 請重新連線錯誤的概念，完成後再次點擊「確定作答」。</span>';
        }});
    }}

    // 通關通知外層母網頁 SPA (portal.js)
    function notifySectionComplete() {{
        const payload = {{
            type: 'SECTION_COMPLETE',
            sectionId: '{cfg['section_id']}',
            title: '{cfg['title']}'
        }};

        if (window.parent && window.parent !== window) {{
            window.parent.postMessage(payload, '*');
        }}
        if (window.top && window.top !== window && window.top !== window.parent) {{
            window.top.postMessage(payload, '*');
        }}
    }}

    // 回報本頁高度給父層以自適應調整 iframe 高度
    function reportIframeHeight() {{
        setTimeout(() => {{
            const h = document.documentElement.scrollHeight || document.body.scrollHeight;
            if (window.parent && window.parent !== window) {{
                window.parent.postMessage({{ type: 'RESIZE_IFRAME', height: h }}, '*');
            }}
        }}, 200);
    }}

    renderMatchGame();
}})();
</script>

</body>
</html>
"""
    return html


def generate_index_html(cfg, slide_count):
    """產生標準公版 index.html 主控制器框架"""
    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{cfg['full_title']}</title>

    <style>
        :root {{
            --header-height: 58px;
            --slide-height:  calc(100vh - var(--header-height));
            --toolbar-space: 70px;
            --header-bg:     #1e293b;
            --accent:        #38bdf8;
            --accent2:       #a78bfa;
            --primary-bg:    #0f172a;
            --card-border:   rgba(56,189,248,0.22);
        }}

        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

        html, body {{
            width: 100%; height: 100%;
            background: var(--primary-bg);
            font-family: 'Segoe UI', 'Microsoft JhengHei', 'PingFang TC', sans-serif;
            overflow-x: hidden;
            overflow-y: auto;
            scroll-behavior: smooth;
            scroll-padding-top: var(--header-height);
        }}

        /* ── 頂端固定標頭 ── */
        #chapter-header {{
            position: fixed;
            top: 0; left: 0; width: 100%;
            height: var(--header-height);
            background: var(--header-bg);
            border-bottom: 1px solid var(--card-border);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 28px;
            z-index: 9999;
            backdrop-filter: blur(12px);
            box-shadow: 0 2px 20px rgba(0,0,0,0.5);
        }}

        .header-left {{ display: flex; align-items: center; gap: 14px; }}

        .header-badge {{
            font-size: 0.72rem;
            color: var(--accent2);
            background: rgba(167,139,250,0.12);
            border: 1px solid rgba(167,139,250,0.35);
            padding: 2px 10px;
            border-radius: 40px;
            letter-spacing: 0.06em;
        }}

        .header-title {{
            font-size: 1.15rem;
            font-weight: 800;
            color: var(--accent);
            letter-spacing: 0.04em;
        }}

        .header-right {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        /* 頁碼指示器 */
        #page-counter {{
            font-size: 0.82rem;
            color: rgba(255,255,255,0.5);
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.12);
            padding: 3px 12px;
            border-radius: 30px;
            font-weight: 700;
        }}

        /* 捷徑按鈕區 */
        #jump-bar {{
            display: flex;
            align-items: center;
            gap: 4px;
            flex-wrap: wrap;
        }}

        .jump-btn {{
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.12);
            color: rgba(255,255,255,0.6);
            font-size: 0.7rem;
            font-weight: 700;
            padding: 2px 7px;
            border-radius: 6px;
            cursor: pointer;
            transition: 0.2s;
        }}
        .jump-btn:hover {{ background: var(--accent); color: #0f172a; border-color: var(--accent); }}
        .jump-btn.active-pg {{ background: var(--accent); color: #0f172a; border-color: var(--accent); }}

        /* ── 主捲動容器 ── */
        #main-scroller {{
            margin-top: var(--header-height);
            display: flex;
            flex-direction: column;
            gap: 0;
            background: var(--primary-bg);
        }}

        /* ── 每個 iframe 外框：中央舞台定位，右側預留 70px 避開浮動工具列 ── */
        .slide-frame-wrap {{
            width: 100%;
            height: var(--slide-height);
            min-height: 540px;
            box-sizing: border-box;
            padding: 10px var(--toolbar-space) 12px 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            border-bottom: 2px solid var(--card-border);
            scroll-margin-top: var(--header-height);
            overflow: hidden;
        }}

        /* ── 中央舞台卡片（iframe） ── */
        .slide-frame-wrap iframe {{
            width: 100%;
            max-width: 1440px;
            height: 100%;
            border-radius: 16px;
            border: 1px solid var(--card-border);
            box-shadow: 0 10px 35px rgba(0, 0, 0, 0.45);
            display: block;
            background: var(--primary-bg);
            transition: box-shadow 0.3s ease;
        }}

        .slide-frame-wrap iframe:hover {{
            box-shadow: 0 14px 45px rgba(0, 0, 0, 0.6);
        }}

        /* ── quiz 外框稍作區別：高度依題型與連連看互動彈性延伸 ── */
        .quiz-frame-wrap {{
            height: auto !important;
            min-height: var(--slide-height);
            padding-bottom: 35px;
            border-top: 3px solid var(--accent2);
            overflow: visible;
        }}

        .quiz-frame-wrap iframe {{
            height: var(--slide-height);
            max-width: 1100px;
        }}

        /* ── 載入佔位符 ── */
        .loading-placeholder {{
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100%;
            color: rgba(255,255,255,0.35);
            font-size: 0.95rem;
            gap: 10px;
        }}
        .loading-placeholder::before {{
            content: '';
            width: 18px; height: 18px;
            border: 2px solid var(--accent);
            border-top-color: transparent;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }}
        @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
    </style>
</head>
<body>

    <!-- ── 頂端固定標頭 ── -->
    <header id="chapter-header">
        <div class="header-left">
            <span class="header-badge">{cfg['badge']}</span>
            <span class="header-title">{cfg['full_title']}</span>
        </div>
        <div class="header-right">
            <div id="jump-bar"></div>
            <div id="page-counter">— / —</div>
        </div>
    </header>

    <!-- ── 主體：iframe 堆疊容器 ── -->
    <main id="main-scroller"></main>

    <script>
    (() => {{
        const scroller      = document.getElementById('main-scroller');
        const pageCounter   = document.getElementById('page-counter');
        const jumpBar       = document.getElementById('jump-bar');

        const SLIDES = [];
        let currentVisible = 0;
        const wrappers = [];

        // ── 自動偵測當前目錄下的 slidepage 數量並串接 quiz.html ──
        async function detectSlides() {{
            const detected = [];
            let idx = 1;
            const MAX_DETECT = 80;
            let probeBlocked = false;

            while (idx <= MAX_DETECT) {{
                const filename = `slidepage${{idx}}.html`;
                let exists = false;
                try {{
                    let res = await fetch(filename, {{ method: 'HEAD' }});
                    if (res.status === 405) {{
                        res = await fetch(filename, {{ method: 'GET' }});
                    }}
                    exists = res.ok;
                }} catch (e) {{
                    exists = false;
                    if (idx === 1) probeBlocked = true;
                }}

                if (exists) {{
                    detected.push({{ file: filename, label: String(idx) }});
                    idx++;
                }} else {{
                    break;
                }}
            }}

            // 本地 fallback
            if (probeBlocked || detected.length === 0) {{
                console.warn('[AutoDetect] 本地 fetch 受限，啟用預設備援頁數（{slide_count}頁）');
                for (let k = 1; k <= {slide_count}; k++) {{
                    detected.push({{ file: `slidepage${{k}}.html`, label: String(k) }});
                }}
            }}

            // 探測 quiz.html 是否存在
            let hasQuiz = false;
            try {{
                let qRes = await fetch('quiz.html', {{ method: 'HEAD' }});
                if (qRes.status === 405) qRes = await fetch('quiz.html', {{ method: 'GET' }});
                hasQuiz = qRes.ok;
            }} catch (e) {{
                hasQuiz = true;
            }}

            if (hasQuiz) {{
                detected.push({{
                    file: 'quiz.html',
                    label: `${{detected.length + 1}} 📝`,
                    isQuiz: true
                }});
            }}

            return detected;
        }}

        // ── 建立頁碼捷徑按鈕 ─────────────────────────────────
        function buildJumpBar() {{
            jumpBar.innerHTML = '';
            SLIDES.forEach((slide, idx) => {{
                const btn = document.createElement('button');
                btn.className = 'jump-btn';
                btn.textContent = slide.label;
                btn.title = slide.file;
                btn.dataset.jumpIdx = idx;
                btn.addEventListener('click', () => scrollToSlide(idx));
                jumpBar.appendChild(btn);
            }});
        }}

        function updateActiveBtn(idx) {{
            jumpBar.querySelectorAll('.jump-btn').forEach((b, i) => {{
                b.classList.toggle('active-pg', i === idx);
            }});
            pageCounter.textContent = `${{idx + 1}} / ${{SLIDES.length}}`;
        }}

        function scrollToSlide(idx) {{
            const wrap = wrappers[idx];
            if (wrap) {{
                wrap.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                let startTime = Date.now();
                function animScrollSync() {{
                    if (window.__chemReportScroll) window.__chemReportScroll();
                    if (Date.now() - startTime < 800) {{
                        requestAnimationFrame(animScrollSync);
                    }}
                }}
                requestAnimationFrame(animScrollSync);
            }}
        }}

        // ── 建立 iframe ───────────────────────────────────────
        function createIframe(slide, idx) {{
            const wrap = document.createElement('div');
            wrap.className = 'slide-frame-wrap' + (slide.isQuiz ? ' quiz-frame-wrap' : '');
            wrap.id = `slide-wrap-${{idx}}`;
            wrap.dataset.idx = idx;

            const placeholder = document.createElement('div');
            placeholder.className = 'loading-placeholder';
            placeholder.textContent = slide.isQuiz ? '載入通關測驗…' : `載入第 ${{slide.label}} 頁…`;
            wrap.appendChild(placeholder);

            const iframe = document.createElement('iframe');
            iframe.title = `第 ${{slide.label}} 頁`;
            iframe.allow = 'fullscreen';
            iframe.setAttribute('loading', 'lazy');

            iframe.addEventListener('load', () => {{
                if (placeholder.parentNode) placeholder.remove();
                if (slide.isQuiz) {{
                    try {{
                        const iDoc = iframe.contentDocument || iframe.contentWindow.document;
                        setTimeout(() => {{
                            const h = iDoc.documentElement.scrollHeight || iDoc.body.scrollHeight;
                            if (h && h > 200) {{
                                iframe.style.height = (h + 40) + 'px';
                                wrap.style.height = (h + 40) + 'px';
                            }}
                        }}, 500);
                    }} catch(e) {{}}
                }}
            }});

            iframe.addEventListener('error', () => {{
                if (placeholder.parentNode) placeholder.remove();
                const errDiv = document.createElement('div');
                errDiv.style.cssText = 'height:100%;display:flex;align-items:center;justify-content:center;color:#f87171;font-size:1rem;';
                errDiv.textContent = `⚠️ 無法載入 ${{slide.file}}`;
                wrap.appendChild(errDiv);
            }});

            iframe.src = slide.file;
            wrap.appendChild(iframe);
            wrappers.push(wrap);
            return wrap;
        }}

        // ── Intersection Observer：偵測當前頁面 ─────────────
        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    const idx = parseInt(entry.target.dataset.idx, 10);
                    if (!isNaN(idx)) {{
                        currentVisible = idx;
                        updateActiveBtn(idx);
                    }}
                }}
            }});
        }}, {{
            root: null,
            threshold: 0.2,
            rootMargin: '-58px 0px 0px 0px'
        }});

        // ── 訊息監聽與轉發 ────
        window.addEventListener('message', (e) => {{
            if (!e.data) return;

            // 通關解鎖訊號轉發至外層 SPA (portal.js)
            if (e.data.type === 'SECTION_COMPLETE') {{
                if (window.parent && window.parent !== window) {{
                    window.parent.postMessage(e.data, '*');
                }}
            }}

            // 自適應調整 quiz iframe 高度
            if (e.data.type === 'RESIZE_IFRAME' && e.data.height) {{
                const quizIframe = document.querySelector('.quiz-frame-wrap iframe');
                const quizWrap = document.querySelector('.quiz-frame-wrap');
                if (quizIframe) {{
                    const newH = Math.max(e.data.height + 40, window.innerHeight - 58);
                    quizIframe.style.height = newH + 'px';
                    if (quizWrap) quizWrap.style.height = newH + 'px';
                }}
            }}
        }});

        // ── 初始化：自動偵測並建立所有 iframe ───────────────
        async function init() {{
            pageCounter.textContent = '探測中…';

            const detectedSlides = await detectSlides();
            SLIDES.length = 0;
            SLIDES.push(...detectedSlides);

            pageCounter.textContent = `1 / ${{SLIDES.length}}`;
            buildJumpBar();

            SLIDES.forEach((slide, idx) => {{
                const wrap = createIframe(slide, idx);
                scroller.appendChild(wrap);
                observer.observe(wrap);
            }});

            updateActiveBtn(0);
        }}

        if (document.readyState === 'loading') {{
            document.addEventListener('DOMContentLoaded', init);
        }} else {{
            init();
        }}

        // ── 鍵盤換頁 ──────────────────────────
        let keyLock = false;
        document.addEventListener('keydown', (e) => {{
            if (e.key !== 'ArrowDown' && e.key !== 'ArrowUp' &&
                e.key !== 'PageDown'  && e.key !== 'PageUp') return;
            e.preventDefault();
            if (keyLock) return;
            keyLock = true;
            setTimeout(() => {{ keyLock = false; }}, 300);

            if ((e.key === 'ArrowDown' || e.key === 'PageDown') && currentVisible < SLIDES.length - 1) {{
                scrollToSlide(currentVisible + 1);
            }} else if ((e.key === 'ArrowUp' || e.key === 'PageUp') && currentVisible > 0) {{
                scrollToSlide(currentVisible - 1);
            }}
        }});

    }})();
    </script>

    <!-- ── 捲動位置中繼器 (對齊其他章節) ── -->
    <script src="../../unified_chem_spa/js/scroll_relay.js"></script>

    <!-- ── Chem Whiteboard Scroll Sync Bridge (即時雙向連動白板座標) ── -->
    <script id="__chem_scroll_bridge">
    (function() {{
      if (window.__chemScrollBridgeInstalled) return;
      window.__chemScrollBridgeInstalled = true;

      function getScrollPos() {{
        var sy = window.scrollY || window.pageYOffset || 0;
        var sx = window.scrollX || window.pageXOffset || 0;
        if (document.documentElement) {{
          sy = Math.max(sy, document.documentElement.scrollTop || 0);
          sx = Math.max(sx, document.documentElement.scrollLeft || 0);
        }}
        if (document.body) {{
          sy = Math.max(sy, document.body.scrollTop || 0);
          sx = Math.max(sx, document.body.scrollLeft || 0);
        }}
        return {{ sx: sx, sy: sy }};
      }}

      function reportScroll() {{
        if (window.parent && window.parent !== window) {{
          var pos = getScrollPos();
          window.parent.postMessage({{ type: '__chem_scroll', sy: pos.sy, sx: pos.sx }}, '*');
        }}
      }}

      window.__chemReportScroll = reportScroll;

      window.addEventListener('scroll', reportScroll, {{ capture: true, passive: true }});
      document.addEventListener('scroll', reportScroll, {{ capture: true, passive: true }});
      window.addEventListener('wheel', function() {{
        requestAnimationFrame(reportScroll);
        setTimeout(reportScroll, 40);
        setTimeout(reportScroll, 120);
      }}, {{ capture: true, passive: true }});
      window.addEventListener('touchmove', function() {{
        requestAnimationFrame(reportScroll);
        setTimeout(reportScroll, 40);
        setTimeout(reportScroll, 120);
      }}, {{ capture: true, passive: true }});
      window.addEventListener('keydown', function(e) {{
        if (['ArrowUp', 'ArrowDown', 'PageUp', 'PageDown', 'Space', 'Home', 'End'].indexOf(e.code) !== -1) {{
          requestAnimationFrame(reportScroll);
          setTimeout(reportScroll, 60);
          setTimeout(reportScroll, 180);
        }}
      }}, {{ passive: true }});

      window.addEventListener('message', function(e) {{
        if (!e.data) return;
        if (e.data.type === '__chem_scroll_by') {{
          var dy = e.data.deltaY || 0;
          var dx = e.data.deltaX || 0;
          window.scrollBy({{ top: dy, left: dx, behavior: 'instant' }});
          if (document.documentElement) document.documentElement.scrollTop += dy;
          if (document.body) document.body.scrollTop += dy;
          reportScroll();
        }} else if (e.data.type === '__chem_get_scroll') {{
          reportScroll();
        }}
      }});

      if (document.readyState === 'loading') {{
        document.addEventListener('DOMContentLoaded', reportScroll);
      }} else {{
        reportScroll();
      }}
      setTimeout(reportScroll, 200);
      setTimeout(reportScroll, 800);
    }})();
    </script>
</body>
</html>
"""
    return html


def process_section(cfg):
    """處理單一小節的完整分割與生成流程"""
    sec_dir = os.path.join(BASE_DIR, cfg['dir'])
    orig_index = os.path.join(sec_dir, 'index.html')
    old_index = os.path.join(sec_dir, 'index_old.html')

    print(f"\n==================================================")
    print(f"處理單元：{cfg['unit']} {cfg['title']} ({cfg['dir']})")
    print(f"==================================================")

    # 1. 備份原 index.html 為 index_old.html（如果 index_old.html 還不存在）
    if not os.path.exists(old_index):
        if os.path.exists(orig_index):
            shutil.copy2(orig_index, old_index)
            print(f"  ✓ 已建立備份：index_old.html")
        else:
            raise FileNotFoundError(f"找不到 {orig_index}")
    else:
        print(f"  ℹ index_old.html 已存在，使用現有備份來源")

    # 讀取 index_old.html 作為原始來源
    with open(old_index, 'r', encoding='utf-8', errors='replace') as f:
        raw = f.read()

    # 2. 提取 <head>
    head_match = re.search(r'<head>.*?</head>', raw, re.DOTALL | re.IGNORECASE)
    if not head_match:
        raise RuntimeError(f"{cfg['dir']} 找不到 <head>")
    head_block = head_match.group(0)

    # 調整 CSS：去除 toolbar 預留空間，滿版置中
    head_modified = head_block.replace('right: 68px', 'right: 4px').replace('right: 58px', 'right: 4px')

    # 3. 提取 slides-container
    m = re.search(r'<div id=\"slides-container\">(.*?)</div>\s*<!--\s*/slides-container', raw, re.DOTALL)
    if not m:
        m = re.search(r'<div id=\"slides-container\">(.*?)</div>\s*<canvas id=\"drawing-layer\"', raw, re.DOTALL)
    if not m:
        m = re.search(r'<div id=\"slides-container\">(.*?)(?:<canvas\b|</div>\s*</div>\s*<!--\s*/presentation-area)', raw, re.DOTALL)
    if not m:
        raise RuntimeError(f"{cfg['dir']} 找不到 slides-container")
    container_inner = m.group(1)

    # 4. 提取 slide 列表（最後一個是 slide-game 連連看，跳過它，獨立做成 quiz.html）
    raw_slides = extract_slides(container_inner)
    print(f"  提取到 {len(raw_slides)} 個 slide 片段")

    content_slides = []
    for s in raw_slides:
        if 'id="slide-game"' in s or "id='slide-game'" in s or 'id="slide-game ' in s:
            print(f"    -> 排除舊連連看 slide-game (將由 quiz.html 承接)")
            continue
        content_slides.append(s)

    slide_count = len(content_slides)
    print(f"  有效內容 slide 數量：{slide_count}")

    # 5. 提取共用 JavaScript
    after_container = raw[m.end():]
    scripts_raw = re.findall(r'<script(?:\s[^>]*)?>.*?</script>', after_container, re.DOTALL | re.IGNORECASE)
    common_scripts = []
    for s in scripts_raw:
        # 排除白板滾動中繼（在主 index.html 中已有，slidepage 內部不需要）
        if '__chem_scroll_bridge' in s or 'scroll_relay.js' in s:
            continue
        # 只排除純開場遮罩的小腳本
        if len(s) < 2000 and ('startTeaching' in s or 'btn-start' in s):
            continue
        common_scripts.append(s)

    common_js_block = "\n".join(common_scripts)

    # 提取 container 外的 style（如 random-draw-balls 等）
    extra_styles_raw = re.findall(r'<style\b[^>]*>.*?</style>', after_container, re.DOTALL | re.IGNORECASE)
    extra_styles_block = "\n".join(extra_styles_raw)

    # 6. 生成 slidepage1.html ~ slidepageN.html
    for i, slide_content in enumerate(content_slides, start=1):
        # 確保 slide 有 active class
        slide_active = re.sub(
            r'class="(slide(?:[^"]*?))"',
            lambda sm: f'class="{sm.group(1)} active"' if 'active' not in sm.group(1) else sm.group(0),
            slide_content,
            count=1
        )

        slidepage_html = f"""<!DOCTYPE html>
<html lang="zh-TW">
{head_modified}
{extra_styles_block}
<body>
<div id="app">
    <div id="presentation-area">
        <div id="slides-container">
{slide_active}
        </div><!-- /slides-container -->
    </div><!-- /presentation-area -->
</div><!-- /app -->

{common_js_block}

</body>
</html>
"""
        out_page = os.path.join(sec_dir, f"slidepage{i}.html")
        with open(out_page, "w", encoding="utf-8") as pf:
            pf.write(slidepage_html)
        print(f"    ✓ slidepage{i}.html 已寫入 ({len(slidepage_html):,} bytes)")

    # 7. 生成 quiz.html
    quiz_html = generate_quiz_html(cfg)
    quiz_path = os.path.join(sec_dir, "quiz.html")
    with open(quiz_path, "w", encoding="utf-8") as qf:
        qf.write(quiz_html)
    print(f"  ✓ quiz.html 已寫入 ({len(quiz_html):,} bytes)")

    # 8. 生成新公版 index.html
    index_html = generate_index_html(cfg, slide_count)
    with open(orig_index, "w", encoding="utf-8") as inf:
        inf.write(index_html)
    print(f"  ✓ index.html 公版主框架已寫入 ({len(index_html):,} bytes)")

    print(f"  單元 {cfg['unit']} 完成！")


def main():
    print("🚀 開始執行第六章（化學反應速率）全單元公版化編修作業...")
    for cfg in CHAPTERS_CONFIG:
        process_section(cfg)
    print("\n🎉 全部小節（01~05）處理完畢！06_秒錶反應保持原貌，並已完成解鎖串接。")


if __name__ == '__main__':
    main()
