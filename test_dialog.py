import sys

from PyQt5 import QtCore, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QToolBox, QLabel, QMenu, QAction, \
    QTableView, QCheckBox, QLineEdit, QHBoxLayout, QScrollArea, QPushButton, QMessageBox

from finder import Finder

SIZE_WIDTH, SIZE_HEIGHT = 1200, 600


class TestDialogWind(QDialog):
    def __init__(self, finder):
        super().__init__()
        self.setWindowTitle('Формирование теста')
        self.resize(SIZE_WIDTH, SIZE_HEIGHT)
        self.list_modules = finder.list_modules
        self.list_topics = finder.list_topics_names
        self.list_content = finder.list_topics_data
        self.setStyleSheet('font-size: 16px')
        self.list_models = [None] * len(finder.list_topics_names)

        self.label_name = QLabel()
        self.label_name.setText('Название теста:')
        self.linedit_name = QLineEdit()
        self.layout_name = QHBoxLayout()
        self.layout_name.addWidget(self.label_name)
        self.layout_name.addWidget(self.linedit_name)

        self.check_random = QCheckBox()
        self.check_random.setText('Случайное перемешивание вопросов')
        self.check_study = QCheckBox()
        self.check_study.setText('Обучающий режим теста')
        self.layout_check = QHBoxLayout()
        self.layout_check.addWidget(self.check_random)
        self.layout_check.addWidget(self.check_study)

        self.table = [None] * len(self.list_topics)
        self.tool_box = QToolBox()
        for i in range(len(self.list_topics)):
            self.create_table(i)
            self.table[i] = QTableView(self)
            self.table[i].setModel(self.list_models[i])
            self.table[i].resizeColumnToContents(0)
            self.table[i].setColumnWidth(1, 100)
            self.table[i].setColumnWidth(2, 320)
            self.table[i].setColumnWidth(3, 120)
            self.table[i].setColumnWidth(4, 180)
            self.table[i].setGridStyle(QtCore.Qt.SolidLine)
            self.table[i].resizeRowsToContents()
            self.table[i].setWordWrap(True)
            self.tool_box.addItem(self.table[i], self.list_topics[i])
        self.tool_box.setCurrentIndex(0)

        self.button_save = QPushButton()
        self.button_save.setText("Сохранить")
        self.button_save.setDefault(True)
        self.button_save.clicked.connect(self.save_test)
        self.button_cancel = QPushButton()
        self.button_cancel.setText('Отмена')
        self.button_cancel.clicked.connect(self.close)
        self.layout_button = QHBoxLayout()
        self.layout_button.addWidget(self.button_save)
        self.layout_button.insertSpacing(0, SIZE_WIDTH // 3)
        self.layout_button.addWidget(self.button_cancel)
        self.layout_button.addSpacing(SIZE_WIDTH // 3)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.layout_name)
        self.layout.addLayout(self.layout_check)
        self.layout.addWidget(self.tool_box)
        self.layout.addLayout(self.layout_button)
        self.setLayout(self.layout)

        self.selected_items = {}

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

    def get_selected_items(self):
        for i in range(len(self.list_models)):
            for j in range(self.list_models[i].rowCount()):
                name_class = self.list_models[i].item(j, 0)
                count_items_this_class = self.list_models[i].item(j, 1)
                if name_class.checkState():
                    if self.list_topics[i] not in self.selected_items:
                        self.selected_items[self.list_modules[i]] =[(name_class.text(), 
                                                                    int(count_items_this_class.text()))]
                    else:
                        self.selected_items[self.list_modules[i]].append((name_class.text(), 
                                                                        int(count_items_this_class.text())))
                
    def validate(self):
        if len(self.linedit_name.text()) == 0 or self.linedit_name.text().isspace():
            QMessageBox.warning(self, 'Предупреждение', 'Введите название теста. Это поле не должно быть пустым.')
            return False
        self.get_selected_items()
        if not self.selected_items:
            QMessageBox.warning(self, 'Предупреждение', 'Не выбраны задания теста. Должно быть выбрано хотя бы одно задание.')
            return False
        return True

    def save_test(self):
        if self.validate():
            for key, value in self.selected_items.items():
                print(key, value)


if __name__ == '__main__':
    finder = Finder()
    app = QApplication(sys.argv)
    wnd = TestDialogWind(finder)
    wnd.show()
    sys.exit(app.exec())
