import matplotlib.pyplot as plt
import numpy as np

from environment import Environment

# CONFIG
TASK = 3
REPEAT = 1000


# Task 3
def task3():
    ev = list()
    var = list()
    for j in range(1000):
        data = list()
        for i in range(REPEAT):
            u = 100
            n = u
            env = Environment([1 / n], n=n, u=u)
            result = env.election()
            data.append(result)
        ev.append(sum([k * l for k, l in [[x, data.count(x) / REPEAT] for x in set(data)]]))
        var.append(np.var(data))

    plt.title(f"TASK 3 expected value {len(ev)} data points")
    plt.plot(ev)
    plt.hlines(y=np.array(ev).mean(), xmin=0, xmax=len(ev), linewidth=2, color='r')
    plt.show()

    plt.title(f"TASK 3 variance {len(var)} data points")
    plt.plot(var)
    plt.hlines(y=np.array(var).mean(), xmin=0, xmax=len(var), linewidth=2, color='r')
    plt.show()

    pp = np.array(ev).mean()
    p = 1 / pp

    print(pp)
    print(np.array(var).mean(), (1 - p) / (p * p))


if __name__ == '__main__':
    task3()
