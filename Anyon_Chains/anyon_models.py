"""
Demonstrating the use of the AnyonChain class for creation of different anyon
chain models.

Note: Fib and LeeYang are the same bar the local hamiltonian but have been kept
as seperate classes for demonstration purposes and ease of use.
"""
import logging
import itertools as it

from Anyon_Chains.anyon_chain import AnyonChain
from scipy.constants import golden

__author__ = "Klavs Riekstins"


class Fibonacci(AnyonChain):

    def __init__(self, length, periodic):
        """
        Anyon chain of fibonacci anyons

        :param length: Number of external anyons in chain
        :param periodic: If space/chain is periodic
        """
        if length < 3:
            logging.error("Chain length must be > 2, defaulting to 3")
            length = 3

        basis = self.get_states(length, periodic)
        h_local = {
            "101,101": -(golden ** (-2)),
            "010,010": -1,
            "111,111": -(golden ** (-1)),
            "101,111": -(golden ** (-3 / 2)),
            "111,101": -(golden ** (-3 / 2))
        }

        super().__init__(length, periodic, basis, h_local)

    @staticmethod
    def get_states(length, periodic):
        """
        Gets all valid states of flat chain (in ascending binary order).

        :return: Ordered flat basis for given system
        """
        if periodic:
            states = it.product([0, 1], repeat=length)
        else:
            states = it.product([0, 1], repeat=length + 1)

        valid = []
        for state in states:
            if periodic:
                tup = state + (state[0], state[1])
            else:
                tup = state

            state_str = "".join(map(str, tup))
            if "00" not in state_str:
                valid.append("".join(map(str, state)))

        return valid


class LeeYang(AnyonChain):

    def __init__(self, length, periodic):
        """
        Anyon chain of fibonacci anyons

        :param length: Number of external anyons in chain
        :param periodic: If space/chain is periodic
        """
        if length < 3:
            logging.error("Chain length must be > 2, defaulting to 3")
            length = 3

        basis = self.get_states(length, periodic)
        h_local = {
            "101,101": (golden ** 2),
            "010,010": 1,
            "111,111": -golden,
            "101,111": (1j * (golden ** (3 / 2))),
            "111,101": (1j * (golden ** (3 / 2)))
        }

        super().__init__(length, periodic, basis, h_local)

    @staticmethod
    def get_states(length, periodic):
        """
        Gets all valid states of flat chain (in ascending binary order).

        :return: Ordered flat basis for given system
        """
        if periodic:
            states = it.product([0, 1], repeat=length)
        else:
            states = it.product([0, 1], repeat=length + 1)

        valid = []
        for state in states:
            if periodic:
                tup = state + (state[0], state[1])
            else:
                tup = state

            state_str = "".join(map(str, tup))
            if "00" not in state_str:
                valid.append("".join(map(str, state)))

        return valid
