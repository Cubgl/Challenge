from .template import *


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


class DecToOct(Task):
    def statement(self):
        return "Переведите десятичное число {{a}} в восьмеричную систему счисления"

    def calculate(self, **values_params):
        return f"{values_params['a']:o}"

    def set_constraint_params(self):
        self.params['a'] = SegmentConstraint(42, 135)


class DecToBin(Task):
    def statement(self):
        return "Переведите десятичное число {{a}} в двоичную систему счисления"

    def calculate(self, **values_params):
        return f"{values_params['a']:b}"

    def set_constraint_params(self):
        self.params['a'] = SegmentConstraint(42, 95)


class DecToOtherNumberSystemWithoutLetters(Task):
    def statement(self):
        return "Переведите десятичное число {{a}} в систему счисления c основанием {{p}}"

    def calculate(self, **values_params):
        number = self.values_params['a']
        radix = self.values_params['p']
        res = ''
        while number != 0:
            res = str(number % radix) + res
            number //= radix
        return res

    def set_constraint_params(self):
        self.params['a'] = SegmentConstraint(42, 114)
        self.params['p'] = ListValuesConstraint(3, 4, 5, 6, 7, 9)


class DecToOtherNumberSystemWithLetters(Task):
    def statement(self):
        return "Переведите десятичное число {{a}} в систему счисления c основанием {{p}}"

    def _digit_to_letter(self, value_digit):
        if 0 <= value_digit <= 9:
            return str(value_digit)
        return chr(value_digit - 10 + ord('A'))

    def calculate(self, **values_params):
        number = self.values_params['a']
        radix = self.values_params['p']
        res = ''
        while number != 0:
            res = self._digit_to_letter(number % radix) + res
            number //= radix
        return res

    def set_constraint_params(self):
        self.params['a'] = SegmentConstraint(102, 314)
        self.params['p'] = ListValuesConstraint(11, 12, 13, 14, 15, 17)
