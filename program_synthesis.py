from z3 import *
from component import Component
from program import Program
import bit_vector_tests as BVT


s = Solver()
p = Program()
p.create_add_component()
# p.create_add_component()
# p.create_add_component()
# p.create_add_component()
constraints = p.generate_encoding_constraints()
#print(constraints)
s.add(constraints)
s.check()
print(s.model())

# s = Solver()
# p = Program()
# p.create_add_component()
# p.create_add_component()
# s.add(p.components[0].constraint())
# s.add(p.components[1].constraint())
# print(s)

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