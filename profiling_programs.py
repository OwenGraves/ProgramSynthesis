from constants import BV_LENGTH
from z3 import *
from program import Program
from program_synthesis import ProgramSynthesis
import bit_vector_tests as BVT

def P15():
    p = Program(num_prog_inputs=2)
    p.create_add_component()
    p.create_and_component()
    p.create_xor_component()
    p.create_bitshiftright_component(1)
    return ProgramSynthesis(p, BVT.P15, 'P15')

def P16():
    p = Program(num_prog_inputs=2)
    p.create_xor_component()
    p.create_xor_component()
    p.create_negate_component()
    p.create_and_component()
    p.create_ule_component()
    return ProgramSynthesis(p, BVT.P16, 'P16')

def P6():
    p = Program()
    p.create_increment_component()
    p.create_and_component()
    p.create_or_component()
    p.create_not_component()
    p.create_add_component()
    p.create_xor_component()
    return ProgramSynthesis(p, BVT.P6, 'P6')

def P7():
    p = Program()
    p.create_increment_component()
    p.create_and_component()
    p.create_or_component()
    p.create_not_component()
    p.create_add_component()
    p.create_xor_component()
    return ProgramSynthesis(p, BVT.P7, 'P7')

def P8_divide():
    p = Program()
    p.create_decrement_component()
    p.create_not_component()
    p.create_and_component()
    p.create_divide_component()
    p.create_divide_component()
    p.create_divide_component()
    return ProgramSynthesis(p, BVT.P8, 'P8 Divide')

def P8_increment():
    p = Program()
    p.create_decrement_component()
    p.create_not_component()
    p.create_and_component()
    p.create_increment_component()
    p.create_increment_component()
    p.create_increment_component()
    return ProgramSynthesis(p, BVT.P8, 'P8 Increment')

def P8_xor():
    p = Program()
    p.create_decrement_component()
    p.create_not_component()
    p.create_and_component()
    p.create_xor_component()
    p.create_xor_component()
    p.create_xor_component()
    return ProgramSynthesis(p, BVT.P8, 'P8 Xor')

def P8_decrement():
    p = Program()
    p.create_decrement_component()
    p.create_not_component()
    p.create_and_component()
    p.create_decrement_component()
    p.create_decrement_component()
    p.create_decrement_component()
    return ProgramSynthesis(p, BVT.P8, 'P8 Dec')

def P8_bitshiftleft1():
    p = Program()
    p.create_decrement_component()
    p.create_not_component()
    p.create_and_component()
    p.create_bitshiftleft_component(1)
    p.create_bitshiftleft_component(1)
    p.create_bitshiftleft_component(1)
    return ProgramSynthesis(p, BVT.P8, 'P8 BitShiftL1')