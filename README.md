## Bit Vector Program Synthesis

Automatic bit vector program generation based on program synthesis techniques from https://susmitjha.github.io/papers/icse10.pdf.

### Running

To run, install [z3 for Python](https://github.com/Z3Prover/z3#python) then execute ```python synthesis_examples.py```.

### Examples

Synthesize a program to find the floor of the average of two inputs:
```
p = Program(num_prog_inputs=2)
p.create_add_component()
p.create_and_component()
p.create_xor_component()
p.create_bitshiftright_component(1)
iterative_synthesis(p, lambda x, y: (x + y) // 2)
```
automatically produces
```
o1 = I1 ^ I2
o2 = o1 >> 1
o3 = I1 & I2
res = o3 + o2
```

Turn on the rightmost bit of a bit vector:
```
p = Program()
p.create_increment_component()
p.create_add_component()
p.create_and_component()
p.create_or_component()
p.create_not_component()
iterative_synthesis(p, reference_implementation)
```
finds
```
o1 = I1 + 1
res = o1 | I1
```
