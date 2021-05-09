"""Таблица умножения"""

from .template import *


class Mult2(Task):
    def statement(self):
        return "{{a}} x 2 = ? "

    def calculate(self, **values_params):
        return str(values_params['a'] * 2)

    def set_constraint_params(self):
        self.params['a'] = SegmentConstraint(1, 10)


class Mult3(Task):
    def statement(self):
        return "{{a}} x 3 = ? "

    def calculate(self, **values_params):
        return str(values_params['a'] * 3)

    def set_constraint_params(self):
        self.params['a'] = SegmentConstraint(1, 10)


class Mult4(Task):
    def statement(self):
        return "{{a}} x 4 = ? "

    def calculate(self, **values_params):
        return str(values_params['a'] * 4)

    def set_constraint_params(self):
        self.params['a'] = SegmentConstraint(1, 10)


class Mult5(Task):
    def statement(self):
        return "{{a}} x 5 = ? "

    def calculate(self, **values_params):
        return str(values_params['a'] * 5)

    def set_constraint_params(self):
        self.params['a'] = SegmentConstraint(1, 10)


class Mult6(Task):
    def statement(self):
        return "{{a}} x 6 = ? "

    def calculate(self, **values_params):
        return str(values_params['a'] * 6)

    def set_constraint_params(self):
        self.params['a'] = SegmentConstraint(1, 10)


class Mult7(Task):
    def statement(self):
        return "{{a}} x 7 = ? "

    def calculate(self, **values_params):
        return str(values_params['a'] * 7)

    def set_constraint_params(self):
        self.params['a'] = SegmentConstraint(1, 10)


class Mult8(Task):
    def statement(self):
        return "{{a}} x 8 = ? "

    def calculate(self, **values_params):
        return str(values_params['a'] * 8)

    def set_constraint_params(self):
        self.params['a'] = SegmentConstraint(1, 10)


class Mult9(Task):
    def statement(self):
        return "{{a}} x 9 = ? "

    def calculate(self, **values_params):
        return str(values_params['a'] * 9)

    def set_constraint_params(self):
        self.params['a'] = SegmentConstraint(1, 10)

