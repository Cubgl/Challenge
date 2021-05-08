import sys

from PyQt5.QtCore import QItemSelectionModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QDialog, QApplication, QListView, QAbstractItemView, QVBoxLayout, \
    QPushButton, QHBoxLayout, QLabel, QMessageBox, QListWidget

from DatabaseTools.database_engine import DatabaseEngine
from PupilApp.Pupil_app import CentralArea

SIZE_WIDTH, SIZE_HEIGHT = 750, 550


class SelectTestWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Challenge')
        self.resize(SIZE_WIDTH, SIZE_HEIGHT)
        self.setStyleSheet('font-size: 18px')
        self.data_challenges = db.search_all_challenges()
        self.list_widget = QListWidget()
        for elem in self.data_challenges:
            self.list_widget.addItem(elem[1])
        self.list_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.btn_ok = QPushButton('Начать тест')
        self.btn_ok.setDefault(True)
        self.btn_ok.clicked.connect(self.begin_test)
        self.btn_exit = QPushButton('Выход')
        self.btn_exit.clicked.connect(self.reject)
        self.label = QLabel("Выберите тест")
        self.horiz_layout = QHBoxLayout()
        self.horiz_layout.addWidget(self.btn_ok)
        self.horiz_layout.addWidget(self.btn_exit)
        self.vert_layout = QVBoxLayout(self)
        self.vert_layout.addWidget(self.label)
        self.vert_layout.addWidget(self.list_widget)
        self.vert_layout.addLayout(self.horiz_layout)
        self.setLayout(self.vert_layout)
        self.data_test, self.test_items = None, None

    def begin_test(self):
        item_selected = self.list_widget.selectedItems()
        if len(item_selected) == 0:
            QMessageBox().information(self, "Тест не выбран", 'Выделите тест в списке, пожалуйста!')
            return
        title_test = item_selected[0].text()
        # print(title_test)
        id_test = db.search_id_challenge(title_test)
        self.data_test, self.test_items = db.load_test_params(id_test)
        self.accept()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    db = DatabaseEngine()
    ask_test = SelectTestWindow()
    if ask_test.exec() == QDialog.Accepted:
        wnd = CentralArea(ask_test.test_items, ask_test.data_test[0], ask_test.data_test[1])
        wnd.exec()
    sys.excepthook = except_hook
    sys.exit(app.exec())
    db.close()