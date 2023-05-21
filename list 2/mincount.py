import hashlib
import random

import mmh3
import numpy as np
from farmhash import FarmHash128
from cityhash import CityHash128
import xxhash
from matplotlib import pyplot as plt


def min_count(k, h, multiset, bits=128):
    """
    The MinCount algorithm is a probabilistic data structure used for estimating the frequency of elements in a set.
    It works by hashing elements of the set to a fixed number of buckets and maintaining a count for each bucket.

    When a new element is added to the set, the algorithm hashes the element to determine the bucket it belongs to,
    and increments the count for that bucket. When estimating the frequency of an element, the algorithm hashes the
    element and returns the count for the corresponding bucket.

    MinCount uses a technique called stochastic averaging to improve accuracy while using a small amount of memory.
    This technique involves maintaining multiple independent counts for each bucket and taking the minimum of these
    counts as the estimate of the frequency.

    :param k: the size of the array storing hashes of selected elements
    :param h: hash function with uniform distribution
    :param multiset: multiset to analyze
    :param bits: length of hash function
    :return: estimated value of number of elements in multiset
    """
    # Initialization
    upper_bound = 2 ** bits - 1
    hash_table = [1.0] * k
    # Analyze multiset
    for x in multiset:
        hash_value = h(x) / upper_bound
        if hash_value < hash_table[k - 1] and hash_value not in hash_table:
            hash_table[k - 1] = hash_value
            hash_table.sort()

    return k - hash_table.count(1.0) if hash_table[k - 1] == 1.0 else (k - 1) / hash_table[k - 1]


def prepare_hash_function(bits=128, function="murmur"):
    hfs = {
        "sha3_256": lambda x: int(hashlib.sha3_256(bytes(x)).hexdigest(), 16),
        "murmur": lambda x: mmh3.hash128(bytes(x), signed=False),
        "xxhash": lambda x: int(xxhash.xxh128(bytes(x)).hexdigest(), 16),
        "sha1": lambda x: int(hashlib.sha1(bytes(x)).hexdigest(), 16),
        "md5": lambda x: int(hashlib.md5(bytes(x)).hexdigest(), 16),
        "farmhash": lambda x: FarmHash128(bytes(x)),
        "cityhash": lambda x: CityHash128(bytes(x)),
        "mod": lambda x: x % 2 ** (bits // 2),
    }

    def hash_function(x: int):
        return hfs[function](x) & (2 ** bits - 1)

    return hash_function


def prepare_mutlisets(multiply=1, shuffle=False):
    def prepare_multiset(n: int):
        temp_set = []
        lower_bound = int(n / 2 * (n - 1))
        upper_bound = int((n + 1) / 2 * n)
        for i in range(lower_bound, upper_bound):
            temp_set.append(i + 1)
        return random.sample(temp_set * multiply, len(temp_set * multiply)) if shuffle else temp_set * multiply

    return prepare_multiset


def task5_a(m=5, n=1000):
    h = prepare_hash_function()
    for current_m in range(1, m + 1):
        n_hat = []
        multiset = prepare_mutlisets(m)
        for trial in range(1, n + 1):
            n_hat.append(min_count(10, h, multiset(trial)))
            if trial % 100 == 0:
                print(f"m = {current_m} done in {100 * trial / n}%")
        fig, ax = plt.subplots()
        ax.plot(n_hat, label='n̂')
        ax.plot([1, n], [1, n], label='n = n̂')
        ax.set_xlabel('n')
        ax.set_ylabel('n̂')
        ax.legend()
        plt.title(f"m = {current_m}, k = 10")
        plt.show()
        fig.savefig(f"output/task 5a m = {current_m}.png")


def task5_b(n=1000):
    ks = [2, 3, 10, 100, 400]
    h = prepare_hash_function()
    for current_k in ks:
        n_hat = []
        multiset = prepare_mutlisets()
        for trial in range(1, n + 1):
            n_hat.append(min_count(current_k, h, multiset(trial)) / trial)
            if trial % 100 == 0:
                print(f"k = {current_k} done in {100 * trial / n}%")
        fig, ax = plt.subplots()
        ax.scatter([i for i, _ in enumerate(n_hat)], n_hat, label='n̂/n', marker=".")
        ax.plot([1, n], [1, 1], label='n = 1.0', color='orange')

        ax.set_xlabel('n')
        ax.set_ylabel('n̂/n')
        ax.legend()
        plt.title(f"k = {current_k}")
        plt.show()
        fig.savefig(f"output/task 5b k = {current_k}.png")


def task5_c(n=1000):
    ks = [207]
    h = prepare_hash_function()
    for current_k in ks:
        n_hat = []
        data = []
        multiset = prepare_mutlisets()
        for trial in range(1, n + 1):
            res = min_count(current_k, h, multiset(trial)) / trial
            data.append(res)
            n_hat.append(abs(res - 1) < 0.1)
            if trial % 100 == 0:
                print(f"k = {current_k} done in {100 * trial / n}%")
        print(f"k = {current_k} |n̂/n - 1| < 10% is {n_hat.count(1) / len(n_hat)} ({n_hat.count(1)}/{len(n_hat)})")

        fig, ax = plt.subplots()
        ax.scatter([i for i, _ in enumerate(data)], data, label='n̂/n', marker=".")
        ax.plot([1, n], [0.9, 0.9], label='n = 0.9', color='orange')
        ax.plot([1, n], [1.1, 1.1], label='n = 1.1', color='orange')
        ax.set_xlabel('n')
        ax.set_ylabel('n̂/n')
        ax.legend()
        plt.title(f"k = {current_k}")
        plt.show()
        fig.savefig(f"output/task 5c k = {current_k}.png")


def task6(n=1000):
    hash_functions = ['sha3_256', 'murmur', 'xxhash', 'sha1', 'md5', 'farmhash', 'cityhash', 'mod']
    hash_lengths = [8, 16, 32, 64, 96, 128]

    for h_length in hash_lengths:
        data = {key: [] for key in hash_functions}
        for h_fn in hash_functions:
            h = prepare_hash_function(h_length, h_fn)
            multiset = prepare_mutlisets()
            for trial in range(1, n + 1):
                data[h_fn].append(min_count(16, h, multiset(trial), h_length) / trial)
                if trial % 100 == 0:
                    print(f"{h_fn} done in {100 * trial / n}%")
        plot_for_task6(data, h_length, n)
        data.pop('mod')
        plot_for_task6(data, h_length, n, False)


def plot_for_task6(data, h_length, n, with_mod=True):
    fig, ax = plt.subplots()
    for alg, alg_data in data.items():
        label = f"{alg} {np.std(alg_data):.2f}"
        ax.scatter([i for i, _ in enumerate(alg_data)], alg_data, label=label, marker=".")
    ax.plot([1, n], [1, 1], color='orange')
    ax.set_xlabel('n')
    ax.set_ylabel('n̂/n')
    ax.legend()
    plt.title(f"h_length = {h_length}")
    plt.show()
    fig.savefig(f"output/task 6 h_length = {h_length}{' with mod' if with_mod else ''}.png")


def task7(n = 1000):
    # a     d
    # 0.005 0.091
    # 0.05  0.0578
    # 0.01  0.08
    alphas = [0.05]
    delta = 0.091
    k = 400
    h = prepare_hash_function()
    n_hat = {0.05: [], 0.01: [], 0.005: []}
    data = {0.05: [], 0.01: [], 0.005: []}
    for current_alpha in alphas:
        multiset = prepare_mutlisets()
        for ms_size in range(1, n + 1):
            for _ in range(1):
                res = min_count(k, h, multiset(ms_size)) / ms_size
                data[current_alpha].append(res)
                n_hat[current_alpha].append(abs(res - 1) < delta)
        print(f"α = {[current_alpha]}, |n̂/n - 1| > 1 + δ is {n_hat[current_alpha].count(1) / len(n_hat[current_alpha])} ({n_hat[current_alpha].count(1)}/{len(n_hat[current_alpha])})")
        print(f"var = {np.var(n_hat[current_alpha])}")

        fig, ax = plt.subplots()
        ax.scatter([i for i, _ in enumerate(data[current_alpha])], data[current_alpha], label='n̂/n', marker=".")
        ax.plot([1, n], [1-delta, 1-delta], label=f'n = {1-delta}', color='orange')
        ax.plot([1, n], [1+delta, 1+delta], label=f'n = {1+delta}', color='orange')
        ax.set_xlabel('n')
        ax.set_ylabel('n̂/n')
        plt.title(f"α = {[current_alpha]}, δ = {delta}")

        ax.legend()

        plt.show()

if __name__ == "__main__":
    # task5_a()
    task5_b()
    # task5_c()
    # task6()
    # task7()
