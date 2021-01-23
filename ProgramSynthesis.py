from z3 import *

s = Solver()

b = BitVec('b', 16)
s.add(b == 5)
s.check()
x = s.model().get_interp(b)
print(x.as_binary_string())
