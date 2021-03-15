from constants import BV_LENGTH
from z3 import *
from program import Program
from program_synthesis import ProgramSynthesis
import bit_vector_tests as BVT
import cProfile
import pstats
import synthesis_examples as se
import matplotlib.pyplot as plt 
import numpy as np

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

def graph_increment():
    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
    n = 8
    x = range(1, n + 1)
    y = bench_increment(n, True)
    y2 = bench_increment(n, False)

    ind = np.arange(n)
    width = 0.4
    
    fig, ax = plt.subplots(figsize=(2 * 6.4, 2 * 4.8))
    
    rects1 = ax.bar(ind, y , width, label='Find Shortest')
    rects2 = ax.bar(ind + width, y2, width, label='Don\'t Find Shortest')

    ax.set_xlabel('Number of increment components')
    ax.set_ylabel('Time')
    ax.set_title('Simple Benchmark')

    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(x)

    ax.legend(loc='best')
    autolabel(rects1)
    autolabel(rects2)
    fig.tight_layout()

    plt.show()
    # plt.savefig('figures/increment.png')

def ps_P15():
    p = Program(num_prog_inputs=2)
    p.create_add_component()
    p.create_and_component()
    p.create_xor_component()
    p.create_bitshiftright_component(1)
    return ProgramSynthesis(p, BVT.P15)

if __name__ == '__main__':
    graph_increment()
    print('done')
    # profiler = cProfile.Profile()
    # profiler.enable()
    # se.test_P16()
    # profiler.disable()
    # stats = pstats.Stats(profiler)
    # stats.strip_dirs()
    # stats.sort_stats('cumtime')
    # stats.print_stats(.1)