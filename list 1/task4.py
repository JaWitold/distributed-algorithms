import numpy as np
import matplotlib.pyplot as plt

from environment import Environment

# CONFIG
TASK = 4
REPEAT = 10000


def prepare_almost_optimal_p_vec(u):
    m = int(np.ceil(np.log2(u)) + 1)
    p_vec = list()
    for i in range(1, m):
        p_vec.append(1 / np.power(2, i))
    return p_vec


def experiment(i):
    u = 1000
    n = i
    p_vec = prepare_almost_optimal_p_vec(u)
    env = Environment(p_vec, n=n, u=u)
    res = env.election()
    # print(len(p_vec), res)
    return res <= len(p_vec)


# Task 4
def task4():
    ev = list()
    var = list()
    for j in range(100):
        data = list()
        for i in range(REPEAT):
            data.append(experiment(i))
        ev.append(sum([k * l for k, l in [[x, data.count(x) / REPEAT] for x in set(data)]]))
        var.append(np.var(data))
    plt.plot(ev)
    plt.show()
    plt.plot(var)
    plt.show()
    print(np.array(ev).mean())
    print(f"min: {np.min(np.array(ev))}")


if __name__ == '__main__':
    task4()
