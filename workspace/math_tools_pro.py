import math

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

# Advanced functions
def power(a, b):
    return math.pow(a, b)

def square_root(a):
    if a < 0:
        raise ValueError("Cannot calculate square root of a negative number.")
    return math.sqrt(a)

def factorial(n):
    return math.factorial(n)

def gcd(a, b):
    return math.gcd(a, b)

def log(a, base=math.e):
    return math.log(a, base)

def calculate_primes(n):
    """Returns a list of prime numbers up to n using the Sieve of Eratosthenes."""
    if n < 2:
        return []
    primes = [True] * (n + 1)
    primes[0] = primes[1] = False
    for p in range(2, int(math.sqrt(n)) + 1):
        if primes[p]:
            for i in range(p * p, n + 1, p):
                primes[i] = False
    return [p for p in range(2, n + 1) if primes[p]]