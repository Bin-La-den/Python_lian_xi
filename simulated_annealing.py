import math
import random
from typing import Callable, TypeVar

T = TypeVar("T")

def simulated_annealing(
    initial_state: T,
    energy: Callable[[T], float],
    neighbor: Callable[[T], T],
    temperature: Callable[[int], float],
    max_iter: int = 10000,
) -> tuple[T, float, list[float]]:
    """
    模拟退火算法。

    参数:
        initial_state: 初始解
        energy: 能量函数（目标函数），值越小越好
        neighbor: 邻域函数，生成当前解的一个邻近解
        temperature: 温度调度函数，输入迭代次数，返回当前温度
        max_iter: 最大迭代次数

    返回:
        (最优解, 最优能量值, 能量历史记录)
    """
    current = initial_state
    current_energy = energy(current)
    best = current
    best_energy = current_energy
    history = [current_energy]

    for i in range(max_iter):
        T = temperature(i)
        if T <= 0:
            break

        candidate = neighbor(current)
        candidate_energy = energy(candidate)
        delta = candidate_energy - current_energy

        # Metropolis 准则：如果更优则接受，否则以一定概率接受
        if delta < 0 or random.random() < math.exp(-delta / T):
            current = candidate
            current_energy = candidate_energy

            if current_energy < best_energy:
                best = current
                best_energy = current_energy

        history.append(current_energy)

    return best, best_energy, history


# ── 冷却调度 ──────────────────────────────────────────────

def exponential_cooling(start_temp: float, alpha: float) -> Callable[[int], float]:
    """指数降温：T(k) = start_temp * alpha^k"""
    return lambda k: start_temp * (alpha ** k)


def linear_cooling(start_temp: float, alpha: float) -> Callable[[int], float]:
    """线性降温：T(k) = start_temp - alpha * k"""
    return lambda k: max(start_temp - alpha * k, 0.0)


def logarithmic_cooling(start_temp: float, c: float = 1.0) -> Callable[[int], float]:
    """对数降温：T(k) = c / log(k + e)"""
    return lambda k: c / math.log(k + math.e)


# ── 示例 1：一元函数最小值 ────────────────────────────────

def demo_function_optimization():
    """求 f(x) = x^2 + 4*sin(3x) 在 [-10, 10] 上的最小值"""

    def f(x: float) -> float:
        return x ** 2 + 4 * math.sin(3 * x)

    def neighbor(x: float) -> float:
        # 在当前值附近随机扰动
        new_x = x + random.uniform(-1.0, 1.0)
        return max(-10.0, min(10.0, new_x))

    # 指数降温：初始温度 100，每步乘以 0.995
    cooling = exponential_cooling(start_temp=100.0, alpha=0.995)

    initial = random.uniform(-10, 10)
    best_x, best_val, hist = simulated_annealing(initial, f, neighbor, cooling, max_iter=2000)

    print("── 一元函数优化 ──")
    print(f"初始 x = {initial:.4f}")
    print(f"最优 x = {best_x:.6f}, f(x) = {best_val:.6f}")
    print(f"最终能量 = {hist[-1]:.6f}")


# ── 示例 2：旅行商问题 (TSP) ──────────────────────────────

def generate_cities(n: int, seed: int = 42) -> list[tuple[float, float]]:
    random.seed(seed)
    return [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(n)]


def distance(a: tuple[float, float], b: tuple[float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def route_length(route: list[int], cities: list[tuple[float, float]]) -> float:
    total = 0.0
    for i in range(len(route)):
        total += distance(cities[route[i]], cities[route[(i + 1) % len(route)]])
    return total


def demo_tsp():
    """用模拟退火求解 TSP"""
    n = 30
    cities = generate_cities(n)

    def energy(route: list[int]) -> float:
        return route_length(route, cities)

    def neighbor(route: list[int]) -> list[int]:
        new_route = route[:]
        i, j = random.sample(range(len(new_route)), 2)
        new_route[i], new_route[j] = new_route[j], new_route[i]
        return new_route

    initial = list(range(n))
    random.shuffle(initial)

    # 对数降温，初始温度与问题规模匹配
    cooling = logarithmic_cooling(start_temp=500.0, c=100.0)

    best, best_len, hist = simulated_annealing(initial, energy, neighbor, cooling, max_iter=50000)

    print("\n── 旅行商问题 (TSP) ──")
    print(f"城市数: {n}")
    print(f"初始路径长度: {route_length(initial, cities):.2f}")
    print(f"最优路径长度: {best_len:.2f}")
    print(f"改进比例: {(1 - best_len / route_length(initial, cities)) * 100:.1f}%")


if __name__ == "__main__":
    demo_function_optimization()
    demo_tsp()