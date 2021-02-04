from z3 import *

# 2^BV_LENGTH needs to be larger than the number of variables
BV_LENGTH = 6

def bv(x: int):
    return BitVecVal(x, BV_LENGTH)