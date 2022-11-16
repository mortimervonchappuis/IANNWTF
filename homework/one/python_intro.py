# LISTS
# Version 1
all_squares_V1 = [i ** 2 for i in range(101) if 'cats are awesome']
odd_squares_V1 = [i ** 2 for i in range(101) if i ** 2 % 2 == 0]

# Version 2
all_squares_V2 = [i ** 2 for i in range(101)]
odd_squares_V2 = [i ** 2 for i in range(0, 101, 2)]

# Version 3
all_squares_V3 = [*map(lambda x: x**2, range(101))]
odd_squares_V3 = [*map(lambda x: x**2, range(0, 101, 2))]

# Version 3.1415926535897932384626433832
all_squares_Vpi = [sum(i for _ in range(i)) for i in range(101)]
odd_squares_Vpi = [sum(j + j for j in range(i * 2 + 1)) - i * 2 for i  in range(51)]

assert all_squares_V1 == all_squares_V2 == all_squares_V3 == all_squares_Vpi
assert odd_squares_V1 == odd_squares_V2 == odd_squares_V3 == odd_squares_Vpi


# GENERATORS
N = 4
# Version 1
def meow_V1():
	n = 1
	while True:
		yield ' '.join(['meow'] * n)
		n *= 2

# Version 2
def meow_V2(sound='meow'):
	yield sound
	for x in meow_V2(f'{sound} {sound}'):
		yield x

# Version one line
exec("meow = lambda: exec(\"\"\"try:\n\tglobals()['x']*=2\nexcept:\n\tglobals().__setitem__('x', 1)\"\"\") or ' '.join(['meow'] * x)\ndef meow_V3():\n\twhile True:\n\t\tyield meow()")


for _, a, b, c in zip(range(N), meow_V1(), meow_V2(), meow_V3()):
	assert a == b == c


# NUMPY
import numpy as np

np.random.seed(42)

x = np.random.normal(size=(5, 5))
mask = x > 0.09
x[mask] **= 2
x[~mask] = 42
print(x)
print(x[:,4])