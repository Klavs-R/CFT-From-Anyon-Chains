import time
import numpy as np
from fibonacci import FibChain
from scipy.constants import golden as p

__author__ = "Klavs Riekstins"
np.set_printoptions(suppress=True, precision=3)


def speed_test(chain, times):
    start = time.perf_counter()
    for i in range(times):
        chain.calc_h()

    print(f"Avg time for {times} calc_h: "
          f"{(time.perf_counter() - start) / times}s")

    start = time.perf_counter()
    for i in range(int(np.floor(times / (len(chain.flat_basis))))):
        chain.get_hams()

    print(f"Avg time for {times} using cycles: "
          f"{(time.perf_counter() - start) / times}s")


def print_states(chain, matrix):
    vals, vecs = np.linalg.eig(matrix)

    print(f"Basis state ordering: {chain.flat_basis}\n")
    print(f"eigenvalues: {vals}\n")
    print(f"Eigenstates:\n{vecs}")


if __name__ == "__main__":
    f_chain = FibChain(3, False)

    print_states(f_chain, f_chain.AllHams[1])
    # speed_test(f_chain, 100000)
    # print(f_chain.AllHams[0], "\n")
    # print(f_chain.get_eigs())
    # print(f_chain.flat_basis)
    # print(np.linalg.eig(f_chain.AllHams[0]))




