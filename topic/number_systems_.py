from .template import Task, SegmentSymbolsConstraint, LengthConstraint, SegmentConstraint


class BinToDec(Task):
    def statement(self):
        return "Переведите двоичное число {{a}} в десятичную систему счисления"

    def calculate(self, **values_params):
        return str(int(str(values_params['a']), base=2))

    def set_constraint_params(self):
        self.params['a'] = SegmentSymbolsConstraint(100000, 1000000, '01', '1')


class OctToDec(Task):
    def statement(self):
        return "Переведите восьмеричное число {{a}} в десятичную систему счисления"

    def calculate(self, **values_params):
        return str(int(str(values_params['a']), base=8))

    def set_constraint_params(self):
        self.params['a'] = SegmentSymbolsConstraint(30, 300, '01234567', '1234567')


class HexToDec(Task):
    def statement(self):
        return "Переведите шестнадцатеричное число {{a}} в десятичную систему счисления"

    def calculate(self, **values_params):
        return str(int(str(values_params['a']), base=16))

    def set_constraint_params(self):
        self.params['a'] = LengthConstraint(2, '0123456789ABCDEF', '123456789ABCDEF')


class DecToHex(Task):
    def statement(self):
        return "Переведите десятичное число {{a}} в шестнадцатеричную систему счисления"

    def calculate(self, **values_params):
        return f"{values_params['a']:X}"

    def set_constraint_params(self):
        self.params['a'] = SegmentConstraint(32, 255)