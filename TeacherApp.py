import sys

from PyQt5 import QtCore
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QToolBox, QLabel, QMenu, QAction, \
    QTableView, QCheckBox, QLineEdit, QHBoxLayout, QScrollArea, QPushButton

from finder import Finder

SIZE_WIDTH, SIZE_HEIGHT = 1200, 600


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

        label_name = QLabel()
        label_name.setText('Название теста:')
        linedit_name = QLineEdit()
        layout_name = QHBoxLayout()
        layout_name.addWidget(label_name)
        layout_name.addWidget(linedit_name)

        check_random = QCheckBox()
        check_random.setText('Случайное перемешивание вопросов')
        check_study = QCheckBox()
        check_study.setText('Обучающий режим теста')
        layout_check = QHBoxLayout()
        layout_check.addWidget(check_random)
        layout_check.addWidget(check_study)

        tool_box = QToolBox()
        for i in range(len(self.list_topics)):
            self.create_table(i)
            table = QTableView(self)
            table.setModel(self.list_models[i])
            table.resizeColumnToContents(0)
            table.setColumnWidth(1, 100)
            table.setColumnWidth(2, 320)
            table.setColumnWidth(3, 120)
            table.setColumnWidth(4, 180)
            table.setGridStyle(QtCore.Qt.SolidLine)
            table.resizeRowsToContents()
            table.setWordWrap(True)
            tool_box.addItem(table, self.list_topics[i])
        tool_box.setCurrentIndex(0)

        button_save = QPushButton()
        button_save.setText("Сохранить")
        button_cancel = QPushButton()
        button_cancel.setText('Забыть')
        layout_button = QHBoxLayout()
        layout_button.addWidget(button_save)
        layout_button.addWidget(button_cancel)

        self.layout = QVBoxLayout()
        self.layout.addLayout(layout_name)
        self.layout.addLayout(layout_check)
        self.layout.addWidget(tool_box)
        self.layout.addLayout(layout_button)
        self.setLayout(self.layout)

    def create_table(self, index):
        count_rows = len(self.list_content[index])
        self.list_models[index] = QStandardItemModel(0, 5)
        for row in range(count_rows):
            item_name = QStandardItem(self.list_content[index][row])
            item_name.setCheckable(True)
            item_count = QStandardItem('1')
            item_count.setEnabled(True)
            try:
                exec(f'import {self.list_modules[index]} as module')
                test_task = eval(f'module.{self.list_content[index][row]}()')
                test_task.make_task()
                example_text = test_task.generated_text
                answer_text = test_task.calculate_answer(**test_task.values_params)
                image_text = test_task.task_image
            except Exception as e:
                example_text = 'ОШИБКА при генерации задания'
            item_text = QStandardItem(example_text)
            item_answer = QStandardItem(answer_text)
            item_image = QStandardItem(image_text)
            self.list_models[index].appendRow(
                [item_name, item_count, item_text, item_answer, item_image])

            self.list_models[index].setHorizontalHeaderLabels(['Название', 'Количество',
                                                               'Пример задания', 'Пример ответа',
                                                               'Изображение'])


if __name__ == '__main__':
    finder = Finder()
    app = QApplication(sys.argv)
    wnd = MainWind(finder)
    wnd.show()
    sys.exit(app.exec())
