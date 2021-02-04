from z3 import *
from constants import BV_LENGTH, bv

def check_test(test, input, output):
    if not isinstance(input, list):
        input = [input]
    s = Solver()
    bv_inputs = [BitVecVal(i, BV_LENGTH) for i in input]
    s.add(test(*bv_inputs) == output)
    return s.check() # s.model()[output]

def eval_test(test, input):
    output = BitVec('output', BV_LENGTH)
    return check_test(test, input, output)

def Psimple(x):
    """Increment."""
    res = x + 1
    return res

def P1(x):
    """Turn-off rightmost 1 bit."""
    o1 = x - 1
    res = x & o1
    return res

def P2(x):
    """Test whether an unsigned integer is of the form 2^n - 1, returns 0 if yes."""
    o1 = x + 1
    res = x & o1
    return res

def P3(x):
    """Isolate the rightmost 1-bit."""
    o1 = -x
    res = x & o1
    return res

# TODO figure out bitwise inequalities?
def P10(x, y):
    """Test if nlz(x) == nlz(y) where nlz is number of leading zeroes."""
    o1 = x & y
    o2 = x ^ y
    res = o2 <= o1 # error
    return res

def P15(x, y):
    """Floor of average of two integers without overflowing."""
    o1 = x & y
    o2 = x ^ y
    o3 = simplify(LShR(o2, bv(1))).as_long()
    res = o1 + o3
    return res
