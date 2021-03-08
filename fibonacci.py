import logging
import numpy as np
import itertools as it

from scipy.constants import golden

__author__ = "Klavs Riekstins"


class FibChain:
    def __init__(self, chain_length, periodic):
        """
        Chain of fibonacci anyons of given length and periodicity

        :param chain_length: Number of anyons external anyons in chain
        :param periodic: If space is periodic
        """
        if chain_length < 3:
            logging.error("Chain length must be > 2, defaulting to 3")

        self.length = max(3, chain_length)
        self.periodic = periodic
        self.flat_basis = self.get_states()
        self.H_basic = {
            "101,101": golden**(-2),
            "010,010": 1,
            "111,111": golden**(-1),
            "101,111": golden**(-3/2),
            "111,101": golden**(-3 / 2)
        }

        self.AllHams = self.get_hams()
        self.Ham = sum(self.AllHams)

    def get_states(self):
        """
        Gets all valid states of flat chain (in ascending binary order).

        :return: Ordered flat basis for given system
        """
        if self.periodic:
            states = it.product([0, 1], repeat=self.length)
        else:
            states = it.product([0, 1], repeat=self.length + 1)

        valid = []
        for state in states:
            if self.periodic:
                tup = state + (state[0], state[1])
            else:
                tup = state

            state_str = "".join(map(str, tup))
            if "00" not in state_str:
                valid.append("".join(map(str, state)))

        return valid

    def calc_h(self):
        """
        Calculates a local hamiltonian at the fist point in the chain by
        distributing calculated hamiltonian for 2-chain (H_basic)
        """
        size = len(self.flat_basis)
        point_h = np.zeros([size, size])

        for i in range(size):
            row = self.flat_basis[i]
            tail1 = row[3:]
            for j in range(size):
                col = self.flat_basis[j]
                tail2 = col[3:]
                if tail1 == tail2:
                    val = self.H_basic.get(f"{row[:3]},{col[:3]}")
                    if val:
                        point_h[i][j] = val

        return point_h

    def __cycle_h(self, basis, initial):
        """
        Cycles the basis vectors and reorders rows and columns of initial
        hamiltonian to new basis ordering (until order gets back to start)
        * Recursive: Must start with flat_basis and first point ham *

        :param basis: Ordered basis most recently used
        :return: All local Hamiltonians
        """
        final = []
        reorder = []
        cur_basis = []
        for vec in basis:
            cycle = f"{vec[-1]}{vec[:-1]}"
            cur_basis.append(cycle)
            reorder.append(self.flat_basis.index(cycle))

        if reorder == sorted(reorder):
            return []
        else:
            temp = initial[reorder, :]
            final.append(temp[:, reorder])
            final.extend(self.__cycle_h(cur_basis, initial))
            return final

    def get_hams(self):
        """
        Wrapper to calculate all local Hamiltonians for periodic chains

        :return: All local Hamiltonians for chain
        """
        if not self.periodic:
            logging.error("Hamiltonian currently only available for periodic")
            return []

        hams = [self.calc_h()]
        hams.extend(self.__cycle_h(self.flat_basis, hams[0]))
        return hams

    def get_eigs(self, individual=False):
        """
        Gets the eigenvalues for Hamiltonian of the system (or eigenvalues for
        local Hamiltonians)

        :param individual: Find eigenvals of local Hamiltonians (True)
        :return: All eigenvals
        """
        vals = []
        if individual:
            for matrix in self.AllHams:
                vals.extend(np.linalg.eigvals(matrix))
        else:
            vals = np.linalg.eigvals(self.Ham)

        return vals
