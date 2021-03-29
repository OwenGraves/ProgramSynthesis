import typing
import itertools
from constants import BV_LENGTH
from z3 import *
from program_synthesis import ProgramSynthesis
import matplotlib.pyplot as plt 
import os
import pathlib
from profiling_programs import *

def graph_data(pss: typing.List[ProgramSynthesis], filename, print_debug=None, find_shortest=None):
    fig, ax = plt.subplots(figsize=(1.5 * 6.4, 1.5 * 4.8))
    colors = itertools.cycle(['#66c2a5','#fc8d62','#8da0cb','#e78ac3','#a6d854','#ffd92f'])
    linestyles = itertools.cycle(['solid'] * 6 + ['dashed'] * 6 + ['dotted'] * 6)

    for ps in pss:
        if print_debug is not None:
            ps.print_debug = print_debug
        if find_shortest is not None:
            ps.find_shortest_program = find_shortest
        color, linestyle = next(colors), next(linestyles)
        ps.iterative_synthesis()
        xs = list(range(1, len(ps.timing_exit_distinct_constraint) + 1))
        ys = ps.timing_exit_solve_constraints
        y2s = ps.timing_exit_distinct_constraint

        ax.plot(sorted([x - 0.5 for x in xs] + xs), sorted(ys + y2s), label=f'{ps.name}', color=color, linestyle=linestyle)

    ax.set_xlabel('Synthesis Loop Iterations')
    ax.set_ylabel('Absolute Finish Times (s)')
    component_names = '\n'.join(ps.name + ' - ' + ps.program.pp_components() for ps in pss)
    ax.set_title(f'{filename}\n{component_names}')

    ax.plot([], [], ' ', label=f'BV_LENGTH={BV_LENGTH}')
    ax.legend(loc='best')

    fig.tight_layout()
    
    # plt.show()
    savefile = pathlib.PurePath('figures', f'{filename}.png')
    pathlib.Path(savefile.parent).mkdir(parents=True, exist_ok=True)
    plt.savefig(savefile)

if __name__ == '__main__':
    graph_data([P15()], 'P15')
    print('done')
