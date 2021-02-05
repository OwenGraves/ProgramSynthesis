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

def bitshift(x, y):
    return simplify(LShR(x, bv(y))).as_long()

def ule(x, y):
    return simplify(If(ULE(bv(x), bv(y)), 1, 0)).as_long()

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

def P4(x):
    """Form a mask that identifies the rightmost 1 bit and trailing 0s."""
    o1 = x - 1
    res = x ^ o1
    return res

def P5(x):
    """Right propagate rightmost 1-bit."""
    o1 = x - 1
    res = x | o1
    return res

def P6(x):
    """Turn on the rightmost 0-bit."""
    o1 = x + 1
    res = x | o1
    return res

def P7(x):
    """Isolate the rightmost 0-bit."""
    o1 = ~x
    o2 = x + 1
    res = o1 & o2
    return res

def P8(x):
    """Form a mask that identifies the trailing 0s."""
    o1 = x - 1
    o2 = ~x
    res = o1 & o2
    return res

def P9(x):
    """Absolute value function."""
    o1 = bitshift(x, BV_LENGTH - 1)
    o2 = x ^ o1
    res = o2 - o1
    return res

def P10(x, y):
    """Test if nlz(x) == nlz(y) where nlz is number of leading zeroes."""
    o1 = x & y
    o2 = x ^ y
    res = ule(o2, o1)
    return res

def P15(x, y):
    """Floor of average of two integers without overflowing."""
    o1 = x & y
    o2 = x ^ y
    o3 = bitshift(o2, 1)
    res = o1 + o3
    return res
