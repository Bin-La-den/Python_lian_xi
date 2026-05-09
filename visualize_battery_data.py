"""
电池放电测试数据可视化脚本
将Test.xlsx中的放电时间-电压数据可视化为多种图表
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

# 设置中文字体
rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
rcParams['axes.unicode_minus'] = False

# 读取Excel文件
file_path = 'Test.xlsx'
df = pd.read_excel(file_path)

# 数据清理和处理
print("=== 数据信息 ===")
print(f"数据形状: {df.shape}")
print(f"列名: {df.columns.tolist()}")
print("\n=== 数据预览 ===")
print(df.head())

# 获取列信息
columns = df.columns[1:].tolist()  # 获取除第一列外的列名
discharge_time = pd.to_numeric(df.iloc[:, 0], errors='coerce')

# 创建图表
fig = plt.figure(figsize=(16, 12))
fig.suptitle('电池放电测试数据可视化', fontsize=16, fontweight='bold')

# 1. 不同电流水平下的放电曲线
ax1 = plt.subplot(2, 2, 1)
for col in columns:
    voltage = pd.to_numeric(df[col], errors='coerce')
    # 只绘制非NaN值
    valid_idx = ~voltage.isna()
    ax1.plot(discharge_time[valid_idx], voltage[valid_idx], marker='', label=col, linewidth=1.5, alpha=0.7)

ax1.set_xlabel('放电时间 (分钟)', fontsize=10)
ax1.set_ylabel('电压 (V)', fontsize=10)
ax1.set_title('不同电流水平下的放电曲线', fontsize=12, fontweight='bold')
ax1.legend(loc='best', fontsize=8)
ax1.grid(True, alpha=0.3)

# 2. 各电流水平的数据点统计
ax2 = plt.subplot(2, 2, 2)
data_counts = []
current_labels = []
for col in columns:
    count = df[col].notna().sum()
    data_counts.append(count)
    current_labels.append(col)

bars = ax2.bar(range(len(current_labels)), data_counts, color='steelblue', alpha=0.7)
ax2.set_xlabel('电流水平', fontsize=10)
ax2.set_ylabel('数据点数', fontsize=10)
ax2.set_title('各电流水平的数据点统计', fontsize=12, fontweight='bold')
ax2.set_xticks(range(len(current_labels)))
ax2.set_xticklabels(current_labels, rotation=45)
ax2.grid(True, alpha=0.3, axis='y')

# 添加数值标签
for i, (bar, count) in enumerate(zip(bars, data_counts)):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20, 
             str(count), ha='center', va='bottom', fontsize=8)

# 3. 最小放电时间对比
ax3 = plt.subplot(2, 2, 3)
min_times = []
for col in columns:
    voltage = pd.to_numeric(df[col], errors='coerce')
    valid_idx = ~voltage.isna()
    if valid_idx.any():
        max_time = discharge_time[valid_idx].max()
        min_times.append(max_time)
    else:
        min_times.append(0)

bars = ax3.bar(range(len(current_labels)), min_times, color='coral', alpha=0.7)
ax3.set_xlabel('电流水平', fontsize=10)
ax3.set_ylabel('最大放电时间 (分钟)', fontsize=10)
ax3.set_title('各电流水平的最大放电时间', fontsize=12, fontweight='bold')
ax3.set_xticks(range(len(current_labels)))
ax3.set_xticklabels(current_labels, rotation=45)
ax3.grid(True, alpha=0.3, axis='y')

# 添加数值标签
for i, (bar, time) in enumerate(zip(bars, min_times)):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50, 
             f'{int(time)}', ha='center', va='bottom', fontsize=8)

# 4. 初始电压对比
ax4 = plt.subplot(2, 2, 4)
initial_voltages = []
for col in columns:
    voltage = pd.to_numeric(df[col], errors='coerce')
    valid_idx = ~voltage.isna()
    if valid_idx.any():
        initial_v = voltage[valid_idx].iloc[0]
        initial_voltages.append(initial_v)
    else:
        initial_voltages.append(0)

bars = ax4.bar(range(len(current_labels)), initial_voltages, color='lightgreen', alpha=0.7)
ax4.set_xlabel('电流水平', fontsize=10)
ax4.set_ylabel('初始电压 (V)', fontsize=10)
ax4.set_title('各电流水平的初始电压', fontsize=12, fontweight='bold')
ax4.set_xticks(range(len(current_labels)))
ax4.set_xticklabels(current_labels, rotation=45)
ax4.grid(True, alpha=0.3, axis='y')

# 添加数值标签
for i, (bar, voltage) in enumerate(zip(bars, initial_voltages)):
    ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
             f'{voltage:.2f}', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.savefig('battery_discharge_analysis.png', dpi=300, bbox_inches='tight')
print("\n=== 图表已保存 ===")
print("文件: battery_discharge_analysis.png")
plt.show()

# 生成统计总结
print("\n=== 统计总结 ===")
for i, col in enumerate(columns):
    voltage = pd.to_numeric(df[col], errors='coerce')
    valid_idx = ~voltage.isna()
    if valid_idx.any():
        print(f"\n{col}:")
        print(f"  数据点数: {valid_idx.sum()}")
        print(f"  最大放电时间: {discharge_time[valid_idx].max():.0f} 分钟")
        print(f"  初始电压: {voltage[valid_idx].iloc[0]:.4f} V")
        print(f"  最终电压: {voltage[valid_idx].iloc[-1]:.4f} V")
        print(f"  电压范围: {voltage[valid_idx].min():.4f} - {voltage[valid_idx].max():.4f} V")
