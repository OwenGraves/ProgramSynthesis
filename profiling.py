import typing
import itertools
from constants import BV_LENGTH
from z3 import *
from program_synthesis import ProgramSynthesis
import matplotlib.pyplot as plt 
import os
import pathlib
from profiling_programs import *

def graph_data(pss: typing.List[ProgramSynthesis], filename, print_debug=None, find_shortest=None, print_components=None):
    fig, ax = plt.subplots(figsize=(1.5 * 6.4, 1.5 * 4.8))
    colors = itertools.cycle(['#66c2a5','#fc8d62','#8da0cb','#e78ac3','#a6d854','#ffd92f'])
    linestyles = itertools.cycle(['solid'] * 6 + ['dashed'] * 6 + ['dotted'] * 6)

    for ps in pss:
        if print_debug is not None:
            ps.print_debug = print_debug
        if find_shortest is not None:
            ps.find_shortest_program = find_shortest
        color, linestyle = next(colors), next(linestyles)
        p = ps.iterative_synthesis()
        if isinstance(p, str):
            print(p)
        xs = list(range(1, len(ps.timing_exit_distinct_constraint) + 1))
        ys = ps.timing_exit_solve_constraints
        y2s = ps.timing_exit_distinct_constraint

        ax.plot(sorted([x - 0.5 for x in xs] + xs), sorted(ys + y2s), label=f'{ps.name}', color=color, linestyle=linestyle)

    ax.set_xlabel('Synthesis Loop Iterations')
    ax.set_ylabel('Absolute Finish Times (s)')
    if print_components is not None:
        component_names = pss[0].program.pp_components()
    else:
        component_names = '\n'.join(ps.name + ' - ' + ps.program.pp_components() for ps in pss)
    ax.set_title(f'{filename}\n{component_names}')

    ax.plot([], [], ' ', label=f'BV_LENGTH={BV_LENGTH}')
    ax.legend(loc='best')

    fig.tight_layout()
    
    # plt.show()
    savefile = pathlib.PurePath('figures', f'{filename}.png')
    pathlib.Path(savefile.parent).mkdir(parents=True, exist_ok=True)
    plt.savefig(savefile)

def graph_several(prog_with_name, base_name, **kwargs):
    for p, name in prog_with_name:
        graph_data(p, base_name + name, **kwargs)


if __name__ == '__main__':
    # graph_data(P1through8(), 'P1 - P8', print_components=1)
    # graph_data(P1through8except3(), 'P1 - P8 no negate', print_components=1)
    # graph_data(P1through8except3(), 'P1 - P8 no negate, no find shortest', find_shortest=False, print_debug=True, print_components=1)
    # graph_data(P1_2_5_8(), 'P1,2,5-8 no negate, no xor, find shortest', find_shortest=True, print_debug=True, print_components=1)
    # graph_data(P1_2_5_8(), 'P1,2,5-8 no negate, no xor, no find shortest', find_shortest=False, print_debug=True, print_components=1)
    comp_list = [(Program.create_increment_component, 'Increment'), (Program.create_add_component, 'Add'), (Program.create_and_component, 'And'), (Program.create_xor_component, 'Xor'), (Program.create_not_component, 'Not'), (Program.create_divide_component, 'Divide')]
    # for i in range(1, 4):
    #     graph_several([(Pinc_dec_and_or(comp, i), name) for comp, name in comp_list], f'IncDecAndOr{i}/', print_debug=True, print_components=1)
    # graph_data(shortestComparison_P1(), 'ShortestComparisons/P1_0', print_debug=True)
    # graph_data(shortestComparison_P14(), 'ShortestComparisons/P14_5', print_debug=True)
    # graph_data(shortestComparison_P16(), 'ShortestComparisons/P16_1', print_debug=True)
    # graph_data(alternative_increment(), 'P1 alternative increment', print_debug=True)
    print('done')
