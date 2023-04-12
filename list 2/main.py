import hashlib
import random
import matplotlib.pyplot as plt


def hash_value(value):
    # Use a hash function to generate a 32-bit hash value for a given input value and seed
    h = hashlib.sha256()
    h.update(str(value).encode('utf-8'))
    return int(h.hexdigest(), 16)


def min_count(k, h, M):
    # Initialize the counters
    counters = [2 ** 256 - 1] * k

    # Process each element in the multiset
    for value in M:
        # Hash the value k times with different seeds
        # for i in range(k):
        #     hash_val = h(value, i)
        #     # Update the corresponding counter if the hash value has a small number of trailing zeroes
        #     counters[i] = min(counters[i], math.log(hash_val & -hash_val, 2))
        hash_val = h(value)
        if hash_val not in counters and hash_val < counters[k - 1]:
            counters[k - 1] = hash_val
            counters.sort()

    # Compute the estimate of the distinct count using the harmonic mean of the counters
    if counters[k-1] == 1.0:
        estimate = k - counters.count(1.0)
    else:
        estimate = (k - 1) / counters[k - 1]

    return estimate


def task1():
    # Generate a random multiset of size 100 with values in the range [0, 999]
    M = prepare_multi_sets()
    for Ms in M:
        for m in range(1, 5, 1):
            # Compute the actual distinct count
            actual_count = len(set(Ms))

            # Compute the estimated distinct count using MinCount with k=10
            temp_set = Ms * m
            random.shuffle(temp_set)
            estimated_count = min_count(10, hash_value, temp_set)

            print('Actual count:', actual_count)
            print('Estimated count:', estimated_count)
    print("m does not influences estimated value")


def task2():
    ks = [2, 3, 10, 100, 400]
    M = prepare_multi_sets()

    for k in ks:
        estimates = []
        n_values = []
        for Ms in M:
            # Generate a random multiset of size n with values in the range [0, n*10)
            # Compute the estimated distinct count using MinCount with the current k
            estimate = min_count(k, hash_value, Ms)
            # Store the ratio of the estimate to the actual count
            estimates.append(estimate / len(set(Ms)))
            n_values.append(len(set(Ms)))
        plt.plot(n_values, estimates, label=f'k={k}')

    plt.xlabel('n')
    plt.ylabel('n_hat/n')
    plt.legend()
    # plt.show()

def task3():
    ks = [300]
    M = prepare_multi_sets()
    mean = []
    for k in ks:
        for i in range(100):
            estimates = []
            for Ms in M:
                # Compute the estimated distinct count using MinCount with the current k
                estimate = min_count(k, hash_value, Ms)
                # Store the ratio of the estimate to the actual count minus one
                estimates.append(abs((estimate / len(set(Ms)) - 1)))
            mean.append(len([1 for i in estimates if i < 0.1]) / len(estimates))
        print(f"{k}: {sum(mean) / len(mean)}")


def prepare_multi_sets():
    M = []
    counter = 1
    for k in range(1001):
        temp = []
        for _ in range(k + 1):
            temp.append(counter)
            counter += 1
        M.append(temp)
    return M


if __name__ == "__main__":
    task1()
    # task3()
