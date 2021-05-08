import sys

from PyQt5 import QtCore
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableView, QDialog, \
    QTableWidgetItem

from DatabaseTools.database_engine import DatabaseEngine
from TeacherApp.for_teacher import Ui_MainWindow
from TeacherApp.finder import Finder
from TeacherApp.test_dialog import TestDialogWind

SIZE_WIDTH, SIZE_HEIGHT = 800, 600


class TeacherAppMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('TeacherApp')
        self.setStyleSheet('font-size: 16px')
        self.resize(SIZE_WIDTH, SIZE_HEIGHT)
        self.add_test.triggered.connect(self.new_test)
        self.button_add.clicked.connect(self.new_test)
        self.button_delete.clicked.connect(self.remove_test)
        self.delete_test.triggered.connect(self.remove_test)
        self.edit_test.triggered.connect(self.update_test)
        self.button_edit.clicked.connect(self.update_test)
        self.tableWidget_test.itemChanged.connect(self.item_changed)
        self.titles = ['title', 'mixing', 'training']
        self.quit.triggered.connect(self.close)
        self.all_cahllenges = None
        self.load_challenges_form_db()
        self.init_table_view()

    def load_challenges_form_db(self):
        db = DatabaseEngine()
        self.all_cahllenges = db.search_all_challenges()
        db.close()

    def item_changed(self, item):
        id = self.all_cahllenges[item.row()][0]
        db = DatabaseEngine()
        db.update_challenges(self.titles[item.column()], item.text(), id)
        db.close()
        self.load_challenges_form_db()

    def update_test(self):
        if len(self.tableWidget_test.selectedIndexes()) == 0:
            QMessageBox().information(self, "Тест не выбран", 'Выделите тест в списке, пожалуйста!')
            return
        row_selected = self.tableWidget_test.selectedIndexes()[0].row()
        id_selected = self.all_cahllenges[row_selected][0]
        db = DatabaseEngine()
        info_challenge, items_challenge = db.get_test_params(id_selected)
        db.close()
        test_params_window = TestDialogWind(finder, (info_challenge, items_challenge))
        test_params_window.exec()
        self.load_challenges_form_db()
        self.init_table_view()

    def remove_test(self):
        if len(self.tableWidget_test.selectedIndexes()) == 0:
            QMessageBox().information(self, "Тест не выбран", 'Выделите тест в списке, пожалуйста!')
            return
        row_selected = self.tableWidget_test.selectedIndexes()[0].row()
        title_selected = self.all_cahllenges[row_selected][1]
        result = QMessageBox.question(
            self, 'Подтверждение удаления теста',
            f'Вы действительно хотите удалить тест с названием: {title_selected}?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if result == QMessageBox.Yes:
            id_selected = self.all_cahllenges[row_selected][0]
            db = DatabaseEngine()
            res_del = db.delete_challenge(id_selected)
            db.close()
            if res_del == -1:
                QMessageBox().warning(self, "Ошибка", 'Произошла ошибка при удалении теста.')
            else:
                QMessageBox().information(self, "Результат удаления",
                                          f'Тест c названием {title_selected} успешно удален.')
                self.load_challenges_form_db()
                self.init_table_view()

    def init_table_view(self):
        self.tableWidget_test.setColumnCount(len(self.all_cahllenges[0]) - 1)
        self.tableWidget_test.setRowCount(len(self.all_cahllenges))
        self.tableWidget_test.setHorizontalHeaderLabels(
            ['Название теста', 'Случайный порядок', 'Режим обучения']
        )
        self.tableWidget_test.setColumnWidth(0, 450)
        self.tableWidget_test.setColumnWidth(1, 165)
        self.tableWidget_test.setColumnWidth(2, 165)
        for i, line in enumerate(self.all_cahllenges):
            for j, item in enumerate(line):
                if j == 0:
                    continue
                self.tableWidget_test.setItem(i, j - 1, QTableWidgetItem(str(item)))

    def new_test(self):
        sel_items = []
        db = DatabaseEngine()
        test_params_window = TestDialogWind(finder, sel_items)
        test_params_window.exec()
        db.close()
        self.load_challenges_form_db()
        self.init_table_view()

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


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    finder = Finder()
    wnd = TeacherAppMainWindow()
    wnd.show()

    sys.excepthook = except_hook
    sys.exit(app.exec_())
