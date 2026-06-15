# -*- coding: utf-8 -*-
from fpdf import FPDF
import os

OUT = r"c:\Users\julsh\OneDrive - 國立新化高級工業職業學校\玩具檔案\my_化學網\光電池討論筆記.pdf"

# ── font paths ────────────────────────────────────────────────────────────────
WIN_FONTS = r"C:\Windows\Fonts"

def fpath(name):
    return os.path.join(WIN_FONTS, name)

# We'll use a CJK-capable font.
# Try NotoSansCJK, else fallback to system MSGOTHIC / Meiryo / DengXian
CJK_CANDIDATES = [
    ("NotoSansCJKtc-Regular.otf",  "NotoSans", False),
    ("NotoSansCJKtc-Bold.otf",     "NotoSans", True),
    ("msjh.ttc",   "MsJh",   False),   # Microsoft JhengHei
    ("msjhbd.ttc", "MsJh",   True),
    ("DengXian.ttf",  "DengXian", False),
    ("DengXianBold.ttf","DengXian",True),
    ("simsun.ttc", "SimSun",  False),
    ("MSMINCHO.TTC","MsMincho",False),
]

# Pick first available family
chosen_regular = None
chosen_bold    = None
family = None

for fname, fam, bold in CJK_CANDIDATES:
    fp = fpath(fname)
    if os.path.exists(fp):
        if not bold and chosen_regular is None:
            chosen_regular = fp
            family = fam
        elif bold and chosen_bold is None and fam == family:
            chosen_bold = fp

# If we got a regular but no bold, reuse regular for bold
if chosen_regular and not chosen_bold:
    chosen_bold = chosen_regular

print(f"Using font: {family}  regular={chosen_regular}  bold={chosen_bold}")

# ── helpers ───────────────────────────────────────────────────────────────────
DARK_BLUE  = (26,  58, 110)
MID_BLUE   = (58, 110, 200)
LIGHT_BLUE = (230, 238, 255)
WHITE      = (255, 255, 255)
TEXT       = (30,  30,  60)
MUTED      = (100, 115, 145)
GREEN_BG   = (238, 250, 245)
GREEN_BD   = (39,  174,  96)
RED_BG     = (255, 240, 240)
RED_BD     = (229,  57,  53)
AMBER_BG   = (255, 248, 225)
AMBER_BD   = (249, 168,  37)
PURPLE_BG  = (243, 238, 255)
PURPLE_BD  = (124,  58, 237)

# ── PDF class ─────────────────────────────────────────────────────────────────
class ChemPDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=18)
        self.set_margins(18, 18, 18)
        # register fonts
        self.add_font("CJK",  "", chosen_regular, uni=True)
        self.add_font("CJK",  "B", chosen_bold,   uni=True)
        self._fam = "CJK"

    # ── header/footer ─────────────────────────────────────────────────────────
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font(self._fam, "B", 8)
        self.set_text_color(*MUTED)
        self.cell(0, 8, "光電池與變色鏡片 化學機制討論筆記", align="L")
        self.ln(0)
        self.set_draw_color(*LIGHT_BLUE)
        self.line(18, self.get_y(), 192, self.get_y())
        self.ln(4)
        self.set_text_color(*TEXT)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-14)
        self.set_font(self._fam, "", 8)
        self.set_text_color(*MUTED)
        self.cell(0, 8, f"第 {self.page_no()-1} 頁  ·  高中化學學習網", align="C")

    # ── helpers ───────────────────────────────────────────────────────────────
    def h(self, size, bold=False):
        self.set_font(self._fam, "B" if bold else "", size)

    def write_text(self, txt, size=11, bold=False, color=TEXT, indent=0):
        self.set_font(self._fam, "B" if bold else "", size)
        self.set_text_color(*color)
        if indent:
            self.set_x(self.get_x() + indent)
        self.multi_cell(0, 6, txt)
        self.set_text_color(*TEXT)

    def section_title(self, num, title):
        """Numbered section heading"""
        self.ln(4)
        y = self.get_y()
        # circle badge
        self.set_fill_color(*DARK_BLUE)
        self.ellipse(18, y, 9, 9, "F")
        self.set_font(self._fam, "B", 10)
        self.set_text_color(*WHITE)
        self.set_xy(18, y + 1.5)
        self.cell(9, 6, str(num), align="C")
        # title
        self.set_font(self._fam, "B", 14)
        self.set_text_color(*DARK_BLUE)
        self.set_xy(30, y + 0.5)
        self.cell(0, 8, title)
        self.ln(10)
        # underline
        self.set_draw_color(*LIGHT_BLUE)
        self.set_line_width(0.5)
        self.line(18, self.get_y(), 192, self.get_y())
        self.ln(4)
        self.set_text_color(*TEXT)

    def sub_title(self, txt):
        self.ln(3)
        self.set_font(self._fam, "B", 11)
        self.set_text_color(*DARK_BLUE)
        self.cell(0, 7, txt)
        self.ln(7)
        self.set_text_color(*TEXT)

    def body(self, txt, size=10.5):
        self.set_font(self._fam, "", size)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 6, txt)
        self.ln(2)

    def eq(self, lines):
        """Equation / code block"""
        self.ln(2)
        self.set_fill_color(248, 249, 253)
        self.set_draw_color(208, 216, 240)
        self.set_line_width(0.3)
        x, y = self.get_x(), self.get_y()
        self.set_font(self._fam, "", 10)
        # measure height
        total = len(lines) * 6 + 8
        self.rect(x, y, 174, total, "FD")
        self.set_xy(x + 4, y + 4)
        for line in lines:
            self.set_font(self._fam, "B" if line.startswith("★") else "", 10)
            txt = line.lstrip("★")
            self.set_x(x + 4)
            self.cell(0, 6, txt)
            self.ln(6)
        self.ln(3)

    def info_box(self, title, lines, bg, bd):
        """Colored info box with left border"""
        self.ln(2)
        x, y = self.get_x(), self.get_y()
        # measure content
        self.set_font(self._fam, "", 10)
        line_h = 6
        total_h = (len(lines) + 1) * line_h + 8
        # background
        self.set_fill_color(*bg)
        self.rect(x, y, 174, total_h, "F")
        # left border bar
        self.set_fill_color(*bd)
        self.rect(x, y, 3, total_h, "F")
        # title
        self.set_xy(x + 6, y + 3)
        self.set_font(self._fam, "B", 10)
        self.set_text_color(*bd)
        self.cell(0, line_h, title)
        self.ln(line_h)
        # body lines
        self.set_font(self._fam, "", 10)
        self.set_text_color(*TEXT)
        for line in lines:
            self.set_x(x + 6)
            self.multi_cell(168, line_h, line)
        self.set_xy(x, y + total_h + 3)
        self.ln(2)

    def table(self, headers, rows, col_widths=None):
        """Simple styled table"""
        self.ln(2)
        n = len(headers)
        if col_widths is None:
            w = 174 / n
            col_widths = [w] * n
        # header row
        self.set_fill_color(*DARK_BLUE)
        self.set_text_color(*WHITE)
        self.set_font(self._fam, "B", 9.5)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 7, h, border=0, fill=True)
        self.ln(7)
        # data rows
        self.set_text_color(*TEXT)
        for ri, row in enumerate(rows):
            self.set_fill_color(*(LIGHT_BLUE if ri % 2 == 0 else WHITE))
            self.set_font(self._fam, "", 9.5)
            # use multi_cell for the last column, simple cell for others
            x0, y0 = self.get_x(), self.get_y()
            max_h = 6
            for i, cell in enumerate(row):
                self.set_xy(x0 + sum(col_widths[:i]), y0)
                self.set_fill_color(*(LIGHT_BLUE if ri % 2 == 0 else WHITE))
                # estimate lines needed
                chars_per_line = int(col_widths[i] / 3.5)
                lines_needed = max(1, (len(cell) + chars_per_line - 1) // chars_per_line)
                h = lines_needed * 6
                if h > max_h:
                    max_h = h
            # second pass: draw cells
            for i, cell in enumerate(row):
                self.set_xy(x0 + sum(col_widths[:i]), y0)
                self.set_fill_color(*(LIGHT_BLUE if ri % 2 == 0 else WHITE))
                self.multi_cell(col_widths[i], 6, cell, border="B", fill=True)
            self.set_xy(x0, y0 + max_h)
        self.ln(3)

    def divider(self):
        self.ln(3)
        self.set_draw_color(192, 204, 224)
        self.dashed_line(18, self.get_y(), 192, self.get_y(), dash_length=2, space_length=2)
        self.ln(5)

    def answer_box(self, lines):
        self.ln(3)
        x, y = self.get_x(), self.get_y()
        total_h = len(lines) * 8 + 10
        # gradient-like dark blue box
        self.set_fill_color(*DARK_BLUE)
        self.rect(x, y, 174, total_h, "F")
        self.set_text_color(*WHITE)
        self.set_font(self._fam, "B", 13)
        for i, line in enumerate(lines):
            self.set_xy(x, y + 4 + i * 8)
            self.cell(174, 8, line, align="C")
        self.set_xy(x, y + total_h + 3)
        self.set_text_color(*TEXT)
        self.ln(2)

# ── BUILD PDF ──────────────────────────────────────────────────────────────────
pdf = ChemPDF()

# ── COVER ─────────────────────────────────────────────────────────────────────
pdf.add_page()
pdf.set_fill_color(*DARK_BLUE)
pdf.rect(0, 0, 210, 297, "F")

# accent stripe
pdf.set_fill_color(*MID_BLUE)
pdf.rect(0, 120, 210, 4, "F")

# icon area
pdf.set_font("CJK", "B", 60)
pdf.set_text_color(*WHITE)
pdf.set_y(60)
pdf.cell(0, 30, "⚡", align="C")

# main title
pdf.ln(10)
pdf.set_font("CJK", "B", 24)
pdf.cell(0, 12, "光電池與變色鏡片", align="C"); pdf.ln(12)
pdf.cell(0, 12, "化學機制討論筆記", align="C"); pdf.ln(14)

# subtitle
pdf.set_font("CJK", "", 13)
pdf.set_text_color(180, 200, 240)
pdf.cell(0, 8, "電化學 × 光化學 × 固態物理", align="C"); pdf.ln(20)

# tags
tags = ["氧化還原", "電極電位", "光致變色", "AgCl 光化學"]
pdf.set_font("CJK", "", 10)
tag_w = 36
total_w = tag_w * len(tags) + 4 * (len(tags)-1)
x_start = (210 - total_w) / 2
for i, tag in enumerate(tags):
    pdf.set_xy(x_start + i * (tag_w + 4), pdf.get_y())
    pdf.set_fill_color(40, 70, 130)
    pdf.set_draw_color(100, 140, 200)
    pdf.set_line_width(0.3)
    pdf.cell(tag_w, 7, tag, border=1, fill=True, align="C")

# date
pdf.set_y(250)
pdf.set_font("CJK", "", 10)
pdf.set_text_color(140, 160, 200)
pdf.set_draw_color(80, 100, 160)
pdf.line(55, pdf.get_y(), 155, pdf.get_y())
pdf.ln(5)
pdf.cell(0, 6, "高中化學學習網  ·  2026 年 5 月 29 日", align="C")

# ── TABLE OF CONTENTS ─────────────────────────────────────────────────────────
pdf.add_page()
pdf.set_text_color(*TEXT)

# TOC box
pdf.ln(2)
pdf.set_fill_color(*LIGHT_BLUE)
pdf.set_draw_color(*MID_BLUE)
pdf.set_line_width(0.4)
pdf.rect(18, pdf.get_y(), 174, 8, "F")
pdf.set_font("CJK", "B", 13)
pdf.set_text_color(*DARK_BLUE)
pdf.set_x(22)
pdf.cell(0, 8, "📋  目錄")
pdf.ln(12)

toc = [
    ("1", "題目背景與光電池裝置說明"),
    ("2", "照光時 AB 兩端電壓計算（核心計算）"),
    ("3", "停止照光後逆反應是否自發？（熱力學分析）"),
    ("4", "變色鏡片如何達成可逆反應？（固態物理機制）"),
    ("5", "變色鏡片是否含有氯化亞銅？（成份比較）"),
    ("6", "AgCl 光解：兩種描述的統一"),
    ("7", "總結與重點整理"),
]
pdf.set_font("CJK", "", 11)
pdf.set_text_color(*TEXT)
for num, title in toc:
    pdf.set_x(22)
    pdf.set_font("CJK", "B", 11)
    pdf.set_text_color(*MID_BLUE)
    pdf.cell(10, 8, num + ".")
    pdf.set_font("CJK", "", 11)
    pdf.set_text_color(*TEXT)
    pdf.cell(0, 8, title)
    pdf.ln(8)

# ── SECTION 1 ─────────────────────────────────────────────────────────────────
pdf.add_page()
pdf.section_title(1, "題目背景與光電池裝置說明")
pdf.body("題目描述一個光電池（photoelectrochemical cell），其組成如下：")
pdf.table(
    ["半電池", "電極", "溶液", "端點"],
    [
        ["左側", "銀棒（鑲有氯化銀）", "1 M KCl 水溶液", "A"],
        ["右側", "白金絲（Pt）",        "氯化亞銅（CuCl）溶液", "B"],
    ],
    [22, 54, 72, 22]
)
pdf.sub_title("照光後發生的光化學反應")
pdf.eq(["AgCl(s)  ──hν──→  Ag(s)  +  Cl(AgCl)",
        "（氯原子暫時吸附在 AgCl 表面，記為 Cl(AgCl)）"])

pdf.sub_title("題目給定的半反應標準還原電位")
pdf.table(
    ["#", "半反應", "E°（V）"],
    [
        ["①", "AgCl(s) + e⁻ → Ag(s) + Cl(aq)⁻", "+0.22"],
        ["②", "Cu(aq)²⁺ + e⁻ → Cu(aq)⁺",         "+0.15"],
        ["③", "Cl(AgCl) + e⁻ → Cl(aq)⁻",          "+3.80  ★最高★"],
        ["④", "Cu(aq)⁺ + e⁻ → Cu(s)",              "+0.52"],
        ["⑤", "Ag(aq)⁺ + e⁻ → Ag(s)",              "+0.79"],
    ],
    [12, 120, 42]
)
pdf.info_box("🔑 關鍵觀察", [
    "Cl(AgCl) 的還原電位高達 +3.80 V，是極強的氧化劑。",
    "照光後產生的 Cl(AgCl) 將主導電化學反應方向。",
], LIGHT_BLUE, MID_BLUE)

# ── SECTION 2 ─────────────────────────────────────────────────────────────────
pdf.add_page()
pdf.section_title(2, "照光時 AB 兩端電壓計算")
pdf.sub_title("判斷正負極")
pdf.body("照光後 Cl(AgCl) 是最強氧化劑（E° = +3.80 V），優先在左側 A 極（Ag 棒）被還原，"
         "→ A 端為陰極（正極）。右側 B 端（Pt）發生氧化反應 → B 端為陽極（負極）。")
pdf.table(
    ["電極", "位置", "反應類型", "半反應", "E°"],
    [
        ["A 端（正極）", "左（Ag棒）", "陰極（還原）", "Cl(AgCl)+e⁻→Cl(aq)⁻", "+3.80 V"],
        ["B 端（負極）", "右（Pt絲）", "陽極（氧化）", "Cu⁺→Cu²⁺+e⁻（逆）",  "逆+0.15 V"],
    ],
    [28, 24, 28, 62, 22]
)
pdf.sub_title("計算電池電動勢")
pdf.eq([
    "E(電池) = E°(陰極) − E°(陽極)",
    "       = 3.80 − 0.15",
    "★       = 3.65 V",
])
pdf.answer_box([
    "V(AB) = V(A) − V(B) = +3.65 V",
    "A 端為正（+），B 端為負（−）",
    "電流由 A 流向外電路至 B",
])

# ── SECTION 3 ─────────────────────────────────────────────────────────────────
pdf.add_page()
pdf.section_title(3, "停止照光後逆反應是否自發？")
pdf.body("停止照光後不再產生 Cl(AgCl)。若要透過電化學逆反應回復（電池反向放電），需考慮：")
pdf.table(
    ["電極", "逆向半反應", "E°"],
    [
        ["B端（陰極）", "Cu(aq)²⁺ + e⁻ → Cu(aq)⁺", "+0.15 V"],
        ["A端（陽極）", "Ag(s) + Cl⁻ → AgCl(s) + e⁻（氧化）", "−0.22 V"],
    ],
    [28, 116, 30]
)
pdf.eq([
    "E(逆) = E°(陰極) − E°(陽極，還原電位)",
    "     = 0.15 − 0.22",
    "★     = −0.07 V  <  0",
])
pdf.info_box("❌ 電化學逆反應不自發", [
    "E < 0  →  ΔG = −nFE > 0  →  非自發反應",
    "光電池在電化學上是不可逆的，",
    "無法像一般充電電池般逆向放電。",
], RED_BG, RED_BD)

pdf.sub_title("那為何題目說停光後會「立即回復」？")
pdf.table(
    ["機制", "是否發生", "說明"],
    [
        ["光化學重組\nCl(AgCl)+Ag→AgCl", "✅ 自發", "Cl活性極強，直接與鄰近Ag重組"],
        ["電化學逆反應\n（放電反向）",     "❌ 不自發", "E=−0.07V，ΔG>0"],
    ],
    [60, 28, 86]
)
pdf.info_box("💡 結論", [
    "系統回復初始 AgCl 狀態，靠的是光化學途徑（Cl 與 Ag 直接重組），",
    "而非電化學逆反應。",
    "停光 → Cl(AgCl) 失去光能支撐 → 立即與 Ag 重組 → AgCl 回復。",
], AMBER_BG, AMBER_BD)

# ── SECTION 4 ─────────────────────────────────────────────────────────────────
pdf.add_page()
pdf.section_title(4, "變色鏡片如何達成可逆反應？")
pdf.body("變色鏡片與題目光電池組成相似，但可逆性的關鍵差異在於反應介質的物理限制。")

pdf.sub_title("核心差異：產物能不能「逃跑」")
pdf.table(
    ["比較項目", "題目光電池", "玻璃變色鏡片"],
    [
        ["介質",      "液態電解質溶液",           "固態玻璃基質"],
        ["Cl 的去向", "擴散進溶液，遠離 Ag",      "被困在晶粒附近，無法移動"],
        ["Cu²⁺ 去向", "在另極生成，產物分離",     "留在固態晶粒附近"],
        ["逆反應",    "❌ 不自發（E=−0.07 V）",   "✅ 熱力學可行（固態重組）"],
    ],
    [36, 70, 68]
)

pdf.sub_title("玻璃變色鏡片的完整機制")
pdf.eq([
    "【照光變暗】",
    "AgCl(s) ──hν──→ Ag(s) + Cl(AgCl)",
    "  → Cl 吸附在 AgCl 晶粒表面",
    "  → Ag⁰ 聚集成奈米銀團簇（黑色）→ 鏡片變暗",
    "",
    "【停光恢復（熱力學自發）】",
    "Cl(AgCl) + Ag(s) ──熱能──→ AgCl(s)",
    "  → Cl 未逃離，立即與鄰近 Ag 重組",
    "  → AgCl 再生，銀團簇消失 → 鏡片恢復透明",
])
pdf.info_box("🔑 關鍵：固態空間限制（Spatial Confinement）", [
    "AgCl 微晶被嵌在玻璃網絡中，Cl 原子根本無法擴散遠離，",
    "永遠待在 Ag 旁邊。停光後，熱振動能量就足以驅動",
    "Cl + Ag → AgCl 的重組。",
], GREEN_BG, GREEN_BD)

# ── SECTION 5 ─────────────────────────────────────────────────────────────────
pdf.add_page()
pdf.section_title(5, "變色鏡片是否含有氯化亞銅（CuCl）？")
pdf.info_box("⚠️ 令人驚訝的答案", [
    "傳統玻璃型光致變色鏡片（如 Corning Photogray）",
    "確實含有 CuCl！與題目光電池成分幾乎相同。",
], AMBER_BG, AMBER_BD)

pdf.sub_title("傳統玻璃變色鏡片成分")
pdf.table(
    ["成分", "角色"],
    [
        ["AgCl / AgBr 微晶", "主要感光物質"],
        ["CuCl（Cu⁺）",      "電洞捕捉劑（增感劑）★關鍵"],
        ["SiO₂、Al₂O₃、B₂O₃", "玻璃基質（提供空間限制）"],
    ],
    [60, 114]
)

pdf.sub_title("Cu⁺ 的功能")
pdf.eq([
    "【無 Cu⁺ 的情況】",
    "AgCl + hν → [e⁻ + h⁺]",
    "  → e⁻ 與 h⁺ 立即復合 → 白白放熱，Ag⁰ 很少形成",
    "  → 變暗效率極差",
    "",
    "【有 Cu⁺ 的情況】",
    "AgCl + hν → [e⁻ + h⁺]",
    "  h⁺ 被 Cu⁺ 捕捉：Cu⁺ + h⁺ → Cu²⁺  （阻止立即復合）",
    "  e⁻ 還原銀離子：Ag⁺ + e⁻ → Ag⁰  （銀原子大量形成）",
    "  Ag⁰ 聚集成銀團簇 → 鏡片迅速有效變暗 ✅",
])

pdf.sub_title("與題目光電池的對比")
pdf.table(
    ["比較", "題目光電池", "玻璃變色鏡片"],
    [
        ["AgCl", "✅", "✅"],
        ["CuCl", "✅", "✅  也有！"],
        ["Cu²⁺ 命運", "隨溶液遠離", "被困在固態晶粒附近"],
        ["逆反應",   "❌ 電化學不自發", "✅ 熱力學自發重組"],
    ],
    [36, 68, 70]
)

pdf.sub_title("現代塑膠變色鏡片（Transitions 等）")
pdf.info_box("🌀 完全不同的有機機制", [
    "採用有機光致變色化合物（螺吡喃、萘吡喃）嵌入塑膠，",
    "靠分子構型改變（開環↔閉環）變色，完全不含 AgCl 或 CuCl。",
    "",
    "  螺吡喃（無色，閉環）──hν──→ 開環型（有色）",
    "  開環型 ──熱能/可見光──→ 螺吡喃（無色，閉環）✅ 可逆",
], PURPLE_BG, PURPLE_BD)

# ── SECTION 6 ─────────────────────────────────────────────────────────────────
pdf.add_page()
pdf.section_title(6, "AgCl 光解：兩種描述的統一")
pdf.body("學習中常見到 AgCl 光解的兩種寫法，容易誤以為是兩個同時存在的反應：")
pdf.info_box("化學描述", ["AgCl(s) + hν → Ag(s) + Cl(AgCl)"], LIGHT_BLUE, MID_BLUE)
pdf.info_box("固態物理描述", ["AgCl + hν → Ag⁺ + e⁻（電子電洞對）"], PURPLE_BG, PURPLE_BD)
pdf.info_box("⚠️ 重要釐清", [
    "這不是兩個同時競爭的反應——",
    "它們是同一個反應在不同層次的描述！",
], AMBER_BG, AMBER_BD)

pdf.sub_title("完整的反應步驟順序")
pdf.eq([
    "步驟①  AgCl 吸收光子（hν）",
    "",
    "步驟②  在晶格中瞬間產生「電子-電洞對」（極短暫中間態）",
    "        e⁻（導帶） ＋ h⁺（價帶）",
    "",
    "步驟③  兩者同時發生：",
    "        e⁻ 遷移：  Ag⁺ + e⁻ → Ag⁰",
    "        h⁺ 遷移：  Cl⁻ + h⁺ → Cl⁰",
    "",
    "步驟④  淨結果（化學描述）：",
    "★       AgCl + hν → Ag⁰ + Cl(AgCl)",
])

pdf.sub_title("兩種描述的對應關係")
pdf.table(
    ["描述方式", "適用情境", "重點"],
    [
        ["化學描述\n（Ag+Cl 生成）", "討論最終產物\n討論逆反應重組", "說明宏觀化學變化"],
        ["固態物理描述\n（電子電洞對）", "解釋 Cu⁺ 增感作用\n解釋光電效率", "說明微觀機制"],
    ],
    [44, 70, 60]
)
pdf.info_box("✅ 正確理解", [
    "「電子電洞對」是中間過渡態，「Ag⁰ 和 Cl(AgCl) 的生成」是最終結果。",
    "兩種描述都正確，只是描述的層次不同。",
    "Cu⁺ 的角色是在步驟③捕捉電洞，防止 e⁻ 與 h⁺ 復合，使 Ag⁰ 能大量累積。",
], GREEN_BG, GREEN_BD)

# ── SECTION 7 ─────────────────────────────────────────────────────────────────
pdf.add_page()
pdf.section_title(7, "總結與重點整理")

pdf.sub_title("🎯 核心計算結果")
pdf.table(
    ["情況", "反應", "E°", "自發？"],
    [
        ["照光（正向）", "Cl(AgCl)還原 / Cu⁺氧化", "+3.65 V", "✅  V(AB)=+3.65V"],
        ["停光（電化學逆向）", "Cu²⁺還原 / Ag氧化", "−0.07 V", "❌ 不自發"],
    ],
    [36, 60, 26, 52]
)

pdf.sub_title("🔬 三種系統的比較")
pdf.table(
    ["系統", "AgCl", "CuCl", "逆反應途徑", "可逆性"],
    [
        ["題目光電池",   "✅", "✅", "光化學重組（有限）", "有限可逆"],
        ["玻璃變色鏡片", "✅", "✅", "熱驅動重組（固態限制）", "✅ 可逆"],
        ["塑膠變色鏡片", "❌", "❌", "分子構型開環↔閉環",   "✅ 可逆"],
    ],
    [40, 14, 14, 64, 26]
)

pdf.sub_title("💡 最重要的概念")
points = [
    "① 電化學可逆性的關鍵不只是 E° 的正負，更在於產物是否被分離。",
    "② 固態介質的「空間限制」讓 AgCl 系統能在停光後自發重組，",
    "   這是玻璃變色鏡片的核心原理。",
    "③ Cu⁺ 是「電洞捕捉劑」，阻止光生電子電洞對立即復合，",
    "   讓銀原子能有效累積形成銀團簇。",
    "④ AgCl 光解的「化學描述」與「固態物理描述」是同一過程的不同層次，",
    "   並非兩個競爭反應。",
]
pdf.set_font("CJK", "", 10.5)
pdf.set_text_color(*TEXT)
for pt in points:
    pdf.set_x(20)
    pdf.multi_cell(0, 6.5, pt)
    pdf.ln(1)

pdf.ln(6)
pdf.answer_box([
    "🏁  光電池照光時  V(AB) = +3.65 V（A正B負）",
    "停光後電化學逆反應 E = −0.07 V，不自發",
])

# ── SAVE ──────────────────────────────────────────────────────────────────────
pdf.output(OUT)
print(f"✅ PDF 已完成：{OUT}")
