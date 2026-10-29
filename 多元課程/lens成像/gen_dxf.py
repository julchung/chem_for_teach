"""
iPhone 17 標準版 鏡頭轉接貼片 DXF 產生器
=============================================
所有尺寸單位：mm（毫米）

外框：Rounded Rectangle  34 × 42 mm，圓角 R10
主鏡頭：Ø16.5 mm
超廣角：Ø14.5 mm
小圓孔（感應器）：Ø3 mm

座標系：原點在外框幾何中心
"""

import math
import ezdxf
from ezdxf import units

# ─── 尺寸參數 ────────────────────────────────────────────────
# 外框（Rounded Rectangle）
W  = 34.0    # 寬度 (x 方向)
H  = 42.0    # 高度 (y 方向)
R  = 10.0    # 圓角半徑

# 鏡頭孔（圓形）
D_MAIN = 16.5   # 主鏡頭直徑
D_UW   = 14.5   # 超廣角直徑
D_DOT  = 3.0    # 小圓孔直徑

# 兩鏡頭圓心距（中心間距）
CC_DIST = 20.0  # 主鏡頭與超廣角圓心距

# 主鏡頭圓心（在外框中心偏上）
MAIN_CX = 0.0
MAIN_CY = CC_DIST / 2   # = +10.0

# 超廣角圓心（在外框中心偏下）
UW_CX = 0.0
UW_CY = -CC_DIST / 2    # = -10.0

# 小圓孔圓心（右下角附近）
DOT_CX = W/2 - 5.0      # 距右邊 5mm
DOT_CY = UW_CY           # 與超廣角同高


# ─── 建立 DXF 文件 ───────────────────────────────────────────
doc = ezdxf.new('R2010')
doc.units = units.MM
msp = doc.modelspace()

# 圖層設定
doc.layers.add('OUTLINE',   color=1)  # 紅色 = 外輪廓
doc.layers.add('LENS_MAIN', color=3)  # 綠色 = 主鏡頭
doc.layers.add('LENS_UW',   color=5)  # 藍色 = 超廣角
doc.layers.add('DOT',       color=6)  # 洋紅 = 小圓孔
doc.layers.add('CENTER',    color=8)  # 灰色 = 中心線
doc.layers.add('DIMS',      color=2)  # 黃色 = 標注

# ─── 繪製外框（Rounded Rectangle）───────────────────────────
# 以四段直線 + 四段圓弧組成
# 頂部直線
msp.add_line((-W/2+R, H/2), (W/2-R, H/2), dxfattribs={'layer': 'OUTLINE'})
# 底部直線
msp.add_line((-W/2+R, -H/2), (W/2-R, -H/2), dxfattribs={'layer': 'OUTLINE'})
# 左側直線
msp.add_line((-W/2, H/2-R), (-W/2, -H/2+R), dxfattribs={'layer': 'OUTLINE'})
# 右側直線
msp.add_line((W/2, H/2-R), (W/2, -H/2+R), dxfattribs={'layer': 'OUTLINE'})

# 四個圓角弧
# 右上角 (W/2-R, H/2-R)，從 0° 到 90°
msp.add_arc((W/2-R, H/2-R), R, 0, 90, dxfattribs={'layer': 'OUTLINE'})
# 左上角 (-W/2+R, H/2-R)，從 90° 到 180°
msp.add_arc((-W/2+R, H/2-R), R, 90, 180, dxfattribs={'layer': 'OUTLINE'})
# 左下角 (-W/2+R, -H/2+R)，從 180° 到 270°
msp.add_arc((-W/2+R, -H/2+R), R, 180, 270, dxfattribs={'layer': 'OUTLINE'})
# 右下角 (W/2-R, -H/2+R)，從 270° 到 360°
msp.add_arc((W/2-R, -H/2+R), R, 270, 360, dxfattribs={'layer': 'OUTLINE'})

# ─── 繪製主鏡頭孔 ───────────────────────────────────────────
msp.add_circle((MAIN_CX, MAIN_CY), D_MAIN/2, dxfattribs={'layer': 'LENS_MAIN'})

# ─── 繪製超廣角鏡頭孔 ────────────────────────────────────────
msp.add_circle((UW_CX, UW_CY), D_UW/2, dxfattribs={'layer': 'LENS_UW'})

# ─── 繪製小圓孔 ──────────────────────────────────────────────
msp.add_circle((DOT_CX, DOT_CY), D_DOT/2, dxfattribs={'layer': 'DOT'})

# ─── 中心線（十字） ──────────────────────────────────────────
cl_attr = {'layer': 'CENTER', 'linetype': 'CENTER'}

# 外框垂直中心線
msp.add_line((0, H/2+5), (0, -H/2-5), dxfattribs={'layer': 'CENTER'})
# 外框水平中心線
msp.add_line((-W/2-5, 0), (W/2+5, 0), dxfattribs={'layer': 'CENTER'})

# 主鏡頭中心十字
cs = 3.0
msp.add_line((MAIN_CX-cs, MAIN_CY), (MAIN_CX+cs, MAIN_CY), dxfattribs={'layer': 'CENTER'})
msp.add_line((MAIN_CX, MAIN_CY-cs), (MAIN_CX, MAIN_CY+cs), dxfattribs={'layer': 'CENTER'})

# 超廣角中心十字
msp.add_line((UW_CX-cs, UW_CY), (UW_CX+cs, UW_CY), dxfattribs={'layer': 'CENTER'})
msp.add_line((UW_CX, UW_CY-cs), (UW_CX, UW_CY+cs), dxfattribs={'layer': 'CENTER'})

# 小圓孔中心十字
msp.add_line((DOT_CX-1.5, DOT_CY), (DOT_CX+1.5, DOT_CY), dxfattribs={'layer': 'CENTER'})
msp.add_line((DOT_CX, DOT_CY-1.5), (DOT_CX, DOT_CY+1.5), dxfattribs={'layer': 'CENTER'})


# ─── 尺寸標注 ────────────────────────────────────────────────
dim_style = doc.dimstyles.new('MM_STYLE')
dim_style.dxf.dimtxt = 1.5    # 文字高度
dim_style.dxf.dimasz = 1.2    # 箭頭大小
dim_style.dxf.dimscale = 1.0

# 整體寬度標注（底部外側）
msp.add_linear_dim(
    base=(0, -H/2 - 8),
    p1=(-W/2, -H/2),
    p2=(W/2, -H/2),
    angle=0,
    dimstyle='MM_STYLE',
    override={'dimpost': '%%C<>'} if False else {},
    dxfattribs={'layer': 'DIMS'}
).render()

# 整體高度標注（右側外側）
msp.add_linear_dim(
    base=(W/2 + 10, 0),
    p1=(W/2, -H/2),
    p2=(W/2, H/2),
    angle=90,
    dimstyle='MM_STYLE',
    dxfattribs={'layer': 'DIMS'}
).render()

# 主鏡頭直徑標注
msp.add_diameter_dim(
    center=(MAIN_CX, MAIN_CY),
    radius=D_MAIN/2,
    angle=45,
    dimstyle='MM_STYLE',
    dxfattribs={'layer': 'DIMS'}
).render()

# 超廣角直徑標注
msp.add_diameter_dim(
    center=(UW_CX, UW_CY),
    radius=D_UW/2,
    angle=45,
    dimstyle='MM_STYLE',
    dxfattribs={'layer': 'DIMS'}
).render()

# 小圓孔直徑標注
msp.add_diameter_dim(
    center=(DOT_CX, DOT_CY),
    radius=D_DOT/2,
    angle=45,
    dimstyle='MM_STYLE',
    dxfattribs={'layer': 'DIMS'}
).render()

# 兩鏡頭圓心距標注
msp.add_linear_dim(
    base=(-W/2 - 10, 0),
    p1=(MAIN_CX, MAIN_CY),
    p2=(UW_CX, UW_CY),
    angle=90,
    dimstyle='MM_STYLE',
    dxfattribs={'layer': 'DIMS'}
).render()

# ─── 儲存 DXF ────────────────────────────────────────────────
output_path = r"iPhone17_lens_protector.dxf"
doc.saveas(output_path)
print(f"[OK] DXF saved: {output_path}")
print()
print("=== Dimensions ===")
print(f"Frame:           {W} x {H} mm, corner R{R} mm")
print(f"Main lens (D):   {D_MAIN} mm")
print(f"Ultra-wide (D):  {D_UW} mm")
print(f"Sensor dot (D):  {D_DOT} mm")
print(f"Lens C-C dist:   {CC_DIST} mm")
print(f"Main lens Y:     +{MAIN_CY} mm (from center)")
print(f"UltraWide Y:     {UW_CY} mm (from center)")
print(f"Dot center:      ({DOT_CX}, {DOT_CY}) mm (from center)")
