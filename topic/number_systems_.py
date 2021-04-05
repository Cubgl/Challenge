from .template import Task, SegmentSymbolsConstraint


class BinToDec(Task):
    def statement(self):
        return "Переведите двоичное число {{a}} в десятичную систему счисления"

    def calculate(self, **values_params):
        return int(str(values_params['a']), base=2)

    def set_constraint_params(self):
        self.params['a'] = SegmentSymbolsConstraint(100000, 1000000, '01', '1')


class OctToDec(Task):
    def statement(self):
        return "Переведите восьмеричное число {{a}} в десятичную систему счисления"

    def calculate(self, **values_params):
        return int(str(values_params['a']), base=8)

    def set_constraint_params(self):
        self.params['a'] = SegmentSymbolsConstraint(30, 300, '01234567', '1234567')