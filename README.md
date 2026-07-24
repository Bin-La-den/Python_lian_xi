# Python 练习

Python 数据分析与可视化练习项目，涵盖数据统计、地理信息可视化、科学绘图等。

## 项目结构

```
Python_lian_xi/
├── analyze_data.py          # 省份数据统计 → 柱状图
├── map_china.py             # 中国地图标注（Albers 投影 + 南海附图）
├── plot_line_chart.py       # 电池状态折线图
├── A.py                     # 系统信息采集
├── B.py                     # 线性回归示例
├── data.xlsx                # 省份收件人数据
├── Test.xlsx / Test2.xlsx   # 测试数据
├── environment.yml          # Conda 环境配置
└── .github/workflows/       # GitHub Actions 自动生成 CHANGELOG
```

## 环境配置

```bash
# 创建 conda 环境
conda env create -f environment.yml

# 激活环境
conda activate ml_env
```

主要依赖：Python 3.12、NumPy、Matplotlib、Pandas、scikit-learn

## 各脚本说明

### analyze_data.py — 省份数据统计

读取 `data.xlsx` 中的收件人省份数据，按省份统计数量，生成横向柱状图。

```bash
python analyze_data.py
```

输出：`province_bar.png`

### map_china.py — 中国地图可视化

从阿里云 DataV 获取中国 GeoJSON 数据，使用 Albers 等面积圆锥投影（中国地图标准投影），在地图上标注数据覆盖的省份，包含南海诸岛附图。

```bash
python map_china.py
```

输出：`china_province_map.pdf`、`china_province_map.png`

### plot_line_chart.py — 电池状态折线图

读取 `Test2.xlsx`，以电压为自变量，四组电池状态数据为因变量，绘制多系列折线图。

```bash
python plot_line_chart.py
```

输出：`电池状态折线图.pdf`

### B.py — 线性回归

使用 scikit-learn 生成模拟数据、训练线性回归模型并进行可视化。

```bash
python B.py
```

输出：`线性回归结果.pdf`

### A.py — 系统信息采集

采集当前运行环境的系统信息（OS、Python 路径、CPU 等），输出到文本文件。

## 变更日志

每次 push 后由 GitHub Actions 自动更新，详见 [CHANGELOG.md](./CHANGELOG.md)。
