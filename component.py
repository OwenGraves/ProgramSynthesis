from z3 import *
import re

class Component:
    def __init__(self, inputs, output, func, func_arity):
        self.inputs = inputs
        self.output = output
        self.func = func
        self.func_arity = func_arity

    def __str__(self):
        return str(self.constraint()).replace('==', '=')

    def __lt__(self, other): # orders based on output variable number, somewhat hacky
        def extract_int_value(c):
            return int(re.split(r'\D+', str(c.output))[-1])
        return extract_int_value(self) < extract_int_value(other)

    def constraint(self):
        return self.output == self.func(*self.inputs)