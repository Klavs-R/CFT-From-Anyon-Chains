import itertools as it
import numpy as np

__author__ = "Klavs Riekstins"


class FibChain:
    def __init__(self, chain_length, periodic):
        """
        Chain of fibonacci anyons of given length
        :param chain_length: Number of anyons external anyons in chain
        :param periodic: If space is periodic
        """
        self.length = chain_length
        self.periodic = periodic
        self.flat_basis = self.get_states()

    def get_states(chain):
        if chain.periodic:
            states = it.product([0, 1], repeat=chain.length)
        else:
            states = it.product([0, 1], repeat=chain.length + 1)

        valid = []
        for state in states:
            if chain.periodic:
                tup = state + (state[0], state[1])
            else:
                tup = state

            state_str = "".join([f"{i}" for i in tup])
            if "00" not in state_str:
                valid.append(state)

        return valid
