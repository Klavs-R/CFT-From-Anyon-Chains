import numpy as np
from fibonacci import FibChain

__author__ = "Klavs Riekstins"
np.set_printoptions(precision=2)


if __name__ == "__main__":
    f_chain = FibChain(4, True)

    print(f_chain.Ham, "\n")
    print(f_chain.get_eigs())
