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