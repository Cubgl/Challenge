import sys

from PyQt5 import QtCore
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableView

from TeacherApp.for_teacher import Ui_MainWindow
from TeacherApp.finder import Finder
from TeacherApp.test_dialog import TestDialogWind

PATH_DB = '../db/challenge.db'

class TeacherAppMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.add_test.triggered.connect(self.new_test)
        self.quit.triggered.connect(self.close)
        self.init_table_view()

    def init_table_view(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(PATH_DB)
        db.open()
        model = QSqlTableModel(self, db)
        model.setTable('challenges')
        model.setHeaderData(1, QtCore.Qt.Horizontal, 'Название теста')
        model.setHeaderData(2, QtCore.Qt.Horizontal, 'Перемешивать вопросы')
        model.setHeaderData(3, QtCore.Qt.Horizontal, 'Режим обучения')
        model.select()
        self.tableView_test.setModel(model)
        self.tableView_test.hideColumn(0)
        self.tableView_test.setColumnWidth(1, 200)
        self.tableView_test.setColumnWidth(2, 150)
        self.tableView_test.setColumnWidth(3, 150)

    def new_test(self):
        finder = Finder()
        test_params_window = TestDialogWind(finder)
        test_params_window.exec()

    def closeEvent(self, e):
        result = QMessageBox.question(self, 'Подтверждение закрытия окна',
                                      'Вы действительно хотите закрыть окно?',
                                      QMessageBox.Yes | QMessageBox.No,
                                      QMessageBox.No)
        if result == QMessageBox.Yes:
            e.accept()
            QMainWindow.closeEvent(self, e)
        else:
            e.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = TeacherAppMainWindow()
    wnd.show()
    sys.exit(app.exec_())