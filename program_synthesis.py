from z3 import *
from component import Component
from bit_vector_tests import BVT

s = Solver()

print(BVT.checkTest(BVT.P1, 0b1010, 0b1000))

x, y = Ints('x y')
c = Component.add([x,y], 5)
s.add(c.constraint())
print(s.check())
print(s.model())
print(s)