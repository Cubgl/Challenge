import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QToolBar, QAction, QRadioButton, \
    QDockWidget, QGroupBox, QHBoxLayout, QTextEdit, QVBoxLayout, QLineEdit, QLabel, QPushButton, \
    QMessageBox

from topic.number_systems_ import BinToDec, OctToDec

SIZE_WIDTH, SIZE_HEIGHT = 600, 600


class CentralArea(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.main_wind = parent

        self.central_layout = QVBoxLayout(self)

        self.label_statement = QLabel(self)
        self.label_statement.setText('Условие задачи:')
        self.central_layout.addWidget(self.label_statement)

        self.task_layout = QHBoxLayout(self)

        self.statement = QTextEdit(self)
        self.resize(SIZE_WIDTH // 2, SIZE_HEIGHT // 2)
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

        self.last_line_layout.addWidget(self.save_button)
        self.last_line_layout.addSpacing(SIZE_WIDTH // 2)

        self.central_layout.addLayout(self.last_line_layout)

        self.setLayout(self.central_layout)

    def send_answer(self):
        answer = self.student_answer.text()
        if len(answer) == 0 or answer.isspace():
            return
        self.main_wind.results[self.main_wind.switch_bar.selected_item] = self.student_answer.text()
        self.main_wind.change_task()

    def save_answer(self):
        index = self.main_wind.switch_bar.selected_item
        self.main_wind.answers[index] = self.student_answer.text()


class SwitchMenu(QToolBar):
    def __init__(self, parent, count_tasks):
        super().__init__(parent)

        self.selected_item = 0
        self.main_window = parent

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
        self.addWidget(groupbox)

        self.addSeparator()

        self.finish_button = QPushButton(self)
        self.finish_button.setText('Завершить тест')
        self.finish_button.clicked.connect(self.finish_test)
        self.addWidget(self.finish_button)

    def change_task(self):
        btn = self.sender()
        self.selected_item = int(btn.text()) - 1
        current_task = self.main_window.tasks[self.selected_item]
        self.main_window.change_task()

    def finish_test(self):
        count = 0
        for i in range(len(self.main_window.results)):
            count += int(self.main_window.results[i]) == self.main_window.tasks[i].good_answer
        msg_box = QMessageBox()
        msg_box.about(self, 'Результат',
                                    f'Ваш результат: {count} из {len(self.main_window.results)}.')


class MainWindow(QMainWindow):

    def __init__(self, list_tasks):
        super().__init__()

        self.setWindowTitle('Challenge')
        self.resize(600, 600)
        self.setWindowFlags(QtCore.Qt.MSWindowsFixedSizeDialogHint)

        self.setStyleSheet('font-size: 14px')

        self.tasks = list_tasks
        self.answers = [None] * len(self.tasks)
        self.results = [None] * len(self.tasks)

        self.switch_bar = SwitchMenu(self, len(self.tasks))
        self.addToolBar(self.switch_bar)

        self.centralWidget = CentralArea(self)
        self.setCentralWidget(self.centralWidget)

        self.change_task()

    def change_task(self):
        index = self.switch_bar.selected_item
        current_task = self.tasks[index]
        self.centralWidget.statement.setHtml(current_task.generated_text)
        if self.results[self.switch_bar.selected_item] is not None:
            self.centralWidget.student_answer.setEnabled(False)
            self.centralWidget.save_button.setEnabled(False)
            answer = self.results[self.switch_bar.selected_item]
            self.centralWidget.save_button.setText(f'Ответ принят')
            self.centralWidget.student_answer.setText(answer)
        else:
            self.centralWidget.student_answer.setEnabled(True)
            self.centralWidget.save_button.setText('Отправить ответ')
            if self.answers[index] is not None:
                self.centralWidget.student_answer.setText(self.answers[index])
            else:
                self.centralWidget.student_answer.setText("")
            self.centralWidget.save_button.setEnabled(True)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = MainWindow([BinToDec(), BinToDec(), OctToDec(), OctToDec()])
    wnd.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
