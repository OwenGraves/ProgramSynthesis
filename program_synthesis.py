from z3 import *
from component import Component
from program import Program
import bit_vector_tests as BVT


# p = Program()
# p.create_increment_component()
# const = [([2], 3), ([3], 4), ([7], 8)]
# q = p.behave_constraints(const)
# w = p.solve_constraints(q)
# z = p.l_values_to_prog(w)
# print(z)

p = Program()
p.create_decrement_component()
p.create_and_component()
const = [([0b111], BVT.P1(0b111)), ([0b10100], BVT.P1(0b10100))]
q = p.behave_constraints(const)
w = p.solve_constraints(q)
z = p.l_values_to_prog(w)
print(z)
