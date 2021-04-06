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

def first8_program():
    p = Program()
    p.create_increment_component()
    p.create_decrement_component()
    p.create_and_component()
    # p.create_negate_component()
    p.create_xor_component()
    p.create_or_component()
    p.create_not_component()
    return p

def P1through8():
    ps = []
    for p in [BVT.P1, BVT.P2, BVT.P3, BVT.P4, BVT.P5, BVT.P6, BVT.P7, BVT.P8]:
        ps.append(ProgramSynthesis(first8_program(), p, p.__name__))
    return ps

def P1through8except3():
    ps = []
    for p in [BVT.P1, BVT.P2, BVT.P4, BVT.P5, BVT.P6, BVT.P7, BVT.P8]:
        ps.append(ProgramSynthesis(first8_program(), p, p.__name__))
    return ps

def first8_program_no_xor():
    p = Program()
    p.create_increment_component()
    p.create_decrement_component()
    p.create_and_component()
    # p.create_negate_component()
    # p.create_xor_component()
    p.create_or_component()
    p.create_not_component()
    return p

def P1_2_5_8():
    ps = []
    for p in [BVT.P1, BVT.P2, BVT.P5, BVT.P6, BVT.P7, BVT.P8]:
        ps.append(ProgramSynthesis(first8_program_no_xor(), p, p.__name__))
    return ps

def inc_dec_and_or_with(comp, number):
    p = Program()
    p.create_increment_component()
    p.create_decrement_component()
    p.create_and_component()
    p.create_or_component()
    for _ in range(number):
        comp(p)
    return p

def Pinc_dec_and_or(comp, number):
    ps = []
    for p in [BVT.Psimple_inc, BVT.Psimple_dec, BVT.P1, BVT.P2, BVT.P5, BVT.P6]:
        ps.append(ProgramSynthesis(inc_dec_and_or_with(comp, number), p, p.__name__))
    return ps

def shortestComparison_P1():
    ps = []
    p = Program()
    p.create_decrement_component()
    p.create_and_component()
    p.create_xor_component()
    p.create_xor_component()
    p.create_decrement_component()
    oracle = BVT.P1
    ps_short = ProgramSynthesis(p, oracle, 'Shortest')
    ps_short.find_shortest_program = True
    ps.append(ps_short)
    ps_no_short = ProgramSynthesis(p, oracle, 'No Shortest')
    ps_no_short.find_shortest_program = False
    ps.append(ps_no_short)
    return ps

def shortestComparison_P14():
    ps = []
    p = Program(num_prog_inputs=2)
    p.create_bitshiftleft_component(-1)
    p.create_increment_component()
    p.create_subtract_component()
    p.create_and_component()
    p.create_divide_component()
    oracle = BVT.P14
    ps_short = ProgramSynthesis(p, oracle, 'Shortest')
    ps_short.find_shortest_program = True
    ps.append(ps_short)
    ps_no_short = ProgramSynthesis(p, oracle, 'No Shortest')
    ps_no_short.find_shortest_program = False
    ps.append(ps_no_short)
    return ps

def shortestComparison_P16():
    ps = []
    p = Program(num_prog_inputs=2)
    p.create_xor_component()
    p.create_xor_component()
    p.create_and_component()
    p.create_negate_component()
    p.create_ule_component()
    p.create_and_component()
    oracle = BVT.P16
    ps_short = ProgramSynthesis(p, oracle, 'Shortest')
    ps_short.find_shortest_program = True
    ps.append(ps_short)
    ps_no_short = ProgramSynthesis(p, oracle, 'No Shortest')
    ps_no_short.find_shortest_program = False
    ps.append(ps_no_short)
    return ps

def alternative_increment():
    ps = []
    p = Program(num_prog_inputs=1)
    # p.create_increment_component()
    p.create_bitshiftleft_component(1)
    p.create_bitshiftright_component(1)
    p.create_ule_component()
    p.create_ult_component()
    p.create_bvredor_component()
    p.create_and_component()
    p.create_add_component()
    oracle = BVT.Psimple_inc
    ps_short = ProgramSynthesis(p, oracle, 'P Simple')
    ps_short.find_shortest_program = True
    ps.append(ps_short)
    return ps