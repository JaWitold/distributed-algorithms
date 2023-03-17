import random

class Node:
    def __init__(self, i):
        self.i = i

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"Node {str(self.i)}"

    @staticmethod
    def beep(p) -> bool:
        assert (0.0 < p)
        assert (p < 1.0)
        r = random.random()
        # print(self.i, r)
        return r <= p
