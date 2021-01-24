from z3 import *

def check_test(test, output, input, input2=None):
    s = Solver()
    x = BitVecVal(input, 32)
    if input2 is not None:
        y = BitVecVal(input2, 32)
        s.add(test(x, y) == output)
    else:
        s.add(test(x) == output)
    return s.check()

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
    o3 = o2 >> 1
    res = o1 + o3
    return res
