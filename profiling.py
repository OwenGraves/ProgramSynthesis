from z3 import *
import cProfile
import pstats
import synthesis_examples as se

if __name__ == '__main__':
    profiler = cProfile.Profile()
    profiler.enable()
    se.test_P16()
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.strip_dirs()
    stats.sort_stats('cumtime')
    stats.print_stats(.1)