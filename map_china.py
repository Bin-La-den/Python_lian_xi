"""
对中国 data.xlsx 中的 24 个省份进行地图标注
使用 Albers 等面积圆锥投影（中国标准地图投影）
包含南海诸岛附图，输出 PDF

运行方式：
    conda activate map_env && python3 map_china.py
"""
import pandas as pd
import requests
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
import numpy as np
from shapely.geometry import shape, MultiPolygon

# ============================================================
# 0. Albers 等面积圆锥投影（中国标准）
# ============================================================
# 标准纬线 25°N, 47°N，中央经线 105°E
PHI1 = np.radians(25)   # 第一标准纬线
PHI2 = np.radians(47)   # 第二标准纬线
LON0 = np.radians(105)  # 中央经线
PHI0 = np.radians(35)   # 投影原点纬度

n_val = (np.sin(PHI1) + np.sin(PHI2)) / 2
C_val = np.cos(PHI1)**2 + 2 * n_val * np.sin(PHI1)
rho0  = np.sqrt(max(C_val - 2 * n_val * np.sin(PHI0), 1e-12)) / n_val

def albers(lon, lat):
    """将 (lon, lat) 度 转换为 Albers 投影坐标 (x, y)"""
    phi   = np.radians(lat)
    lam   = np.radians(lon)
    theta = n_val * (lam - LON0)
    rho   = np.sqrt(max(C_val - 2 * n_val * np.sin(phi), 1e-12)) / n_val
    x = rho * np.sin(theta)
    y = rho0 - rho * np.cos(theta)
    return x, y

def transform_ring(ring):
    """将一个坐标环 [(lon,lat), ...] 转换为投影坐标 [(x,y), ...]"""
    pts = np.array([albers(p[0], p[1]) for p in ring])
    return pts

# ============================================================
# 1. 读取数据
# ============================================================
df = pd.read_excel("data.xlsx")
province_counts = df["收件人省"].value_counts()
data_provinces = set(province_counts.index.tolist())
total = province_counts.sum()
print(f"数据: {len(data_provinces)} 个省份, 共 {total} 人")

# ============================================================
# 2. 获取 GeoJSON
# ============================================================
geojson_url = "https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json"
print(f"获取中国地图数据…")
resp = requests.get(geojson_url, timeout=30)
resp.raise_for_status()
china_geojson = resp.json()

# 过滤空白名称
china_geojson["features"] = [
    f for f in china_geojson["features"]
    if f["properties"].get("name", "").strip()
]
print(f"有效区域: {len(china_geojson['features'])} 个")

# ============================================================
# 3. 名称匹配
# ============================================================
def match_province(data_name, geojson_features):
    for feat in geojson_features:
        gname = feat["properties"].get("name", "")
        if gname == data_name:
            return feat
        if len(gname) >= 2 and data_name.startswith(gname):
            return feat
        if len(data_name) >= 2 and gname.startswith(data_name):
            return feat
    return None

matched = []
for prov in data_provinces:
    feat = match_province(prov, china_geojson["features"])
    if feat:
        matched.append((prov, province_counts[prov], feat))
    else:
        print(f"  未匹配: {prov}")

matched_names = {feat["properties"]["name"] for _, _, feat in matched}
data_feats  = [f for f in china_geojson["features"] if f["properties"]["name"] in matched_names]
other_feats = [f for f in china_geojson["features"] if f["properties"]["name"] not in matched_names]

# ============================================================
# 4. 配色与字体
# ============================================================
C_HIGHLIGHT = "#2a78d6"
C_OTHER     = "#e8e8e8"
C_BG        = "#ffffff"
C_EDGE      = "#ffffff"
C_FRAME     = "#333333"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Source Han Sans CN", "HYKaiTiJ", "LXGW WenKai GB Screen", "DejaVu Sans"],
    "axes.unicode_minus": False,
})

# ============================================================
# 5. 绘制函数
# ============================================================
def draw_feature(ax, feat, facecolor, edgecolor, lw, alpha):
    """将一个 GeoJSON feature 用 Albers 投影绘制到 axes 上"""
    try:
        geom = shape(feat["geometry"])
        polys = geom.geoms if isinstance(geom, MultiPolygon) else [geom]
        for poly in polys:
            if poly.is_empty:
                continue
            ext = transform_ring(poly.exterior.coords)
            ax.add_patch(MplPolygon(ext, closed=True, facecolor=facecolor,
                                     edgecolor=edgecolor, linewidth=lw,
                                     alpha=alpha, joinstyle="round"))
    except Exception:
        pass

def draw_map(ax, features, highlight_names, highlight_color, other_color,
             labels=None):
    """在 axes 上绘制完整中国地图"""
    # 先灰色（底层），再蓝色（上层）
    for feat in features:
        if feat["properties"]["name"] not in highlight_names:
            draw_feature(ax, feat, other_color, C_EDGE, lw=0.25, alpha=0.55)
    for feat in features:
        if feat["properties"]["name"] in highlight_names:
            draw_feature(ax, feat, highlight_color, C_EDGE, lw=0.3, alpha=0.82)

    # 标注
    if labels:
        for name, cnt, center in labels:
            if center is None:
                continue
            cx, cy = albers(center[0], center[1])
            pct = cnt / total * 100
            if pct >= 5:
                ax.text(cx, cy, f"{name}\n{cnt}人", fontsize=9.5, fontweight="bold",
                        color="#0b0b0b", ha="center", va="center",
                        bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.72))
            elif pct >= 2:
                ax.text(cx, cy, f"{name}\n{cnt}", fontsize=7.5, color="#0b0b0b",
                        ha="center", va="center")
            else:
                ax.text(cx, cy, f"{name} {cnt}", fontsize=6, color="#52514e",
                        ha="center", va="center")

# ============================================================
# 6. 计算边界
# ============================================================
all_features = china_geojson["features"]
all_x, all_y = [], []
for feat in all_features:
    try:
        geom = shape(feat["geometry"])
        polys = geom.geoms if isinstance(geom, MultiPolygon) else [geom]
        for poly in polys:
            if poly.is_empty:
                continue
            tx, ty = transform_ring(poly.exterior.coords).T
            all_x.extend(tx)
            all_y.extend(ty)
    except Exception:
        pass

pad = 0.04
x_min, x_max = min(all_x) - pad, max(all_x) + pad
y_min, y_max = min(all_y) - pad, max(all_y) + pad

# 南海附图范围（度）：lon 107~122, lat 3~24
nh_lon_bounds = (107, 122)
nh_lat_bounds = (3, 24)
# 转换南海四角
nh_corners_lon = [nh_lon_bounds[0], nh_lon_bounds[1], nh_lon_bounds[1], nh_lon_bounds[0]]
nh_corners_lat = [nh_lat_bounds[0], nh_lat_bounds[0], nh_lat_bounds[1], nh_lat_bounds[1]]
nh_x = []
nh_y = []
for lo, la in zip(nh_corners_lon, nh_corners_lat):
    x, y = albers(lo, la)
    nh_x.append(x)
    nh_y.append(y)

# ============================================================
# 7. 绘图
# ============================================================
fig, ax = plt.subplots(figsize=(14, 12))
fig.patch.set_facecolor(C_BG)
ax.set_facecolor(C_BG)
ax.set_aspect("equal")

# --- 主图 ---
label_data = []
for _, cnt, feat in matched:
    label_data.append((feat["properties"]["name"], cnt, feat["properties"].get("center")))

draw_map(ax, all_features, matched_names, C_HIGHLIGHT, C_OTHER, labels=label_data)

# 南海附图范围边框（虚线小框标记在主图上）
from matplotlib.patches import Rectangle as MplRect
# 找一个合适的 Albers 坐标位置做南海示意框
ax.add_patch(MplRect((x_min + 0.02, y_min + 0.02),
                      (x_max - x_min) * 0.11,
                      (y_max - y_min) * 0.11,
                      fill=False, edgecolor="#999999",
                      linewidth=0.8, linestyle="--"))
ax.text(x_min + 0.02 + (x_max - x_min) * 0.115, y_min + 0.02,
        "南海\n诸岛", fontsize=7, color="#888888", ha="left", va="bottom")

# 图例
from matplotlib.patches import Patch
legend = [
    Patch(facecolor=C_HIGHLIGHT, edgecolor="white", label=f"有数据省份（{len(matched)} 个）"),
    Patch(facecolor=C_OTHER, edgecolor="white", label="无数据省份"),
]
ax.legend(handles=legend, loc="lower left", fontsize=9,
          frameon=True, facecolor="white", edgecolor="#cccccc",
          bbox_to_anchor=(0.46, 0.01))

# --- 南海诸岛附图（嵌入右下角）---
# 在 figure 坐标中放置一个小 axes
from matplotlib.transforms import Bbox
ax_nh = fig.add_axes([0.72, 0.10, 0.20, 0.22])
ax_nh.set_facecolor(C_BG)
ax_nh.set_aspect("equal")

draw_map(ax_nh, all_features, matched_names, C_HIGHLIGHT, C_OTHER, labels=None)

ax_nh.set_xlim(min(nh_x) - 0.5, max(nh_x) + 0.5)
ax_nh.set_ylim(min(nh_y) - 0.5, max(nh_y) + 0.5)
ax_nh.set_xticks([])
ax_nh.set_yticks([])

# 南海附图边框
for spine in ax_nh.spines.values():
    spine.set_visible(True)
    spine.set_edgecolor(C_FRAME)
    spine.set_linewidth(1.2)

# 南海附图标题
ax_nh.set_title("南海诸岛", fontsize=8, color="#333333", pad=3)

# --- 主图设置 ---
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

fig.suptitle(f"收件人地理分布（{len(data_provinces)} 个省份 · {total} 人）",
             fontsize=18, fontweight="bold", color="#0b0b0b", y=0.98)

# ============================================================
# 8. 导出
# ============================================================
fig.savefig("china_province_map.pdf", format="pdf", facecolor=C_BG, edgecolor="none", dpi=200)
fig.savefig("china_province_map.png", format="png", facecolor=C_BG, edgecolor="none", dpi=200)
plt.close(fig)

print(f"✓ 已生成 china_province_map.pdf")
print(f"✓ 已生成 china_province_map.png")
