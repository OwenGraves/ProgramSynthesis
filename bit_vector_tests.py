from z3 import *

class BVT:
    @staticmethod
    def P1(x): # Turn-off rightmost 1 bit.
        o1 = x - 1
        res = x & o1
        return res

    @staticmethod
    def P2(x): # Test whether an unsigned integer is of the form 2^n - 1
        o1 = x + 1
        res = x & o1
        return res

    @staticmethod
    def check_test(test, input, output, input2=None):
        s = Solver()
        x = BitVecVal(input, 32)
        if input2 is not None:
            y = BitVecVal(input2, 32)
            s.add(test(x, y) == output)
        else:
            s.add(test(x) == output)
        return s.check()

    @staticmethod
    def eval_test(test, input, input2=None):
        s = Solver()
        x = BitVecVal(input, 32)
        output = BitVec('output', 32)
        if input2 is not None:
            y = BitVecVal(input2, 32)
            s.add(test(x, y) == output)
        else:
            s.add(test(x) == output)
        s.check()
        return s.model()[output]