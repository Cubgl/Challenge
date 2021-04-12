import sys

from PyQt5 import QtCore
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QToolBox, QLabel, QMenu, QAction, \
    QTableView, QCheckBox

from finder import Finder

SIZE_WIDTH, SIZE_HEIGHT = 800, 600


class MainWind(QDialog):
    def __init__(self, finder):
        super().__init__()
        self.setWindowTitle('Формирование теста')
        self.resize(SIZE_WIDTH, SIZE_HEIGHT)
        self.list_modules = finder.list_modules
        self.list_topics = finder.list_topics_names
        self.list_content = finder.list_topics_data
        self.setStyleSheet('font-size: 16px')
        self.list_models = [None] * len(finder.list_topics_names)

        tool_box = QToolBox()
        for i in range(len(self.list_topics)):
            self.create_table(i)
            table = QTableView(self)
            table.setModel(self.list_models[i])
            table.resizeColumnToContents(0)
            table.setColumnWidth(1, 300)
            table.setColumnWidth(2, 120)
            table.setGridStyle(QtCore.Qt.SolidLine)
            table.resizeRowsToContents()
            table.setWordWrap(True)
            tool_box.addItem(table, self.list_topics[i])
        tool_box.setCurrentIndex(0)

        self.layout = QVBoxLayout()
        self.layout.addWidget(tool_box)
        self.setLayout(self.layout)

    def create_table(self, index):
        count_rows = len(self.list_content[index])
        self.list_models[index] = QStandardItemModel(0, 3)
        for row in range(count_rows):
            item_name = QStandardItem(self.list_content[index][row])
            item_name.setCheckable(True)
            try:
                exec(f'import {self.list_modules[index]} as module')
                test_task = eval(f'module.{self.list_content[index][row]}()')
                test_task.make_task()
                example_text = test_task.generated_text
            except Exception as e:
                example_text = 'ОШИБКА при генерации задания'
            item_text = QStandardItem(example_text)
            item_answer = QStandardItem('Ответ')
            self.list_models[index].appendRow([item_name, item_text, item_answer])

        self.list_models[index].setHorizontalHeaderLabels(['Название', 'Пример задания',
                                                           'Пример ответа'])


if __name__ == '__main__':
    finder = Finder()
    print(finder.list_topics_names)
    print(finder.list_topics_data)
    app = QApplication(sys.argv)
    wnd = MainWind(finder)
    wnd.show()
    sys.exit(app.exec())
