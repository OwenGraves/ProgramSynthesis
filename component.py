from z3 import *
import operator

class Component:
    def __init__(self, inputs, output, func):
        self.inputs = inputs
        self.output = output
        self.func = func

    def __str__(self):
        return str(self.constraint())

    def __lt__(self, other): # orders based on output variable number, somewhat hacky
        def extract_int_value(c):
            return int(str(c.output)[1:])
        return extract_int_value(self) < extract_int_value(other)

    def constraint(self):
        return self.output == self.func(*self.inputs)

    @classmethod
    def add(cls, inputs, output):
        return cls(inputs, output, operator.add)