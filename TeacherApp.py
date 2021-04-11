import sys

from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QToolBox, QLabel

from finder import Finder

SIZE_WIDTH, SIZE_HEIGHT = 800, 600


class MainWind(QDialog):
    def __init__(self, finder):
        super().__init__()
        self.setWindowTitle('Формирование теста')
        self.resize(SIZE_WIDTH, SIZE_HEIGHT)
        self.list_topics = finder.list_topics_names

        tool_box = QToolBox()
        for elem in self.list_topics:
            tool_box.addItem(QLabel(f'Содержимое вкладки {elem}'), elem)
        tool_box.setCurrentIndex(0)

        self.layout = QVBoxLayout()
        self.layout.addWidget(tool_box)
        self.setLayout(self.layout)


if __name__ == '__main__':
    finder = Finder()
    print(finder.list_topics_names)
    print(finder.list_topics_data)
    app = QApplication(sys.argv)
    wnd = MainWind(finder)
    wnd.show()
    sys.exit(app.exec())
