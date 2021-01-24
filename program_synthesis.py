from z3 import *
from component import Component
import bit_vector_tests as BVT
from program import Program

BV_LENGTH = 32

# print(BVT.check_test(BVT.P1, 0b1000, 0b1010))
# print(BVT.eval_test(BVT.P1, 0b1010))
# print(BVT.eval_test(BVT.P2, 0b11111))
# print(BVT.check_test(BVT.P3, 0b100, 0b10100))
# print(BVT.eval_test(BVT.P15, 1, 20))

# s = Solver()

# x, y = Ints('x y')
# c = Component.add([x,y], 5)
# s.add(c.constraint())
# print(s.check())
# print(s.model())
# print(s)