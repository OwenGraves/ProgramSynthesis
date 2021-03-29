import typing
import itertools
from constants import BV_LENGTH
from z3 import *
from program_synthesis import ProgramSynthesis
import matplotlib.pyplot as plt 
import os
from profiling_programs import *

def graph_data(pss: typing.Union[ProgramSynthesis, typing.List[ProgramSynthesis]], name, print_debug=None, find_shortest=None):
    if isinstance(pss, ProgramSynthesis):
        pss = [pss]

    fig, ax = plt.subplots(figsize=(1.5 * 6.4, 1.5 * 4.8))
    colors = itertools.cycle(['#66c2a5','#fc8d62','#8da0cb','#e78ac3','#a6d854','#ffd92f'])

    for ps in pss:
        if print_debug is not None:
            ps.print_debug = print_debug
        if find_shortest is not None:
            ps.find_shortest_program = find_shortest
        color = next(colors)
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
    directory = 'figures'
    if not os.path.isdir(directory):
        os.makedirs(directory)  
    plt.savefig(os.path.join(directory, f'{name}.png'))

if __name__ == '__main__':
    graph_data([P15(), P16()], 'P15 vs P16')
    print('done')
