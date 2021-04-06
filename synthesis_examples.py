from constants import BV_LENGTH
from z3 import *
from program import Program
from program_synthesis import ProgramSynthesis
import bit_vector_tests as BVT

def test_simple():
    p = Program()
    p.create_decrement_component()
    p.create_decrement_component()
    p.create_increment_component()
    p.create_increment_component()
    print('Simple increment program:')
    ProgramSynthesis(p, BVT.Psimple_inc, 'Simple').timed_synthesis()

def test_P6():
    print('P6 program, turn on rightmost 0-bit:')
    ProgramSynthesis(equal_components(1, 1), BVT.P6, 'P6').timed_synthesis()

def test_P7():
    print('P7 program, isolate the rightmost 0-bit:')
    ProgramSynthesis(equal_components(1, 1), BVT.P7, 'P7').timed_synthesis()

def test_P15():
    p = Program(num_prog_inputs=2)
    p.create_add_component()
    p.create_and_component()
    p.create_xor_component()
    p.create_bitshiftright_component(1)
    print('P15 program, floor of average of inputs, with debug printing:')
    ProgramSynthesis(p, BVT.P15, 'P15', timeout=20000, print_debug=True).timed_synthesis()

def test_P16():
    print('Find max program (also P16):')
    p = Program(num_prog_inputs=2)
    p.create_xor_component()
    p.create_xor_component()
    p.create_negate_component()
    p.create_and_component()
    p.create_ule_component()
    ProgramSynthesis(p, lambda x, y: max(x, y), 'Find Max').timed_synthesis()

def test_P20():
    print('P20 program, determine if power of 2:')
    p = Program()
    p.create_decrement_component()
    p.create_and_component()
    p.create_bvredor_component()
    p.create_or_component()
    p.create_bitshiftright_component(BV_LENGTH - 1)
    ProgramSynthesis(p, BVT.P20, 'P20', timeout=20000).timed_synthesis()

def test_insufficient():
    print('PSimple, testing insufficient components')
    p = Program()
    p.create_and_component()
    p.create_bvredor_component()
    p.create_ule_component()
    p.create_or_component()
    ProgramSynthesis(p, BVT.Psimple_dec, 'PSimple_insufficient').timed_synthesis()

def equal_components(num_prog_inputs, num_each_component):
    # Currently too slow to have all components at once
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

if __name__ == '__main__':
    # Run this file to see some program synthesis examples:
    test_simple()
    test_P6()
    test_P7()
    test_P15()
    test_P16()
    test_P20()
    test_insufficient()