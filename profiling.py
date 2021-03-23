import typing
import itertools
from constants import BV_LENGTH
from z3 import *
from program import Program
from program_synthesis import ProgramSynthesis
import bit_vector_tests as BVT
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
        ps = ProgramSynthesis(p, BVT.Psimple, 'Simple')
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
    ax.set_ylabel('Time (s)')
    ax.set_title('Simple Benchmark')

    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(x)

    ax.legend(loc='best')
    autolabel(rects1)
    autolabel(rects2)
    fig.tight_layout()

    plt.show()
    # plt.savefig('figures/increment.png')

def graph_data(pss: typing.Union[ProgramSynthesis, typing.List[ProgramSynthesis]], name, find_shortest=True):
    if isinstance(pss, ProgramSynthesis):
        pss = [pss]

    fig, ax = plt.subplots(figsize=(1.5 * 6.4, 1.5 * 4.8))
    colors = itertools.cycle(['#66c2a5','#fc8d62','#8da0cb','#e78ac3','#a6d854','#ffd92f'])

    for ps in pss:
        color = next(colors)
        ps.find_shortest_program = find_shortest
        ps.print_debug = True
        ps.iterative_synthesis()
        x = list(map(str, range(1, len(ps.timing_exit_distinct_constraint) + 1)))
        y = ps.timing_exit_solve_constraints
        y2 = ps.timing_exit_distinct_constraint

        ax.plot(x, y, color=color, linestyle='dashed', label=f'{ps.name} Solve Constraints')
        ax.plot(x, y2, color=color, label=f'{ps.name} Exit Distinct')

    ax.set_xlabel('Synthesis Loop Iterations')
    ax.set_ylabel('Absolute Finish Times (s)')
    component_names = '\n'.join(ps.name + ' - ' + ps.program.pp_components() for ps in pss)
    ax.set_title(f'{name}\n{component_names}')

    ax.plot([], [], ' ', label=f'BV_LENGTH={BV_LENGTH}')
    ax.legend(loc='best')

    fig.tight_layout()
    
    # plt.show()
    plt.savefig(f'figures/{name}.png')

def bench_P15():
    p = Program(num_prog_inputs=2)
    p.create_add_component()
    p.create_and_component()
    p.create_xor_component()
    p.create_bitshiftright_component(1)
    return ProgramSynthesis(p, BVT.P15, 'P15')

def bench_P16():
    p = Program(num_prog_inputs=2)
    p.create_xor_component()
    p.create_xor_component()
    p.create_negate_component()
    p.create_and_component()
    p.create_ule_component()
    return ProgramSynthesis(p, BVT.P16, 'P16')

def bench_P16_2():
    p = Program(num_prog_inputs=2)
    p.create_xor_component()
    p.create_xor_component()
    p.create_negate_component()
    p.create_and_component()
    p.create_ule_component()
    return ProgramSynthesis(p, BVT.P16, 'P16_2')

if __name__ == '__main__':
    # graph_increment()
    # graph_data([bench_P15(), bench_P16(), bench_P16_2()], 'P16_Test_2')
    print('done')
