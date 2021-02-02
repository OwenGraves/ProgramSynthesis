from z3 import *
from component import Component
from program import Program
import bit_vector_tests as BVT


# p = Program()
# p.create_increment_component()
# p.create_increment_component()
# p.create_add_component()
# const = [([2], 4)]
# const1 = [([2], 4), ([117], 234)]
# const2 = [([2], 4), ([117], 236)]
# d = p.distinct_constraint(const)
# dw = p.solve_constraints(d)
# print(dw)
# p = Program('', 1, p.components)
# q = p.behave_constraints(const1)
# w = p.solve_constraints(q)
# z = p.l_values_to_prog(w)
# print(z)

# p = Program()
# p.create_increment_component()
# const = [([2], 3), ([3], 4), ([7], 8)]
# q = p.behave_constraints(const)
# w = p.solve_constraints(q)
# z = p.l_values_to_prog(w)
# print(z)

p = Program(num_prog_inputs=2)
p.create_and_component()
p.create_xor_component()
p.create_bitshiftright_component(1)
p.create_add_component()
const = [([5, 9], BVT.P15(5, 9)), ([2, 15], BVT.P15(2, 15))]
q = p.behave_constraints(const)
w = p.solve_constraints(q)
z = p.l_values_to_prog(w)
print(z)
print(BVT.P15(5, 9))
print(BVT.P15(2, 15))

# p = Program()
# p.create_decrement_component()
# p.create_and_component()
# const = [([0b111], BVT.P1(0b111)), ([0b10100], BVT.P1(0b10100))]
# q = p.behave_constraints(const)
# w = p.solve_constraints(q)
# z = p.l_values_to_prog(w)
# print(z)
