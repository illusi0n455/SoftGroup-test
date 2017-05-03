# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'myui.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(540, 517)
        self.fillBtn = QtWidgets.QPushButton(Dialog)
        self.fillBtn.setGeometry(QtCore.QRect(350, 90, 141, 71))
        self.fillBtn.setObjectName("fillBtn")
        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setGeometry(QtCore.QRect(30, 10, 256, 461))
        self.listWidget.setObjectName("listWidget")
        self.exportBtn = QtWidgets.QPushButton(Dialog)
        self.exportBtn.setGeometry(QtCore.QRect(350, 220, 141, 71))
        self.exportBtn.setObjectName("exportBtn")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.fillBtn.setText(_translate("Dialog", "Fill"))
        self.exportBtn.setText(_translate("Dialog", "Export"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    Dialog.show()
    sys.exit(app.exec_())

