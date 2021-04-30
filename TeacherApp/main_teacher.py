import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

from TeacherApp.for_teacher import Ui_MainWindow

from TeacherApp.finder import Finder

from TeacherApp.test_dialog import TestDialogWind

class TeacherAppMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.add_test.triggered.connect(self.new_test)
        self.quit.triggered.connect(self.close)

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