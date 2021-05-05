from constants import BV_LENGTH
from z3 import *
from program import Program
from itertools import product
from timeit import default_timer as timer

class ProgramSynthesis:
    def __init__(self, program: Program, oracle, name, timeout=10000000, print_debug=False):
        self.name = name
        self.program = program
        self.oracle = oracle
        self.timeout = timeout
        self.print_debug = print_debug
        self.find_shortest_program = True
        self.validation_check = False

    def reset_timings(self):
        self.timing_start = timer()
        self.timing_enter_solve_constraints = []
        self.timing_enter_distinct_constraint = []
        self.timing_exit_solve_constraints = []
        self.timing_exit_distinct_constraint = []
        self.timing_end = []

    def add_timing(self, var):
        var.append(round(timer() - self.timing_start, 3))

    def solve_constraints(self, E):
        self.add_timing(self.timing_enter_solve_constraints)
        def solve_constraints_inner(i):
            L = self.program.solve_constraints(self.program.behave_constraints(E, num_lines_to_ignore_at_end=i), self.name)
            if self.print_debug and L:
                print(self.program.l_values_to_prog(L).cull_unused_components(i))
            return L

        for i in range(0, len(self.program.components))[::-1]: # search smallest programs first
            if not self.find_shortest_program:
                i = 0
            L = solve_constraints_inner(i)
            if L:
                break
            elif i == 0:
                return None, None
        self.add_timing(self.timing_exit_solve_constraints)
        return L, i

    def distinct_constraint(self, E, i, L):
        self.add_timing(self.timing_enter_distinct_constraint)
        dist_const = self.program.distinct_constraint(E, L, num_lines_to_ignore_at_end=i)
        solve_const = self.program.solve_constraints(dist_const, self.name, self.timeout)
        self.add_timing(self.timing_exit_distinct_constraint)
        return solve_const

    def validate(self, L, i):
        p = self.program.l_values_to_prog(L).cull_unused_components(i)
        # "validation oracle" - only checks small values for time efficiency
        if self.validation_check:
            for test_input in product(range(2 ** 4), repeat=len(self.program.prog_inputs)):
                if p.evaluate(test_input) != self.oracle(*test_input):
                    return 'Components insufficient in validation'
        self.add_timing(self.timing_end)
        return p

    def iterative_synthesis(self):
        self.reset_timings()
        a0 = [0] * len(self.program.prog_inputs)
        E = [(a0, self.oracle(*a0))]
        while True:
            L, i = self.solve_constraints(E)
            if not L:
                return 'Components insufficient'
            a = self.distinct_constraint(E, i, L)
            if not a:
                return self.validate(L, i)
            a = self.program.get_distinct_inputs(a)
            E.append((a, self.oracle(*a)))
            if self.print_debug:
                print(E)

    def timed_synthesis(self):
        start = timer()
        p = self.iterative_synthesis()
        if not isinstance(p, str) and self.print_debug:
            print('Found:')
        print(p)
        end = timer()
        print('Time taken:', format(end - start, '.2f'))
        return p
