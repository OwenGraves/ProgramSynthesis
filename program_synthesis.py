from z3 import *
from component import Component
from program import Program
import bit_vector_tests as BVT


p = Program()
p.create_increment_component()
p.create_increment_component()
p.create_add_component()
q = p.generate_constrained_program(4, 10)
print(q)





# print(BVT.check_test(BVT.P1, 0b1000, 0b1010))
# print(BVT.eval_test(BVT.P1, 0b1010))
# print(BVT.eval_test(BVT.P2, 0b11111))
# print(BVT.check_test(BVT.P3, 0b100, 0b10100))
# print(BVT.eval_test(BVT.P15, 1, 20))
