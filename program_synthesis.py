from z3 import *
from component import Component
from bit_vector_tests import BVT

s = Solver()

print(BVT.check_test(BVT.P1, 0b1010, 0b1000))
print(BVT.eval_test(BVT.P1, 0b1010))
print(BVT.eval_test(BVT.P2, 0b1010))


x, y = Ints('x y')
c = Component.add([x,y], 5)
s.add(c.constraint())
print(s.check())
print(s.model())
print(s)