import json
import pickle
import os

import numpy as np

__author__ = "Klavs Riekstins"


class AnyonChain:

    def __init__(
            self,
            directory,
            model,
            chain_length,
            periodic,
            basis,
            h_local
    ):
        """
        Generic class for anyon chain with adjacent (nearest neighbour)
        interactions. Chain of given length, periodicity and basis with local
        hamiltonian in a dictionary format.

        :param directory: Directory where models should be saved
        :param model: Name of current model (e.g. Yang-Lee)
        :param chain_length: Number of external anyons in chain
        :param periodic: If space/chain is periodic
        :param basis: Ordered set of basis states for given chain
        :param h_local: Local hamiltonian (2 adjacent anyons) for the chain in
                        above basis formatted as a dictionary:

                        "state1,state2": H matrix position value
        """
        self.model = model
        self.length = max(3, chain_length)
        self.periodic = periodic
        self.flat_basis = basis
        self.H_local = h_local
        self.eigvals = np.array([])
        self.AllHams = []

        self.path = os.path.join(directory, f"{self.model}_{self.length}.pkl")

        if os.path.exists(self.path):
            with open(self.path, "rb") as f:
                unpickler = pickle.Unpickler(f)
                tmp = unpickler.load()

            self.eigvals = tmp["eigenvalues"]
            self.Ham = tmp["full"]

        else:
            self.AllHams = self.get_hams()
            self.Ham = sum(self.AllHams)

    def calc_h(self, pos):
        """
        Calculates a local hamiltonian at given point in the chain by
        distributing the minimal local Hamiltonian (H_basic)
        """
        size = len(self.flat_basis)
        point_h = np.zeros([size, size], dtype=complex)

        for i in range(size):
            row = self.flat_basis[i]
            head1 = row[:pos-1]
            tail1 = row[pos+2:]
            for j in range(size):
                col = self.flat_basis[j]
                head2 = col[:pos - 1]
                tail2 = col[pos+2:]
                if tail1 == tail2 and head1 == head2:
                    val = self.H_local.get(
                        f"{row[pos-1:pos+2]},{col[pos-1:pos+2]}"
                    )
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
        Wrapper to calculate all local Hamiltonians

        :return: All local Hamiltonians for chain
        """
        hams = [self.calc_h(1)]

        if self.periodic:
            hams.extend(self.__cycle_h(self.flat_basis, hams[0]))
        else:
            positions = len(self.flat_basis[0]) - 3
            for pos in range(positions):
                hams.append(self.calc_h(pos + 2))

        return hams

    def get_eigs(self, individual=False):
        """
        Gets the eigenvalues for Hamiltonian of the system (or eigenvalues for
        local Hamiltonians)

        :param individual: Find eigenvals of local Hamiltonians (True)
        :return: All eigenvals
        """
        if individual:
            vals = []
            if not self.AllHams:
                self.AllHams = self.get_hams()

            for matrix in self.AllHams:
                vals.extend(np.linalg.eigvals(matrix))
            return vals

        elif self.eigvals.size == 0:
            self.eigvals = np.linalg.eigvals(self.Ham)

        return self.eigvals

    def save(self):

        if not os.path.exists(os.path.split(self.path)[0]):
            os.mkdir(os.path.split(self.path)[0])

        if self.eigvals.size == 0:
            self.eigvals = self.get_eigs()

        tmp = {
            "eigenvalues": self.eigvals,
            "full": self.Ham
        }

        with open(self.path, "wb") as f:
            pickle.dump(tmp, f)
