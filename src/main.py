from MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication
import sqlalchemy.sql.default_comparator
import sklearn.utils._weight_vector



if __name__ == '__main__':
    app = QApplication([])
    win = MainWindow()
    win.show()
    app.exec_()

