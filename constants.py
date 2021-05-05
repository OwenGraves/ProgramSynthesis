from z3 import *

# 2^BV_LENGTH needs to be larger than the number of variables
BV_LENGTH = 6
# TODO add support for decls in distinct_constraint
USE_SOLVER_PROCESS = False # makes z3 more deterministic

def bv(x: int):
    return BitVecVal(x, BV_LENGTH)