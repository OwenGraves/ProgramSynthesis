from constants import BV_LENGTH
from z3 import *
from program import Program
from program_synthesis import timed_synthesis, equal_components
import bit_vector_tests as BVT

def test_P6():
    print('P6 program, turn on rightmost 0-bit:')
    timed_synthesis(equal_components(1, 1), BVT.P6)

def test_P7():
    print('P7 program, isolate the rightmost 0-bit:')
    timed_synthesis(equal_components(1, 1), BVT.P7)

def test_P15():
    print('P15 program, floor of average of inputs:')
    p = Program(num_prog_inputs=2)
    p.create_add_component()
    p.create_and_component()
    p.create_xor_component()
    p.create_bitshiftright_component(1)
    timed_synthesis(p, BVT.P15, 10000, True)

def test_P16():
    print('P16 program, find max:')
    p = Program(num_prog_inputs=2)
    p.create_xor_component()
    p.create_xor_component()
    p.create_negate_component()
    p.create_and_component()
    p.create_ule_component()
    timed_synthesis(p, lambda x, y: max(x, y), 10000, False)

def test_P20():
    print('P20 program, determine if power of 2:')
    p = Program()
    p.create_decrement_component()
    p.create_and_component()
    p.create_bvredor_component()
    p.create_or_component()
    p.create_bitshiftright_component(BV_LENGTH - 1)
    timed_synthesis(p, BVT.P20, 20000, False)

if __name__ == '__main__':
    test_P6()
    test_P7()
    test_P15()
    test_P16()
    test_P20()