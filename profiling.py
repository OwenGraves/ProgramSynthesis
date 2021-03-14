from constants import BV_LENGTH
from z3 import *
from program import Program
from program_synthesis import ProgramSynthesis
import bit_vector_tests as BVT
import cProfile
import pstats
import synthesis_examples as se

def bench_increment(n, find_shortest):
    increment_timings = []
    for i in range(1, n + 1):
        p = Program()
        for _ in range(i):
            p.create_increment_component()
        # print(p.pp_components())
        ps = ProgramSynthesis(p, BVT.Psimple)
        ps.find_shortest_program = find_shortest # TODO, also do False and graph
        ps.iterative_synthesis()
        increment_timings.append(ps.timing_end[0])
    return increment_timings

def ps_P15():
    p = Program(num_prog_inputs=2)
    p.create_add_component()
    p.create_and_component()
    p.create_xor_component()
    p.create_bitshiftright_component(1)
    return ProgramSynthesis(p, BVT.P15)

if __name__ == '__main__':
    print(bench_increment(7, True))
    # profiler = cProfile.Profile()
    # profiler.enable()
    # se.test_P16()
    # profiler.disable()
    # stats = pstats.Stats(profiler)
    # stats.strip_dirs()
    # stats.sort_stats('cumtime')
    # stats.print_stats(.1)