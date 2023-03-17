import random

from node import Node


class Environment:
    def __init__(self, prob_vec: list, n=0, u=0):
        self.prob_Vec = prob_vec
        self.n, self.nodes = self.generate_nodes(n, u)
        # print(self.nodes, self.n)
        self.u = u

    def election(self) -> int:
        i = 0
        slot = 0
        while slot != 1:
            i += 1
            slot = 0
            for n in self.nodes:
                p = self.prob_Vec[i % len(self.prob_Vec)]
                slot += int(n.beep(p))
        return i

    @staticmethod
    def generate_nodes(n: int, u: int):
        if n == 0:
            assert u >= 2
            random.seed()
            n = int(random.randint(2, u))

        nodes = list()
        for i in range(int(n)):
            nodes.append(Node(i))
        return n, nodes
