import numpy as np

from Anyon_Chains.anyon_models import Fibonacci, LeeYang

__author__ = "Klavs Riekstins"
np.set_printoptions(suppress=True, precision=3)


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


if __name__ == "__main__":
    chain = LeeYang(10, True)
    eigenvals = chain.get_eigs()

    print_eigenvals(eigenvals, 10)

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

