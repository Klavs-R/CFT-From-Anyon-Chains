import numpy as np
import matplotlib.pyplot as plt
import os
import json
import math
import time

from Anyon_Chains.anyon_models import Fibonacci, YangLee

__author__ = "Klavs Riekstins"
np.set_printoptions(suppress=True, precision=3)
plt.style.use('ggplot')


def print_states(chain, matrix):
    vals, vecs = np.linalg.eig(matrix)

    print(f"Basis state ordering: {chain.flat_basis}\n")
    print(f"eigenvalues: {vals}\n")
    print(f"Eigenstates:\n{vecs}")


def print_eigenvals(vals, precision, imaginary=False):

    if imaginary:
        print("Im(eigenvalues):")
        print(*[round(val.imag, precision) for val in vals],
              sep="\n")
    else:
        print("Re(eigenvalues)")
        new_vals = [round(val.real, precision) for val in vals]
        new_vals.sort()

        new_vals += -new_vals[1]
        new_vals *= -(0.4/new_vals[0])
        print(*new_vals, sep="\n")


def accuracy(test_range=15):
    full_calculated = [-0.4, 0, 0.6, 0.6, 1.6, 1.6, 1.6, 2, 2, 2.6, 2.6, 2.6, 2.6, 3, 3, 3.6, 3.6, 3.6, 3.6, 3.6, 3.6,
                       3.6, 4, 4, 4, 4.6, 4.6, 4.6, 4.6, 4.6, 4.6, 4.6, 4.6, 4.6, 4.6, 5, 5, 5, 5, 5.6, 5.6, 5.6, 5.6,
                       5.6, 5.6, 5.6, 5.6, 5.6, 5.6, 5.6, 5.6, 5.6, 5.6, 5.6, 6, 6, 6, 6, 6, 6, 6, 6.6, 6.6, 6.6, 6.6,
                       6.6, 6.6, 6.6, 6.6, 6.6, 6.6, 6.6, 6.6, 6.6, 6.6, 7, 7, 7, 7]

    calculated = full_calculated[:50]

    data = []
    times = []
    for length in range(3, test_range+3):
        start = time.perf_counter()
        chain = YangLee(models, length)
        chain.save()

        eigs = chain.get_eigs()
        eigs.sort()

        eigs += -eigs[1]
        eigs *= -(0.4/eigs[0])

        times.append(time.perf_counter() - start)

        vars = []
        for i in range(len(calculated)-1):
            if i < len(eigs):
                vars.append((eigs[i].real - calculated[i])**2)
            else:
                vars.append(calculated[i]**2)

        data.append(sum(vars)/len(calculated))

    return data, times


if __name__ == "__main__":

    direct = os.getcwd()

    # lengths = {"3": 7, "4": 11, "5": 18, "6": 29, "7": 47, "8": 76, "9": 123, "10": 199, "11": 322, "12": 521, "13": 843, "14": 1364, "15": 2207, "16": 3571, "17": 5778}
    # length = []
    # eigs = []
    #
    # for key in lengths.keys():
    #     length.append(int(key))
    #     eigs.append(lengths[key])

    models = os.path.join(direct, "models")
    data, times = accuracy()
    # with open(os.path.join(direct, "data.json"), "r") as f:
    #     data = json.load(f)
    #
    # with open(os.path.join(direct, "time.json"), "r") as f:
    #     times = json.load(f)

    # plt.plot(length, eigs)
    # plt.ylabel("Number of eigenvalues")
    # plt.xlabel("Chain length")
    # plt.show()

    plt.plot(range(9, 18), np.sqrt(data[6:]))
    plt.ylabel("Standard deviation")
    plt.xlabel("Chain length")
    plt.show()
    #
    # plt.plot(range(3, 18), times)
    # plt.ylabel("Time/s")
    # plt.xlabel("Chain length")
    # plt.show()


    #
    # with open(os.path.join(direct, "data.json"), "w") as f:
    #     json.dump(data, f)
    #
    # with open(os.path.join(direct, "time.json"), "w") as f:
    #     json.dump(times, f)


    # fig, ax_left = plt.subplots()
    # ax_right = ax_left.twinx()
    #
    # ax_left.plot(range(6, 18), np.sqrt(data[3:]), color="red", label="Standard deviation")
    # ax_right.plot(range(6, 18), times[3:], color="blue", label="Time taken to calculate")
    # ax_left.set_ylabel("Standard deviation")
    # ax_right.set_ylabel("Time/s")
    # ax_left.set_xlabel("Chain length")
    # fig.legend(loc=(0.45, 0.7))
    # plt.show()


    #
    # chain = YangLee(models, 5, True)
    # chain.save()
    # eigenvals = chain.get_eigs()
    #
    # # print_eigenvals(eigenvals, 10)
    # eigenvals.sort()
    # for eig in eigenvals:
    #     print(eig)

# def speed_test(chain, times):
#     start = time.perf_counter()
#     for i in range(times):
#         chain.calc_h()
#
#     print(f"Avg time for {times} calc_h: "
#           f"{(time.perf_counter() - start) / times}s")
#
#     start = time.perf_counter()
#     for i in range(int(np.floor(times / (len(chain.flat_basis))))):
#         chain.get_hams()
#
#     print(f"Avg time for {times} using cycles: "
#           f"{(time.perf_counter() - start) / times}s")

