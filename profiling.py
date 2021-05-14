import typing
import itertools
from constants import BV_LENGTH
from z3 import *
from program_synthesis import ProgramSynthesis
import matplotlib.pyplot as plt 
import numpy as np
import pathlib
from profiling_programs import *

def graph_data(pss: typing.List[ProgramSynthesis], filename, print_debug=None, find_shortest=None, print_components=None):
    fig, ax = plt.subplots(figsize=(1.3*6.4, 1.1*4))
    colors = itertools.cycle(['#66c2a5','#fc8d62','#8da0cb','#e78ac3','#a6d854','#ffd92f'])
    linestyles = itertools.cycle(['solid'] * 6 + ['dashed'] * 6 + ['dotted'] * 6)
    # endings = []
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
        # endings.append(y2s[-1])

        ax.plot(sorted([x - 0.5 for x in xs] + xs), sorted(ys + y2s), label=f'{ps.name}', color=color, linestyle=linestyle)

    # print(endings)
    ax.set_xlabel('Synthesis Loop Iterations')
    ax.set_ylabel('Absolute Finish Times (s)')
    if print_components is not None:
        component_names = pss[0].program.pp_components()
    else:
        component_names = '\n'.join(ps.name + ' - ' + ps.program.pp_components() for ps in pss)
    # ax.set_title(f'{filename}\n{component_names}')

    # ax.plot([], [], ' ', label=f'BV_LENGTH={BV_LENGTH}')
    ax.legend(loc='best')

    fig.tight_layout()
    
    # plt.show()
    savefile = pathlib.PurePath('figures', f'{filename}.png')
    pathlib.Path(savefile.parent).mkdir(parents=True, exist_ok=True)
    plt.savefig(savefile)

def graph_several(prog_with_name, base_name, **kwargs):
    for p, name in prog_with_name:
        graph_data(p, base_name + name, **kwargs)

def combine_graphs():
    comp_list = [(Program.create_increment_component, 'Increment'), (Program.create_add_component, 'Add'), (Program.create_and_component, 'And'), (Program.create_xor_component, 'Xor'), (Program.create_not_component, 'Not'), (Program.create_divide_component, 'Divide')]
    psss = [(Pinc_dec_and_or(comp, 1), name) for comp, name in comp_list] # TODO change to 2

    fig, ax = plt.subplots(3, 2, figsize=(10, 11))
    coords = iter([(0, 0), (2, 0), (1, 0), (1, 1), (0, 1), (2, 1)])

    for pss, name in psss:
        px, py = next(coords)
        colors = itertools.cycle(['#66c2a5','#fc8d62','#8da0cb','#e78ac3','#a6d854','#ffd92f'])
        linestyles = itertools.cycle(['solid'] * 6 + ['dashed'] * 6 + ['dotted'] * 6)

        for ps in pss:
            ps.find_shortest_program = True
            color, linestyle = next(colors), next(linestyles)
            p = ps.iterative_synthesis()
            if isinstance(p, str):
                print(p)
            xs = list(range(1, len(ps.timing_exit_distinct_constraint) + 1))
            ys = ps.timing_exit_solve_constraints
            y2s = ps.timing_exit_distinct_constraint

            ax[px][py].plot(sorted([x - 0.5 for x in xs] + xs), sorted(ys + y2s), label=f'{ps.name}', color=color, linestyle=linestyle)
            if py == 0:
                ax[px][py].set_ylabel('Absolute Finish Times (s)')
            if px == 2:
                ax[px][py].set_xlabel('Synthesis Loop Iterations')

        # component_names = '\n'.join(ps.name + ' - ' + ps.program.pp_components() for ps in pss)
        ax[px][py].set_title(f'{name}')
        # ax[px][py].plot([], [], ' ', label=f'BV_LENGTH={BV_LENGTH}')

    ax[0][0].legend(loc='best')
    # fig.text(0.5,0, "Synthesis Loop Iterations", ha="center", va="center")
    # fig.text(0,0.5, "Absolute Finish Times (s)", ha="center", va="center", rotation=90)
    fig.tight_layout()
    
    # plt.show()
    savefile = pathlib.PurePath('figures', f'comparecomponents.png')
    pathlib.Path(savefile.parent).mkdir(parents=True, exist_ok=True)
    plt.savefig(savefile)

def create_bar_graph():
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
    x = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8']
    y = [13.148, 9.93, 12.321, 9.672, 10.847, 10.793, 10.688, 10.288]
    y2 = [10.45, 10.201, 10.084, 6.01, 9.408, 8.682, 8.654, 9.99]

    ind = np.arange(n)
    width = 0.4

    fig, ax = plt.subplots(figsize=(1.3*6.4, 1.1*4))

    rects1 = ax.bar(ind, y , width, label='Find Shortest', color='#66c2a5')
    rects2 = ax.bar(ind + width, y2, width, label='No Find Shortest', color='#fc8d62')

    ax.set_xlabel('Benchmark')
    ax.set_ylabel('Absolute Finish Times (s)')
    # ax.set_title('Simple Benchmark')

    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(x)

    ax.legend(loc='best')
    # autolabel(rects1)
    # autolabel(rects2)
    fig.tight_layout()

    savefile = pathlib.PurePath('figures', f'bargraph.png')
    pathlib.Path(savefile.parent).mkdir(parents=True, exist_ok=True)
    plt.savefig(savefile)

if __name__ == '__main__':
    # graph_data(P1through8(), 'P1 - P8', print_components=1)
    # graph_data(P1through8(), 'P1 - P8', find_shortest=False)
    # graph_data(P1through8except3(), 'P1 - P8 no negate', print_components=1)
    # graph_data(P1through8except3(), 'P1 - P8 no negate, no find shortest', find_shortest=False, print_debug=True, print_components=1)
    # graph_data(P1through8(), 'P1-8 find shortest', find_shortest=True, print_debug=True, print_components=1)
    # graph_data(P1through8(), 'P1-8 no find shortest', find_shortest=False, print_debug=True, print_components=1)
    # combine_graphs()
    # create_bar_graph()
    # graph_data(shortestComparison_P1(), 'ShortestComparisons/P1', print_debug=True)
    # graph_data(shortestComparison_P14(), 'ShortestComparisons/P14', print_debug=True)
    graph_data(shortestComparison_P16(), 'compareP16', print_debug=True)
    # graph_data(shortestComparison_P20(), 'ShortestComparisons/P20', print_debug=True)
    # graph_data(shortestComparison_P21(), 'ShortestComparisons/P21', print_debug=True)
    # graph_data(alternative_increment(), 'P1 alternative increment', print_debug=True)
    print('done')
