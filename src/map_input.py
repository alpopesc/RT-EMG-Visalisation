from PyQt5.QtWidgets import QDialog, QPushButton, QGridLayout,QApplication,\
    QSpinBox,QLabel,QDialogButtonBox,QFileDialog,QMessageBox,QSpacerItem
import numpy as np


class HM_input_dialog(QDialog):
    """
    Heatmap input dialog class:
    The class defines a custom dialog that is used to configure or load a sensor arrangement for the Heatmap. This
    sensor configuration is transmitted with a "formating-matrix" (in this class it is called the output_mtx) to the
    the Heatmap object. The underlying principle is that a matrix of pushbuttons was created where the positions in the
    matrix correspond to their positions in the gird layout. The user is then able to input the position of the
    sensor/channel by pushing a button in the grid of the pushbuttons.
    """
    def __init__(self,nb_chnnl, parent = None):
        """
        _constructor
        Initialises and sets up all the widgets used. Additonally all the signal are connected to their corresponding
        functions/slots
        :param nb_chnnl: number of channels/sensors used for the heatmap
        :param parent: a parent widget
        """
        super().__init__(parent)

        self.setWindowTitle("Setup input map")
        self.nb = nb_chnnl
        row = min(int(2*np.sqrt(nb_chnnl)),32)
        col = row

        self.cnt = 1
        self.mtx = [[]]
        self.output_mtx = np.zeros((row,col))

        self.input_layout = QGridLayout()
        self.general_layout = QGridLayout()
        self.setting_layout = QGridLayout()
        self.Pbutt_layout = QGridLayout()

        self.rowSizeSpBox = QSpinBox()
        self.colSizeSpBox = QSpinBox()
        self.sizeLabel1 = QLabel()
        self.sizeLabel2 = QLabel()
        self.ApplyButton = QPushButton("Apply")
        self.CancelButton = QDialogButtonBox(QDialogButtonBox.Cancel)
        self.SaveButton = QPushButton("Save")
        self.LoadButton = QPushButton("Load")

        self.rowSizeSpBox.setMinimum(1)
        self.colSizeSpBox.setMinimum(1)
        self.rowSizeSpBox.setMaximum(32)
        self.colSizeSpBox.setMaximum(32)
        self.rowSizeSpBox.setValue(row)
        self.colSizeSpBox.setValue(col)

        self.sizeLabel1.setText("Row size")
        self.sizeLabel2.setText("Column size")

        self.CancelButton.rejected.connect(self.reject)
        self.rowSizeSpBox.valueChanged.connect(self.reset_input_size)
        self.colSizeSpBox.valueChanged.connect(self.reset_input_size)
        self.ApplyButton.clicked.connect(self.end)
        self.LoadButton.clicked.connect(self.load_fromText)
        self.SaveButton.clicked.connect(self.save_toText)

        self.reset_input_size()

        self.setting_layout.addWidget(self.sizeLabel1,0,0)
        self.setting_layout.addWidget(self.rowSizeSpBox,0,1)
        self.setting_layout.addWidget(self.sizeLabel2,0,2)
        self.setting_layout.addWidget(self.colSizeSpBox,0,3)
        self.Pbutt_layout.addWidget(self.LoadButton,0,0)
        self.Pbutt_layout.addWidget(self.SaveButton,0,1)
        self.Pbutt_layout.addWidget(self.ApplyButton,0,2)
        self.setting_layout.addLayout(self.Pbutt_layout,0,4)
        self.setting_layout.addWidget(self.CancelButton,0,5)
        self.general_layout.addLayout(self.input_layout,0,0)
        self.general_layout.addItem(QSpacerItem(50,50),1,0)
        self.general_layout.addLayout(self.setting_layout,2,0)
        self.setLayout(self.general_layout)


    def make_Outmatrix(self):
        """
        Constructs the ouptut matrix from the matrix of pushbuttons.
        :return: No return
        """
        for i in range(len(self.mtx)):
            for j in range(len(self.mtx[0])):
                txt = self.mtx[i][j].text()
                if(txt != ''):
                    self.output_mtx[i][j] = int(txt)

    def reshape_Outmatrix(self):
        """
        Reshapes the output_mtx according to the inputed row and col size. Additionally it resets it to an all zero
        matrix
        :return: No return
        """
        self.output_mtx = np.zeros((self.rowSizeSpBox.value(), self.colSizeSpBox.value()))

    def end(self):
        """
        Representing the end of the dialog widget by closing the widget after the output_mtx was created
        :return: No return
        """
        self.make_Outmatrix()
        print(self.output_mtx)
        self.close()

    def reset_input_size(self):
        """
        Resets the size of the pushbutton matrix/grid according to the inputted row- and colsize.
        :return: No return
        """
        for row in self.mtx:
            for e in row:
                e.deleteLater()
                e = None

        self.mtx = [[QPushButton() for j in range(self.colSizeSpBox.value())] for i in range(self.rowSizeSpBox.value())]

        for i in range(len(self.mtx)):
            for j in range(len(self.mtx[0])):

                r = self.rowSizeSpBox.value()
                c = self.colSizeSpBox.value()
                a = int(60 - r)
                b = int(60 - c)
                if(self.sender() == self.rowSizeSpBox):
                    if(r >= c):
                        self.mtx[i][j].setFixedSize(a, a)
                    else:
                        self.mtx[i][j].setFixedSize(b, b)

                else:
                    if(r <= c):
                        self.mtx[i][j].setFixedSize(b, b)
                    else:
                        self.mtx[i][j].setFixedSize(a, a)

                self.mtx[i][j].clicked.connect(lambda state, r = i, c = j: self.set_sensor(r,c))
                self.mtx[i][j].setCheckable(True)
                self.input_layout.addWidget(self.mtx[i][j], i, j)
                #self.general_layout.addLayout(self.input_layout,0,0)
                #self.setLayout(self.general_layout)

        print(self.frameSize())
        self.output_mtx = np.zeros((r,c))
        self.cnt = 1
        print("dododo")



    def set_sensor(self, i,j):
        """
        displays the index of the positioned sensor/channel
        :param i: row position
        :param j: col position
        :return:
        """
        if(self.mtx[i][j].isChecked()):
            self.mtx[i][j].setText(str(self.cnt))
            self.cnt = self.cnt + 1

        else:
            val = int(self.mtx[i][j].text())
            self.mtx[i][j].setText('')
            self.cnt = val
            for m in range(len(self.mtx)):
                for n in range(len(self.mtx[0])):
                    if(self.mtx[m][n].isChecked() and int(self.mtx[m][n].text()) >= val):
                        self.mtx[m][n].setText('')
                        self.mtx[m][n].setChecked(False)


    def save_toText(self):
        """
        Saves the current sensor/channel configuration to a txt file by writing the output_mtx to a textfile.
        :return: No return
        """
        dest_path = QFileDialog.getSaveFileName(filter="Text files (*.txt)", initialFilter= "Text files (*.txt)")
        print(dest_path)
        self.make_Outmatrix()
        with open(dest_path[0], 'wb') as f:
            np.savetxt(f, self.output_mtx)
        self.reshape_Outmatrix()

    def load_fromText(self):
        """
        Loads a sensor configuration from a txt file
        :return: No return
        """
        dest_path = QFileDialog.getOpenFileName(filter="Text files (*.txt)", initialFilter= "Text files (*.txt)")
        if(dest_path[0] != ''):
            try:
                m = np.loadtxt(dest_path[0])
                if(self.check_highest_nb(m)):
                    r = len(m)
                    c = len(m[0])
                    if (r < 32 and c < 32):
                        self.rowSizeSpBox.setValue(r)
                        self.colSizeSpBox.setValue(c)
                        for i in range(r):
                            for j in range(c):
                                if(m[i][j] != 0):
                                    self.mtx[i][j].setText(str(int(m[i][j])))
                                    self.mtx[i][j].setChecked(True)
                    else:
                        wrn = QMessageBox(self)
                        wrn.setWindowTitle("Unable to load the format to the window")
                        wrn.setText("The given format is to big to load onto the window. Do you want to apply it directly ?")
                        wrn.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                        wrn.setIcon(QMessageBox.Question)
                        button = wrn.exec_()

                        if button == QMessageBox.Yes:
                            self.output_mtx = m
                            print(m)
                            self.close()
                else:
                    wrn2 = QMessageBox(self)
                    print("passing by")
                    wrn2.setWindowTitle("InputError")
                    wrn2.setText("You have selected more sensors than available")
                    wrn2.setIcon(QMessageBox.Critical)
                    button = wrn2.exec_()
            except:
                wrn3 = QMessageBox(self)
                print("passing by")
                wrn3.setWindowTitle("InputError")
                wrn3.setText("You have selected an invalid text file")
                wrn3.setIcon(QMessageBox.Critical)
                button = wrn3.exec_()


    def check_highest_nb(self,m):
        """
        Checks if a matrix contains a sensor/channel - index that is higher than the given number of sensors
        :param m: matrix of interst
        :return: A boolean; True if the matrix is legal to use (all indeces are smaller then the number of channels
        """
        switch = True
        for i in range(len(m)):
            for j in range(len(m[i])):
                if (m[i][j] > self.nb):
                    switch = False
        return switch


    @staticmethod
    def get_inp_matrix(n,parent = None):
        """
        This is the central function that is needed to initialise the Dialog and pass on the information acquired
        :param n: number of channels/sensors
        :param parent: parent
        :return: output_mtx that corresponds to the sensor channel configuration
        """
        D = HM_input_dialog(n,parent)
        D.exec_()
        if(D.check_highest_nb(D.output_mtx)):
            return D.output_mtx
        else:
            wrn4 = QMessageBox(D)
            print("passing by")
            wrn4.setWindowTitle("InputError")
            wrn4.setText("You have selected more sensors than available")
            wrn4.setIcon(QMessageBox.Critical)
            button = wrn4.exec_()
            return [[]]


