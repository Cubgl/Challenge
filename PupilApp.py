import sys

from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QRadioButton, QGroupBox, QHBoxLayout, QTextEdit, \
    QVBoxLayout, QLineEdit, QLabel, QPushButton, QMessageBox, QDialog

from topic.excel_table_ import *

SIZE_WIDTH, SIZE_HEIGHT = 800, 600


class CentralArea(QDialog):
    def __init__(self, list_tasks):
        super().__init__()
        self.setWindowTitle('Challenge')
        self.resize(SIZE_WIDTH, SIZE_HEIGHT)
        self.setStyleSheet('font-size: 18px')

        self.selected_item = 0
        self.tasks = list_tasks
        for i in range(len(self.tasks)):
            self.tasks[i].make_task()
        self.tasks[0].statement()
        print('Изображение:', self.tasks[0].task_image)

        self.answers = [None] * len(self.tasks)
        self.results = [None] * len(self.tasks)

        self.interface()
        self.change_text_task()
        self.student_answer.setFocus()

    def interface(self):
        self.central_layout = QVBoxLayout(self)

        switch_panel = QHBoxLayout(self)
        self.interface_switch_bar(len(self.tasks), switch_panel)
        self.central_layout.addLayout(switch_panel)

        self.label_statement = QLabel(self)
        self.label_statement.setText('Условие задачи:')
        self.central_layout.addWidget(self.label_statement)

        self.task_layout = QHBoxLayout(self)

        self.statement = QTextEdit(self)
        self.resize(SIZE_WIDTH // 2, SIZE_HEIGHT // 4)
        self.statement.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.task_layout.addWidget(self.statement)

        self.picture = QLabel(self)
        self.picture.move(self.statement.width(), 0)
        self.picture.resize(self.picture.width(), self.picture.height())
        self.pixmap = QPixmap()
        self.picture.setPixmap(self.pixmap)
        self.task_layout.addWidget(self.picture)

        self.central_layout.addLayout(self.task_layout)

        self.label_student_answer = QLabel(self)
        self.label_student_answer.setText('Ответ:')
        self.central_layout.addWidget(self.label_student_answer)

        self.student_answer = QLineEdit(self)
        self.student_answer.textChanged.connect(self.save_answer)
        self.central_layout.addWidget(self.student_answer)

        self.last_line_layout = QHBoxLayout(self)

        self.save_button = QPushButton(self)
        self.save_button.setText('Отправить ответ')
        self.save_button.clicked.connect(self.send_answer)
        self.save_button.setDefault(True)

        self.last_line_layout.addWidget(self.save_button)
        self.last_line_layout.addSpacing(SIZE_WIDTH // 2)

        self.central_layout.addLayout(self.last_line_layout)

        self.setLayout(self.central_layout)

    def interface_switch_bar(self, count_tasks, layout):
        groupbox = QGroupBox(self)
        radiogroup_layout = QHBoxLayout(self)
        for i in range(count_tasks):
            button = QRadioButton(self)
            button.setText(str(i + 1))
            button.clicked.connect(self.change_task)
            if i == 0:
                button.setChecked(True)
            button.setToolTip('Номер задания')
            button.setToolTipDuration(3000)
            radiogroup_layout.addWidget(button)
        groupbox.setLayout(radiogroup_layout)
        layout.addWidget(groupbox)

        self.finish_button = QPushButton(self)
        self.finish_button.setText('Завершить тест')
        self.finish_button.clicked.connect(self.finish_test)
        layout.addWidget(self.finish_button)

        self.result_label = QLabel(self)
        self.result_label.setText('                        ')
        layout.addWidget(self.result_label)

    def send_answer(self):
        answer = self.student_answer.text()
        if len(answer) == 0 or answer.isspace():
            return
        self.results[self.selected_item] = self.student_answer.text()
        self.change_text_task()
        if all(self.results):
            if QMessageBox().question(self, 'Введены все ответы',
                                      'Завершить тест?') == QMessageBox.Yes:
                self.finish_test()

    def save_answer(self):
        index = self.selected_item
        self.answers[index] = self.student_answer.text()

    def change_task(self):
        btn = self.sender()
        self.selected_item = int(btn.text()) - 1
        current_task = self.tasks[self.selected_item]
        self.change_text_task()

    def finish_test(self):
        if not all(self.results):
            QMessageBox().information(self, "Обратите внимание",
                                      'Для завершения теста нужно отправить ВСЕ ответы!')
            return

        count_good_answers = 0
        for i in range(len(self.results)):
            user_answer = ''
            if self.results[i] is not None:
                user_answer = ''.join(self.results[i].upper().split())
            ok_answer = self.tasks[i].good_answer.upper()
            count_good_answers += user_answer == ok_answer
        self.test_result = count_good_answers
        result_string = f'Ваш результат: {count_good_answers} из {len(self.results)}.'
        QMessageBox().information(self, 'Результат', result_string)
        self.test_result = result_string
        self.finish_button.setEnabled(False)
        self.result_label.setText(result_string)

    def change_text_task(self):
        index = self.selected_item
        current_task = self.tasks[index]
        self.statement.setHtml(current_task.generated_text)
        print(current_task.task_image)
        if current_task.task_image is not None:
            self.picture.setPixmap(QPixmap(self.tasks[index].task_image))
        else:
            self.picture.setPixmap(QPixmap())
        if self.results[self.selected_item] is not None:
            self.student_answer.setEnabled(False)
            self.save_button.setEnabled(False)
            answer = self.results[self.selected_item]
            self.save_button.setText(f'Ответ принят')
            self.student_answer.setText(answer)
        else:
            self.student_answer.setEnabled(True)
            self.save_button.setText('Отправить ответ')
            if self.answers[index] is not None:
                self.student_answer.setText(self.answers[index])
            else:
                self.student_answer.setText("")
            self.save_button.setEnabled(True)
        self.student_answer.setFocus()

    def closeEvent(self, e):
        result = QMessageBox.question(self, 'Подтверждение закрытия окна',
                                      'Вы действительно хотите закрыть окно?',
                                      QMessageBox.Yes | QMessageBox.No,
                                      QMessageBox.No)
        if result == QMessageBox.Yes:
            e.accept()
            QDialog.closeEvent(self, e)
        else:
            e.ignore()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = CentralArea([CalcFromWithPicture(), CalcFromIndirectInformation(), CalcFromWithPicture(),
                       CalcFromIndirectInformation()])
    wnd.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
