import sys
import psycopg2
from PyQt5 import QtCore, QtGui, QtWidgets
from myui import Ui_MainWindow
from ast import literal_eval
import json


class Fill(QtCore.QThread):
    signal = QtCore.pyqtSignal(list)

    def __init__(self):
        super().__init__()

    def get_info(self):
        #  я не дуже зрозумів де потрібно було описувати зєдняння тому описав тут
        with psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='1'") as conn:
            cur = conn.cursor()
            cur.execute("""SELECT * FROM theme""")
            rows = cur.fetchall()
            self.signal.emit(rows)


class Export(QtCore.QThread):
    def __init__(self, items):
        super().__init__()
        self.items = items

    def dump_data(self):
        fname, _ = QtWidgets.QFileDialog.getSaveFileName(None, 'Save file', 'myFile', '(*.json)')
        try:
            with open(fname, 'w') as file:
                print(1)
                file.write(json.dumps(self.items))
                print(1)
        except:
            pass


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.fillBtn.clicked.connect(self.fill_list_widget)
        self.ui.exportBtn.clicked.connect(self.export_to_json)

    def fill_list_widget(self):
        filler = Fill()
        filler.signal.connect(self.add_element)
        filler.get_info()

    def add_element(self, mylist):
        for i in mylist:
            self.ui.listWidget.addItem(str(i))

    def export_to_json(self):
        itemslist = [literal_eval(self.ui.listWidget.item(i).text()) for i in range(self.ui.listWidget.count())]
        exporter = Export(itemslist)
        exporter.dump_data()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = MainWindow()
    myapp.show()
    sys.exit(app.exec_())
