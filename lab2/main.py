from factory import Factory
import toml
import math

class Tree(object):
    def __init__(self, kind, height):
        self.kind = kind
        self.age = 0
        self.height = height

    def info(self):
        """ Метод вывода информации о дереве """
        print ("{} years old {}. {} meters high.".format(self.age, self.kind, self.height))

    def grow(self):
        """ Метод роста """
        self.age += 1
        self.height += 0.5

class FruitTree(Tree):
    def __init__(self, kind, height):
        # Необходимо вызвать метод инициализации родителя.
        # В Python 3.x это делается при помощи функции super()
        Tree.__init__(self, kind, height)

    def give_fruits(self):
        print ("Collected 20kg of {}s".format(self.kind))

class Counter:
    def __init__(self):
        self.value = 0

    def inc(self):
        self.value += 1

    def dec(self):
        self.value -= 1

class DoubleCounter(Counter):
    def inc(self):
        Counter.inc(self)  # явно обращаемся к методу класса предка
        Counter.inc(self)  # и передаём ссылку на экземпляр

class Employee:
    """Базовый класс для всех сотрудников"""
    emp_count = 0

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
        Employee.emp_count += 1

    def display_count(self):
        print('Всего сотрудников: %d' % Employee.emp_count)

    def display_employee(self):
        print('Имя: {}. Зарплата: {}'.format(self.name, self.salary))


d = 4
def g():
    print(d)

if __name__ == '__main__':
    serializer = Factory.create_serializer(".json")
    b = serializer.dumps(FruitTree)
    print(b)
    n = serializer.loads(b)

    #
    print(n)



