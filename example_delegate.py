from PyQt5 import QtCore, QtWidgets, QtGui

import sys

from PyQt5.QtWidgets import QWidget


class SpinMaxDelegate(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, optopns, index):
        editor = QtWidgets.QSpinBox(parent)
        editor.setFrame(False)
        editor.setMaximum(0)
        editor.setSingleStep(1)
        return editor

    def setEditorData(self, editor: QWidget, index: QtCore.QModelIndex) -> None:
        value = int(index.model().data(index, QtCore.Qt.EditRole))