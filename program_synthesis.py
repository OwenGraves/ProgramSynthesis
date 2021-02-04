from constants import BV_LENGTH
from z3 import *
from program import Program
import bit_vector_tests as BVT
from timeit import default_timer as timer

def iterative_synthesis(program: Program, oracle, timeout=10000000, print_debug=False):
    a0 = [0] * len(program.prog_inputs)
    E = [(a0, oracle(*a0))]
    while True:
        L = program.solve_constraints(program.behave_constraints(E))
        if print_debug and L:
            print(program.l_values_to_prog(L).cull_unused_components())
        if not L:
            return 'Components insufficient'
        a = program.solve_constraints(program.distinct_constraint(E), timeout)
        if not a:
            return program.l_values_to_prog(L).cull_unused_components()
        a = program.get_distinct_inputs(a)
        E.append((a, oracle(*a)))
        if print_debug:
            print(E)

def timed_synthesis(program: Program, oracle, timeout=10000000, print_debug=False):
    start = timer()
    print(iterative_synthesis(program, oracle, timeout, print_debug))
    end = timer()
    print('Time taken:', end - start)

def equal_components(num_prog_inputs, num_each_component):
    p = Program(num_prog_inputs=num_prog_inputs)
    for _ in range(num_each_component):
        p.create_increment_component()
        p.create_decrement_component()
        p.create_add_component()
        p.create_and_component()
        p.create_xor_component()
    return p

# P15 program
# p = Program(num_prog_inputs=2)
# p.create_add_component()
# p.create_and_component()
# p.create_xor_component()
# p.create_bitshiftright_component(1)
# p.create_add_component()
# p.create_add_component()

timed_synthesis(equal_components(1, 2), BVT.P1, 10000, True)