''' Credits given to Dietrich Epp on Stack Overflow for the help in creating these
    Python equivalences of C(language)'s srand48() and drand48()
'''

'''	Generates a sequence of 48-bit integers, Xi, according the to linear congruential formula

	Xn+1 = (aXn + c) mod m, where n >= 0

	a = 0x5DEECE66D
	c = 0xB
	m = 2^48
'''

class Rand48(object):
	def __init__(self, seed):
		self.n = seed
	# Sets the high order 32-bits of Xi to the seed, and the lower 16-bits to 0x330e
	def srand48(self):
		self.n = (self.n << 16) + 0x330e
	# Stores the last 48-bit Xi and generates the Xn+1 term
	def drand48(self):
		self.n = (0x5DEECE66D * self.n + 0x0B) & (2**48 - 1)
		return self.n / 2**48