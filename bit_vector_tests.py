from z3 import *

class BVT:
    @staticmethod
    def P1(x): # Turn-off rightmost 1 bit.
        o1 = x - 1
        res = x & o1
        return res

    @staticmethod
    def checkTest(test, input, output, input2=None):
        s = Solver()
        x = BitVecVal(input, 32)
        if input2 is not None:
            y = BitVecVal(input2, 32)
            s.add(test(x, y) == output)
        else:
            s.add(test(x) == output)
        return s.check()