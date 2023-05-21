import matplotlib.pyplot as plt
import numpy as np
import random

from environment import Environment

REPEAT = 1000
TASK = 2


def prepare_almost_optimal_p_vec(u):
    m = int(np.ceil(np.log2(u)) + 1)
    p_vec = list()
    for i in range(1, m):
        p_vec.append(1 / np.power(2, i))
    return p_vec


# Case 1: known number of nodes
def task2case1():
    u = random.randint(2, 1000)
    n = u
    env = Environment([1 / n], n=n, u=u)
    x = env.election()
    return x


# Case 2: n = 2
def task2case2():
    u = 1000
    p_vec = prepare_almost_optimal_p_vec(u)

    n = 2
    env = Environment(p_vec, n=n, u=u)
    x = env.election()
    return x


# Case 3: n = u/2
def task2case3():
    u = random.randint(2, 1000)
    p_vec = prepare_almost_optimal_p_vec(u)

    n = u / 2
    env = Environment(p_vec, n=n, u=u)
    x = env.election()
    return x


# Case 4: n = u
def task2case4():
    u = random.randint(2, 1000)
    p_vec = prepare_almost_optimal_p_vec(u)

    n = u
    env = Environment(p_vec, n=n, u=u)
    x = env.election()
    return x


# Task 2
def task2(case_number=1):
    cases = [task2case1, task2case2, task2case3, task2case4]
    data = list()
    for _ in range(REPEAT):
        result = cases[case_number - 1]()
        data.append(result)
    plt.hist(data, bins=len(set(data)))
    # SET PERCENTAGE INSTEAD OF NUMBERS
    # plt.hist(data, weights=np.ones(len(data)) / len(data))
    # plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    plt.title(f"TASK {TASK} CASE {case_number}, {REPEAT} trials")
    plt.show()


if __name__ == '__main__':
    for k in range(1, 5, 1):
        task2(int(k))
