import os
import re

import numpy as np
import matplotlib.pyplot as plt

import scipy
import pandas as pd


def P_Nakamoto(n, q):
    p = 1 - q
    alpha = n * q / p
    prob = 1 - sum(
        (np.power(alpha, k) * np.exp(-alpha) / np.math.factorial(k)) * (1 - np.power(q / p, (n - k))) for k in
        range(0, n))
    return prob


def P_Grunspan(n, q):
    p = 1 - q
    prob = 1 - sum(
        (np.power(p, n) * np.power(q, k) - np.power(p, k) * np.power(q, n)) * scipy.special.comb(k + n - 1, k) for k
        in range(0, n))
    return prob


def point_one():
    n_values = [1, 3, 6, 12, 24, 48]
    q_values = np.linspace(0, 0.5, 100)

    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(12, 8))

    for i, ax in enumerate(axes.flat):
        n = n_values[i]
        prob_nak_vals = [P_Nakamoto(n, q) for q in q_values]
        prob_gru_vals = [P_Grunspan(n, q) for q in q_values]

        ax.plot(q_values, prob_nak_vals, label='Nakamoto')
        ax.plot(q_values, prob_gru_vals, label='Grunspan')
        ax.set_xlabel('q')
        ax.set_ylabel('P(n, q)')
        ax.set_title(f'n = {n}')
        ax.legend()
        ax.grid()

    plt.tight_layout()
    plt.show()
    plt.savefig("plot9.1.png")


def point_two():
    prob_values = [0.001, 0.01, 0.1]
    q_values = np.linspace(0, 0.5, 100)

    fig, axes = plt.subplots(nrows=1, ncols=len(prob_values), figsize=(12, 4))

    for i, ax in enumerate(axes):
        prob = prob_values[i]
        n_values_nakamoto = []
        n_values_grunspan = []
        for q in q_values:
            n_nakamoto = 1
            n_grunspan = 1
            while P_Nakamoto(n_nakamoto, q) > prob:
                n_nakamoto += 1
            while P_Grunspan(n_grunspan, q) > prob:
                n_grunspan += 1
            n_values_nakamoto.append(n_nakamoto)
            n_values_grunspan.append(n_grunspan)

        ax.plot(q_values, n_values_nakamoto, label='Nakamoto')
        ax.plot(q_values, n_values_grunspan, label='Grunspan')
        ax.set_xlabel('q')
        ax.set_ylabel('n')
        ax.set_title(f'P(n, q) = {prob}%')
        ax.legend()
        ax.grid()

    plt.tight_layout()
    plt.show()
    plt.savefig("plot9.2.png")


def point_three():
    # Set the project directory
    project_dir = "./results"

    # Get a list of all files in the project directory
    file_list = os.listdir(project_dir)

    # Filter the files to include only CSV files matching the format "results{n}.csv"
    csv_files = [file for file in file_list if file.startswith("results") and file.endswith(".csv")]
    csv_files = sorted(csv_files, key=lambda x: int(re.search(r"results(\d+)", x).group(1)))

    print(csv_files)
    # Initialize an empty list to store the dataframes
    # Initialize an empty dictionary to store the data
    data_dict = []
    names = []

    # Read each CSV file into a dataframe and add it to the dictionary with the file name as the key
    for file in csv_files:
        pattern = r"results(\d+)\.csv"
        match = re.match(pattern, file)
        if match:
            number = int(match.group(1))

            file_path = os.path.join(project_dir, file)
            df = pd.read_csv(file_path)
            data_dict.append(df.values.tolist())
            names.append(number)

    # Now you have a list of dataframes containing the CSV data
    reshaped_data = []

    reshaped_data = [[[], []], [[], []], [[], []], [[], []], [[], []], [[], []]]
    for i, d in enumerate(data_dict):
        for j, k in enumerate(d):
            reshaped_data[i][0].append(k[0])
            reshaped_data[i][1].append(k[1])
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(12, 8))

    q_values = np.linspace(0, 0.5, 100)
    # Flatten the axes array to easily iterate over it
    for i, ax in enumerate(axes.flat):
        data = reshaped_data[i]
        prob_nak_vals = [P_Nakamoto(names[i], q) for q in q_values]
        prob_gru_vals = [P_Grunspan(names[i], q) for q in q_values]

        ax.plot(q_values, prob_nak_vals, label='Nakamoto')
        ax.plot(q_values, prob_gru_vals, label='Grunspan')
        ax.plot(data[0], data[1], label='Monte-Carlo')
        ax.set_xlabel('q')
        ax.set_ylabel('P(n, q)')
        ax.set_title(f'n = {names[i]}')
        ax.legend()
        ax.grid()

    plt.tight_layout()
    plt.show()
    plt.savefig("plot9.3.png")


if __name__ == "__main__":
    # point_one()
    # point_two()
    point_three()
