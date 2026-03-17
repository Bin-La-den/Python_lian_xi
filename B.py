import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

plt.rcParams['font.sans-serif'] = ['SimHei']   # 或 ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题

# 生成模拟数据
np.random.seed(42)
X = np.linspace(0, 10, 100).reshape(-1, 1)
true_intercept, true_slope = 1.0, 2.5
y = true_intercept + true_slope * X.ravel() + np.random.normal(scale=2.0, size=100)

# 划分训练/测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 训练模型
model = LinearRegression()
model.fit(X_train, y_train)

# 预测
y_pred = model.predict(X_test)

# 评估
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"截距: {model.intercept_:.3f}")
print(f"系数: {model.coef_[0]:.3f}")
print(f"MSE: {mse:.3f}")
print(f"R²: {r2:.3f}")

# 可视化
plt.figure(figsize=(8,5))
plt.scatter(X, y, alpha=0.6, label='数据点')
plt.plot(X, model.predict(X), color='red', linewidth=2, label='拟合线')
plt.xlabel('X')
plt.ylabel('y')
plt.legend()
plt.savefig(r'C:\Python_lian_xi\线性回归结果.pdf')
plt.show()