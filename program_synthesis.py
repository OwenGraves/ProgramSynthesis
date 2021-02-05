from constants import BV_LENGTH
from z3 import *
from program import Program
import bit_vector_tests as BVT
from itertools import product
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
            p = program.l_values_to_prog(L).cull_unused_components()
            # "validation oracle" - only checks small values for time efficiency
            for test_input in product(range(2 ** 4), repeat=len(program.prog_inputs)):
                if p.evaluate(test_input) != oracle(*test_input):
                    return 'Components insufficient'
            return p
        a = program.get_distinct_inputs(a)
        E.append((a, oracle(*a)))
        if print_debug:
            print(E)

def timed_synthesis(program: Program, oracle, timeout=10000000, print_debug=False):
    start = timer()
    p = iterative_synthesis(program, oracle, timeout, print_debug)
    if not isinstance(p, str) and print_debug:
        print('Found:')
    print(p)
    end = timer()
    print('Time taken:', end - start)
    return p

def equal_components(num_prog_inputs, num_each_component):
    p = Program(num_prog_inputs=num_prog_inputs)
    for _ in range(num_each_component):
        p.create_increment_component()
        # p.create_decrement_component()
        # p.create_add_component()
        # p.create_subtract_component()
        # p.create_divide_component()
        p.create_and_component()
        p.create_or_component()
        # p.create_xor_component()
        # p.create_negate_component()
        p.create_not_component()
        # p.create_bitshiftright_component(1)
        # p.create_bitshiftleft_component(-1)
        # p.create_ule_component()
        # p.create_ult_component()
    return p

print('P6 program, turn on rightmost 0-bit:')
timed_synthesis(equal_components(1, 1), BVT.P6)

print('P7 program, isolate the rightmost 0-bit:')
timed_synthesis(equal_components(1, 1), BVT.P7)

print('P15 program, floor of average of inputs:')
p = Program(num_prog_inputs=2)
p.create_add_component()
p.create_and_component()
p.create_xor_component()
p.create_bitshiftright_component(1)
timed_synthesis(p, BVT.P15, 10000, True)

print('P16 program, find max:')
p = Program(num_prog_inputs=2)
p.create_xor_component()
p.create_xor_component()
p.create_negate_component()
p.create_and_component()
p.create_ule_component()
timed_synthesis(p, lambda x, y: max(x, y), 10000, False)

print('P20 program, determine if power of 2:')
p = Program()
p.create_decrement_component()
p.create_and_component()
p.create_bvredor_component()
p.create_or_component()
p.create_bitshiftright_component(BV_LENGTH - 1)
timed_synthesis(p, BVT.P20, 20000, False)