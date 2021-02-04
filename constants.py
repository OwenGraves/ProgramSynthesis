from z3 import *

BV_LENGTH = 5

def bv(x: int):
    return BitVecVal(x, BV_LENGTH)