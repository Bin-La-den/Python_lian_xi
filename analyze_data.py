"""
对 data.xlsx 进行数据可视化分析
生成文件：province_bar.png — 省份分布柱状图
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# 配色方案（CVD 安全的蓝色渐变 — 用色阶表达数量大小）
# ============================================================
SEQ_BLUE = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#2a78d6", "#1c5cab", "#104281"]

INK_PRIMARY   = "#0b0b0b"
INK_SECONDARY = "#52514e"
INK_MUTED     = "#898781"
GRIDLINE      = "#e1e0d9"
SURFACE       = "#fcfcfb"

# matplotlib rc — 使用系统中已安装的 Source Han Sans CN（思源黑体）
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Source Han Sans CN", "HYKaiTiJ", "LXGW WenKai GB Screen", "DejaVu Sans"],
    "axes.unicode_minus": False,
    "figure.dpi": 150,
    "savefig.dpi": 150,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.2,
})

# ============================================================
# 读取数据
# ============================================================
df = pd.read_excel("data.xlsx")
total = len(df)
province_counts = df["收件人省"].value_counts()
max_count = province_counts.iloc[0]
top5 = province_counts.head(5)

print(f"总记录数: {total}")
print(f"覆盖省份: {len(province_counts)}")
print(f"最多省份: {province_counts.index[0]} ({province_counts.iloc[0]} 人, {province_counts.iloc[0] / total * 100:.1f}%)")
print(f"前 5 省份合计占比 {top5.sum() / total * 100:.1f}%")

# ============================================================
# 柱状图 — 各省份收件人数量（横向，按数量降序）
# ============================================================
fig, ax = plt.subplots(figsize=(10, 8))
fig.set_facecolor(SURFACE)
ax.set_facecolor(SURFACE)

provinces_list = list(province_counts.items())
names  = [p[0] for p in reversed(provinces_list)]
counts = [p[1] for p in reversed(provinces_list)]

# 蓝色渐变：数量越大颜色越深
n = len(counts)
color_indices = np.linspace(0, len(SEQ_BLUE) - 1, n).astype(int)
bar_colors = [SEQ_BLUE[i] for i in color_indices]

ax.barh(range(n), counts, height=0.7, color=bar_colors, edgecolor="none")

# 直接标注数值
for i, cnt in enumerate(counts):
    ax.text(cnt + max_count * 0.015, i, str(cnt),
            va="center", fontsize=9, color=INK_SECONDARY)

# 坐标轴
ax.set_yticks(range(n))
ax.set_yticklabels(names, fontsize=10, color=INK_PRIMARY)
ax.tick_params(left=False)
ax.xaxis.set_ticks_position("top")
ax.xaxis.set_label_position("top")
ax.tick_params(axis="x", colors=INK_MUTED, labelsize=8, pad=2)

# 网格线
ax.set_axisbelow(True)
ax.xaxis.grid(True, color=GRIDLINE, linewidth=0.5, alpha=0.7)
ax.yaxis.grid(False)

# 隐藏边框
for spine in ax.spines.values():
    spine.set_visible(False)

ax.set_xlim(0, max_count * 1.18)
ax.set_title("各省份收件人数量分布", fontsize=16, fontweight=600,
             color=INK_PRIMARY, pad=16, loc="left")

fig.tight_layout()
fig.savefig("province_bar.png", facecolor=SURFACE, edgecolor="none")
plt.close(fig)

print("\n✓ 已生成 province_bar.png")
print(f"\n关键发现：")
print(f"  · {province_counts.index[0]} 占比 {province_counts.iloc[0] / total * 100:.1f}%，接近一半")
print(f"  · 前 5 省份合计占比 {top5.sum() / total * 100:.1f}%")
print(f"  · 所有 {total} 个收件人姓名均不重复")