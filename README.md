# Python 练习

Python 数据分析与可视化练习项目，涵盖科学绘图、机器学习、系统信息采集等。

## 项目结构

```
Python_lian_xi/
├── A.py                     # 系统信息采集
├── B.py                     # 线性回归示例
├── test.ipynb               # 正弦曲线噪声可视化练习
├── plot_line_chart.ipynb    # 电池状态折线图
├── data.xlsx                # 省份收件人数据
├── Test.xlsx / Test2.xlsx   # 测试数据
├── output_Fedora.txt        # A.py 在 Fedora/Linux 下的输出
├── output_Windows.txt       # A.py 在 Windows 下的输出
├── CHANGELOG.md             # 变更日志
└── .github/workflows/       # GitHub Actions 自动生成 CHANGELOG
```

## 环境配置

使用 conda（miniforge3）环境 `ml_env`，Python 3.12：

```bash
# 激活环境
conda activate ml_env

# 安装依赖
pip install numpy matplotlib pandas scikit-learn py-cpuinfo jupyter
```

主要依赖：Python 3.12、NumPy、Matplotlib、Pandas、scikit-learn、py-cpuinfo、Jupyter

## 各脚本说明

### A.py — 系统信息采集

采集当前运行环境的系统信息（Python 路径、操作系统、CPU 信息等），写入文本文件。通过注释切换输出文件名：

```bash
python A.py
```

输出：`output_Fedora.txt`（Linux）或 `output_Windows.txt`（Windows，需取消代码中的注释切换）

### B.py — 线性回归

使用 scikit-learn 生成模拟数据、训练线性回归模型，输出截距、系数、MSE、R² 等评估指标并绘制拟合结果。

```bash
python B.py
```

输出：`线性回归结果.pdf`

> 注意：`B.py` 中保存路径为 Windows 硬编码路径（`C:\Python_lian_xi\`），在 Linux 下运行会报错，需改为相对路径。

### test.ipynb — 正弦曲线可视化练习

生成带噪声的正弦数据，用散点图展示观测数据与真实规律（y = sin(x)）的对比，练习 Matplotlib 绘图与中文字体配置。

### plot_line_chart.ipynb — 电池状态折线图

读取 `Test2.xlsx`，以电压为自变量，四组电池状态数据为因变量，绘制多系列折线图（遵循 dataviz 设计规范）。

## 变更日志

每次 push 后由 GitHub Actions 自动更新，详见 [CHANGELOG.md](./CHANGELOG.md)。
