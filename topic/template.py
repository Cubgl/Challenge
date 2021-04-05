import random


class Constraint():
    def __init__(self, str_name=""):
        self.name = str_name
        self.type = type(None)

    def validate(self, value):
        return True

    def generate(self):
        return None


class SegmentConstraint(Constraint):
    def __init__(self, a, b):
        self.name = 'Ограничение на принадлежность промежутку в целом числе'
        self.type = type(int)
        self.left_bound = a
        self.right_bound = b

    def validate(self, value):
        return self.left_bound <= value <= self.right_bound

    def generate(self):
        return random.randint(self.left_bound, self.right_bound)


class SymbolsConstraint(Constraint):
    def __init__(self, symbols, for_first):
        self.name = 'Ограничение на допустимые символы в строке'
        self.type = type(str)
        self.good_symbols = symbols
        self.first_symbol = for_first

    def validate(self, value):
        if type(value) != self.type:
            value = str(value)
        for elem in value:
            if elem not in self.good_symbols:
                return False
        return True

    def generate(self, length):
        if length == 1:
            return random.choice(self.first_symbol)
        return random.choice(self.first_symbol) + ''.join(
            random.choices(self.good_symbols, k=length - 1))


class SegmentSymbolsConstraint(SymbolsConstraint, SegmentConstraint):
    def __init__(self, a, b, symbols, for_first):
        SymbolsConstraint.__init__(self, symbols, for_first)
        SegmentConstraint.__init__(self, a, b)
        self.name = 'Ограничение на принадлежность промежутку и допустимые символы в целом числе'

    def validate(self, value):
        return SymbolsConstraint.validate(self, value) and SegmentConstraint.validate(self, value)

    def generate(self):
        len_left_bound = len(str(self.left_bound))
        len_right_bound = len(str(self.right_bound))
        value = SymbolsConstraint.generate(self, random.randint(len_left_bound, len_right_bound))
        while not SegmentConstraint.validate(self, int(value)):
            value = SymbolsConstraint.generate(self, random.randint(len_left_bound, len_right_bound))
        return value


class Task:
    def __init__(self):
        self.task_image = None
        self.task_text = self.statement()
        self.params = self.get_params(self.task_text)
        self.values_params = {}
        self.good_answer = ''
        self.generate()
        self.generated_text = ""
        self.render_text()

    def set_image(self, filename):
        self.task_image = filename

    def statement(self):
        return ""

    def calculate(self, **params):
        return None

    def get_params(self, text):
        words = text.split()
        dict_params = {}
        for elem in words:
            if len(elem) > 4 and elem[:2] == '{{' and elem[-2:] == '}}':
                dict_params[elem[2:-2]] = Constraint()
        return dict_params

    def calculate_answer(self, **values):
        dict_keys_for_values = sorted(values.keys())
        dict_keys_for_params = sorted(self.params.keys())
        if dict_keys_for_params != dict_keys_for_values:
            return False  # здесь надо породить исключение
        return eval('self.calculate(**values)')

    def set_constraint_params(self):
        pass

    def generate(self):
        self.set_constraint_params()
        for key, elem in self.params.items():
            constraint = elem
            self.values_params[key] = constraint.generate()
        self.good_answer = self.calculate_answer(**self.values_params)

    def render_text(self):
        words = self.task_text.split()
        for i in range(len(words)):
            if len(words[i]) > 4 and words[i][:2] == '{{' and words[i][-2:] == '}}':
                words[i] = str(self.values_params[words[i][2:-2]])
        self.generated_text = ' '.join(words)