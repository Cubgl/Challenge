'''
Электронные таблицы
'''

from .template import *


class CalcFromIndirectInformation(Task):
    def statement(self):
        return """В электронной таблице значение формулы =СРЗНАЧ(A1:C1) равно {{a}}. 
               Чему равно значение ячейки D1, если значение формулы =СУММ(A1:D1) равно {{b}}?"""

    def calculate(self, **values_params):
        return str(self.values_params['b'] - self.values_params['a'])

    def set_constraint_params(self):
        self.params['a'] = SegmentConstraint(5, 20)
        self.params['b'] = SegmentConstraint(21, 40)


class CalcFromWithPicture(Task):
    def statement(self):
        self.task_image = PREFIX_FOR_PATH_TO_IMAGE + 'et1.JPG'
        return """Чему равно значение ячейки D3, исли в ячейку D3 введена формула =MAКС({{a}})."""

    def calculate(self, **values_params):
        data = [[1, 8, 5, 9], [9, 5, 3, 15], [7, 7, 9, None], [None, 24, 3, 6]]
        the_range = values_params['a'].split(':')
        x1, y1 = int(the_range[0][1]) - 1, ord(the_range[0][0]) - ord('A')
        x2, y2 = int(the_range[1][1]) - 1, ord(the_range[1][0]) - ord('A')
        maxi = data[x1][y1]
        for r in range(x1, x2 + 1):
            for c in range(y1, y2 + 1):
                if data[r][c] > maxi:
                    maxi = data[r][c]
        return str(maxi)

    def set_constraint_params(self):
        self.params['a'] = ListConstraint('A1:C3', 'A1:C1', 'B1:C4', 'A1:B3', 'B1:D2', 'A2:C3')
