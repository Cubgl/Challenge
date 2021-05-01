import sys
import sqlite3
from PyQt5 import QtCore
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QToolBox, QLabel, QTableView, \
    QCheckBox, QLineEdit, QHBoxLayout, \
    QPushButton, QMessageBox

from TeacherApp.database_engine import DatabaseEngine
from TeacherApp.finder import Finder

SIZE_WIDTH, SIZE_HEIGHT = 1200, 600


class TestDialogWind(QDialog):
    def __init__(self, finder, con):
        super().__init__()
        self.setWindowTitle('Формирование теста')
        self.resize(SIZE_WIDTH, SIZE_HEIGHT)
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
            self.tool_box.addItem(self.table[i], self.list_topics[i][0])
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
        self.insert_mode = True

    def create_table(self, index):
        count_rows = len(self.list_content[index])
        self.list_models[index] = QStandardItemModel(0, 5)
        for row in range(count_rows):
            item_name = QStandardItem(self.list_content[index][row])
            item_name.setCheckable(True)
            item_name.setEditable(False)
            item_count = QStandardItem('0')
            item_count.setEnabled(True)
            try:
                exec(f'import {self.list_topics[index][1]} as module')
                test_task = eval(f'module.{self.list_content[index][row]}()')
                test_task.make_task()
                example_text = test_task.generated_text
                answer_text = test_task.calculate_answer(**test_task.values_params)
                image_text = test_task.task_image
            except Exception as e:
                example_text = 'ОШИБКА при генерации задания'
            item_text = QStandardItem(example_text)
            item_text.setEditable(False)
            item_answer = QStandardItem(answer_text)
            item_answer.setEditable(False)
            item_image = QStandardItem(image_text)
            item_image.setEditable(False)
            self.list_models[index].appendRow(
                [item_name, item_count, item_text, item_answer, item_image])

            self.list_models[index].setHorizontalHeaderLabels(['Название', 'Количество',
                                                               'Пример задания', 'Пример ответа',
                                                               'Изображение'])
        self.list_models[index].itemChanged.connect(self.change_count)

    def change_count(self, item):
        number_row = item.row()
        new_data = item.data(QtCore.Qt.EditRole)
        parent_model = item.model()
        check_field = parent_model.item(number_row, 0)
        count_field = parent_model.item(number_row, 1)
        if item is check_field:
            if check_field.checkState() == QtCore.Qt.Checked and count_field.data(
                    QtCore.Qt.EditRole) != '0':
                return
            if check_field.checkState() == QtCore.Qt.Checked and count_field.data(
                    QtCore.Qt.EditRole) == '0':
                count_field.setData('1', QtCore.Qt.EditRole)
                return
            if check_field.checkState() != QtCore.Qt.Checked and count_field.data(
                    QtCore.Qt.EditRole) != '0':
                count_field.setData('0', QtCore.Qt.EditRole)
                return
        else:
            if check_field.checkState() != QtCore.Qt.Checked and count_field.data(
                    QtCore.Qt.EditRole) != '0':
                check_field.setCheckState(QtCore.Qt.Checked)
                return
            if check_field.checkState() == QtCore.Qt.Checked and count_field.data(
                    QtCore.Qt.EditRole) == '0':
                check_field.setCheckState(QtCore.Qt.Unchecked)
                return

    def get_selected_items(self):
        for i in range(len(self.list_models)):
            name_topic = self.list_topics[i]
            for j in range(self.list_models[i].rowCount()):
                name_class = self.list_models[i].item(j, 0)
                count_items = self.list_models[i].item(j, 1)
                if name_class.checkState() == QtCore.Qt.Checked:
                    if name_topic not in self.selected_items:
                        self.selected_items[name_topic] = [(name_class.text(),
                                                            int(count_items.text()))]
                    else:
                        self.selected_items[name_topic].append((name_class.text(),
                                                                int(count_items.text())))

    def validate(self):
        if len(self.linedit_name.text()) == 0 or self.linedit_name.text().isspace():
            QMessageBox.warning(self, 'Предупреждение',
                                'Введите название теста. Это поле не должно быть пустым.')
            return False
        self.get_selected_items()
        if not self.selected_items:
            QMessageBox.warning(self, 'Предупреждение',
                                'Не выбраны задания теста. Должно быть выбрано хотя бы одно задание.')
            return False
        return True

    def save_test(self):
        if self.validate():
            if self.insert_mode:
                title_challenge = self.linedit_name.text()
                db.insert_challenge(title_challenge, self.check_random.isChecked(),
                                         self.check_study.isChecked())
                id_challenge = db.search_id_challenge(title_challenge)
                if id_challenge == -1:
                    print("Непридвиденная ошибка базы данных")
                    sys.exit(-1)
                for key, value in self.selected_items.items():
                    for elem in value:
                        db.insert_challenge_item(elem[0], id_challenge, elem[1], key[1])
            for key, value in self.selected_items.items():
                print(key, value)
            self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    finder = Finder()
    db = DatabaseEngine()
    app = QApplication(sys.argv)
    con = sqlite3.connect('../db/challenge.db')
    wnd = TestDialogWind(finder, con)
    wnd.exec()
    db.close()
    sys.excepthook = except_hook
    sys.exit(app.exec())
