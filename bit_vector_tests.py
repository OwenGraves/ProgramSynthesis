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

def ult(x, y):
    return simplify(If(ULT(bv(x), bv(y)), 1, 0)).as_long()

def bvredor(x):
    return simplify(BVRedOr(bv(x))).as_long()

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

def P11(x, y):
    """Test if nlz(x) < nlz(y)."""
    o1 = ~y
    o2 = x & o1
    res = ult(y, o2)
    return res

def P12(x, y):
    """Test if nlz(x) <= nlz(y)."""
    o1 = ~y
    o2 = x & o1
    res = ule(o2, y)
    return res

def P13(x):
    """Sign function."""
    o1 = bitshift(x, BV_LENGTH - 1)
    o2 = -x
    o3 = bitshift(o2, BV_LENGTH - 1)
    res = o1 | o3
    return res

def P14(x, k):
    """Round up x to a multiple of kth power of 2."""
    o1 = -1 << k
    o2 = o1 + 1
    o3 = x - o2
    res = o3 & o1
    return res

def P15(x, y):
    """Floor of average of two integers without overflowing."""
    o1 = x & y
    o2 = x ^ y
    o3 = bitshift(o2, 1)
    res = o1 + o3
    return res

def P16(x, y):
    """Compute max of two integers."""
    o1 = x ^ y
    o2 = ule(y, x)
    o3 = -o2
    o4 = o1 & o3
    res = o4 ^ y
    return res

def P17(x, y):
    """Compute min of two integers."""
    o1 = x ^ y
    o2 = ule(x, y)
    o3 = -o2
    o4 = o1 & o3
    res = o4 ^ y
    return res

def P18(x, y):
    """Ceil of average of two integers without overflowing."""
    o1 = x | y
    o2 = x ^ y
    o3 = bitshift(o2, 1)
    res = o1 - o3
    return res

def P19(x):
    """Turn off the rightmost contiguous string of 1 bits."""
    o1 = x - 1
    o2 = x | o1
    o3 = o2 + 1
    res = o3 & x
    return res

def P20(x):
    """Determine whether an integer is a power of 2.

    Equivalent to:

    def ispower2(x):
        c = str(bin(x)).count('1')
        if c == 1:
            return 0
        return 1
    """
    o1 = x - 1
    o2 = bitshift(o1, BV_LENGTH - 1)
    o3 = o1 & x
    o4 = bvredor(o3)
    res = o2 | o4
    return res

def P21(x):
    """Next higher unsigned number with same number of 1 bits.
    
    Note: Can't use 0 because of the division
    """
    o1 = -x
    o2 = x & o1
    o3 = x + o2
    o4 = x ^ o3
    o5 = o4 // o2
    o6 = bitshift(o5, 2)
    res = o6 | o3
    return res

def P22(x):
    """Round up to the next highest power of 2. (32 bit)."""
    o1 = x - 1
    o2 = bitshift(o1, 1)
    o3 = o1 | o2
    o4 = bitshift(o3, 2)
    o5 = o3 | o4
    o6 = bitshift(o5, 4)
    o7 = o5 | o6
    o8 = bitshift(o7, 8)
    o9 = o7 | o8
    o10 = bitshift(o9, 16)
    o11 = o9 | o10
    res = o11 + 1
    return res