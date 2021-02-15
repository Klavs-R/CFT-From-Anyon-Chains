import itertools as it
import numpy as np

__author__ = "Klavs Riekstins"


class FibAn:
    def __init__(self, val):
        self.val = val

    def __mul__(self, other):
        if (self.val, other.val) == (0, 0):
            return FibAn(0)
        elif {self.val, other.val} == {0, 1}:
            return FibAn(1)
        else:
            return FibAn(np.random.randint(0, 2))


class FibChain:
    def __init__(self, length, periodic=True, boundary=(1, 1)):
        """
        Chain of fibonacci anyons of given length
        :param length: Number of anyons external anyons in chain
        :param periodic: If space is periodic
        :param boundary: Boundary anyons for a bounded chain
        """
        self.length = length
        self.periodic = periodic
        self.bounds = boundary
        self.space = self.get_states()

    def get_states(chain):
        if chain.periodic:
            states = it.product([0, 1], repeat=chain.length)
        else:
            states = it.product([0, 1], repeat=chain.length - 1)

        valid = []
        for state in states:
            if chain.periodic:
                tup = state + (state[0], state[1])
            else:
                tup = (chain.bounds[0],) + state + (chain.bounds[1],)

            state_str = "".join([f"{i}" for i in tup])
            if "00" not in state_str:
                valid.append(state)

        return valid


if __name__ == "__main__":
    f_chain = FibChain(3)
    print(*f_chain.space, sep="\n")
