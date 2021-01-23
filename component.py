import operator

class Component:
    def __init__(self, inputs, output, func):
        self.inputs = inputs
        self.output = output
        self.func = func

    def constraint(self):
        return self.output == self.func(*self.inputs)

    @classmethod
    def add(cls, inputs, output):
        return cls(inputs, output, operator.add)