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

