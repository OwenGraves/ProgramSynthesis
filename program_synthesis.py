from z3 import *
from component import Component
from program import Program
import bit_vector_tests as BVT

def iterative_synthesis(program: Program, oracle):
    a0 = [0] * len(program.prog_inputs)
    E = [(a0, oracle(*a0))]
    while True:
        L = program.solve_constraints(program.behave_constraints(E))
        if not L:
            return 'Components insufficient'
        a = program.solve_constraints(program.distinct_constraint(E))
        if not a:
            return program.l_values_to_prog(L) # TODO validation oracle check
        a = program.get_distinct_inputs(a)
        E.append((a, oracle(*a)))

p = Program(num_prog_inputs=2)
p.create_and_component()
p.create_xor_component()
p.create_bitshiftright_component(1)
p.create_add_component()
print(iterative_synthesis(p, BVT.P15))

# p = Program(num_prog_inputs=1)
# p.create_increment_component()
# const = [([7], 8)]
# q, otherp = p.distinct_constraint(const)
# # print(q)
# w = p.solve_constraints(q)
# print(w)
# z = p.l_values_to_prog(w)
# print(otherp.l_values_to_prog(w))
# print(z)

# p = Program(num_prog_inputs=2)
# p.create_increment_component()
# p.create_add_component()
# const = [([1, 2], 3), ([3, 4], 5)]
# q, otherp = p.distinct_constraint(const)
# w = p.solve_constraints(q)
# print(w)
# z = p.l_values_to_prog(w)
# print(otherp.l_values_to_prog(w))
# print(z)

# p = Program(num_prog_inputs=2)
# p.create_increment_component()
# p.create_add_component()
# const = [([1, 2], 3), ([0, 197], 198)]
# q = p.behave_constraints(const)
# w = p.solve_constraints(q)
# # print(w)
# z = p.l_values_to_prog(w)
# print(z)

# p = Program(num_prog_inputs=2)
# p.create_increment_component()
# p.create_add_component()
# const = [([1, 2], 3), ([0, 197], 1)]
# q = p.behave_constraints(const)
# w = p.solve_constraints(q)
# # print(w)
# z = p.l_values_to_prog(w)
# print(z)

# p = Program(num_prog_inputs=2)
# p.create_and_component()
# p.create_xor_component()
# p.create_bitshiftright_component(1)
# p.create_add_component()
# const = [([5, 9], BVT.P15(5, 9)), ([2, 15], BVT.P15(2, 15))]
# q = p.behave_constraints(const)
# w = p.solve_constraints(q)
# z = p.l_values_to_prog(w)
# print(z)
# print(BVT.P15(5, 9))
# print(BVT.P15(2, 15))

# p = Program()
# p.create_decrement_component()
# p.create_and_component()
# const = [([0b111], BVT.P1(0b111)), ([0b10100], BVT.P1(0b10100))]
# q = p.behave_constraints(const)
# w = p.solve_constraints(q)
# z = p.l_values_to_prog(w)
# print(z)
