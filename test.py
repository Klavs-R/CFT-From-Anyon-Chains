from fibonacci import FibChain

__author__ = "Klavs Riekstins"


if __name__ == "__main__":
    for chain_len in range(10):
        f_chain = FibChain(chain_len, False)
        print(chain_len, len(f_chain.flat_basis))
    f_chain = FibChain(3, False)
    print(*f_chain.flat_basis, sep="\n")
