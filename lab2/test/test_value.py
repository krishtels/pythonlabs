import math

int_test = 69
float_test = 1.5
bool_test = False
none_test = None
str_test = 'Hello'

list1_test = [4, "dff", 0.01]
tuple1_test = (4, "dff", 0.01)
set1_test = {4, "dff", 0.01}
dict1_test = {'Name': 'Karina', 'Age': 19, 'MadeLab': True}

lambda_fanc = lambda a: a + 2


def simple_func(a):
    return a*a


def complex_func(a):
    return simple_func(2)*int_test+a


def math_func(a):
    return math.sin(a)


d = 4


def g():
    print(d)


def inner_func(g):
    a = math_func(g)
    return 12*a


def factorial_recursive(n):
    if n == 1:
        return n
    else:
        return n*factorial_recursive(n-1)


class Counter:
    def __init__(self):
        self.value = 0

    def inc(self):
        self.value += 1

    def dec(self):
        self.value -= 1


class DoubleCounter(Counter):
    def inc(self):
        Counter.inc(self)
        Counter.inc(self)


class Employee:
    emp_count = 0

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
        Employee.emp_count += 1

    def display_count(self):
        print('ALL employees amount: %d' % Employee.emp_count)

    def display_employee(self):
        print('Name: {}. Salary: {}'.format(self.name, self.salary))
