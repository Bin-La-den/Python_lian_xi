import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 1. 定义一个更复杂的“山谷”函数 (损失函数)
# 这模拟了机器学习中寻找最优参数的过程
def surface_func(x, y):
    return (x**2 + y**2) - 10 * np.cos(2 * np.pi * x) - 10 * np.cos(2 * np.pi * y) + 20

# 2. 计算梯度：告诉 AI 每一时刻最陡的下坡方向
def gradient(x, y):
    grad_x = 2 * x + 20 * np.pi * np.sin(2 * np.pi * x)
    grad_y = 2 * y + 20 * np.pi * np.sin(2 * np.pi * y)
    return grad_x, grad_y

# 3. 初始化 AI 的起始位置
curr_x, curr_y = 0.7, 0.8  # 随机丢在半山腰
learning_rate = 0.005      # 步长：走得太快会滑出山谷，太慢则太费时
history = []

# 模拟 1000 步的学习过程
for _ in range(1000):
    history.append((curr_x, curr_y, surface_func(curr_x, curr_y)))
    gx, gy = gradient(curr_x, curr_y)
    curr_x -= learning_rate * gx
    curr_y -= learning_rate * gy

# 4. 绘图设置
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
X = np.linspace(-1, 1, 100)
Y = np.linspace(-1, 1, 100)
X, Y = np.meshgrid(X, Y)
Z = surface_func(X, Y)

# 绘制半透明的山谷背景
ax.plot_surface(X, Y, Z, cmap='terrain', alpha=0.6)
point, = ax.plot([], [], [], 'ro', markersize=10, label='AI Learner', zorder=20)
line, = ax.plot([], [], [], 'r-', linewidth=2, alpha=0.8)

ax.set_title("AI 正在实时寻找全局最优解 (梯度下降可视化)")

# 5. 动画更新函数（修复了之前的空列表解包错误）
def update(frame):
    if frame < 1: return point, line
    # 获取到当前帧为止的所有历史路径
    current_path = history[:frame+1]
    hx, hy, hz = zip(*current_path)
    
    # 更新红点位置和红线轨迹
    point.set_data([hx[-1]], [hy[-1]])
    point.set_3d_properties([hz[-1]])
    line.set_data(hx, hy)
    line.set_3d_properties(hz)
    return point, line

# 创造动画
ani = FuncAnimation(fig, update, frames=len(history), interval=50, blit=False)
plt.legend()
plt.show()