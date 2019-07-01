''' Credits given to Dietrich Epp on Stack Overflow for the help in creating these
    Python equivalences of C(language)'s srand48() and drand48()
'''

# Initializer function for drand48()
def srand48(seed):
    return (seed << 16) + 0x330e

# Generates uniformly distributed psuedorandom numbers using a linear congruential algorithm
#   and 48-bit integer arithmetic (similar to Random.random(), which uses the Mersenne Twister
#   algorithm)
def drand48(value):
    return ((25214903917 * value + 11) & (2**48 - 1)) / 2**48