# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designerjMZeuI.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *




class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(838, 507)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")

        self.DB_radio_bttn = QRadioButton(self.centralwidget)
        self.DB_name_LE = QLineEdit(self.centralwidget)
        self.User_LE = QLineEdit(self.centralwidget)
        self.Host_LE = QLineEdit(self.centralwidget)
        self.DB_Port_LE = QLineEdit(self.centralwidget)
        self.Table_LE = QLineEdit(self.centralwidget)
        self.Channel_LE = QLineEdit(self.centralwidget)
        self.Channel_SpinBox = QSpinBox(self.centralwidget)
        self.Subject_id_LE = QLineEdit(self.centralwidget)
        self.Condition_LE = QLineEdit(self.centralwidget)
        self.Serial_Port_LE = QLineEdit(self.centralwidget)
        self.Baudrate_LE = QLineEdit(self.centralwidget)
        self.TimeoutSpinBox = QSpinBox(self.centralwidget)
        self.Create_Plot_Bttn = QPushButton(self.centralwidget)
        self.PlotBox = QComboBox(self.centralwidget)
        self.FsSpin = QSpinBox(self.centralwidget)

        self.FsLabel = QLabel(self.centralwidget)
        self.FsLabel.setObjectName(u"FsLabel")
        self.gridLayout.addWidget(self.FsLabel,18,0,1,1)

        self.FsSpin.setObjectName(u"FsSpin")
        self.FsSpin.setFixedWidth(150)
        self.gridLayout.addWidget(self.FsSpin,18,1,1,1)


        self.Serial_Port_LE.setObjectName(u"Serial_Port_LE")
        self.Serial_Port_LE.setEnabled(False)
        self.gridLayout.addWidget(self.Serial_Port_LE, 14, 1, 1, 1)

        self.Subject_id_LE.setObjectName(u"Subject_id_LE")
        self.gridLayout.addWidget(self.Subject_id_LE, 9, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(self.horizontalSpacer_4, 11, 0, 1, 7)

        self.Baudrate_LE.setObjectName(u"Baudrate_LE")
        self.Baudrate_LE.setEnabled(False)
        self.gridLayout.addWidget(self.Baudrate_LE, 15, 1, 1, 1)

        self.User_LE.setObjectName(u"User_LE")
        self.gridLayout.addWidget(self.User_LE, 2, 1, 1, 1)

        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)

        self.label_13 = QLabel(self.centralwidget)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setEnabled(False)
        self.gridLayout.addWidget(self.label_13, 14, 0, 1, 1)

        self.DB_Port_LE.setObjectName(u"DB_Port_LE")
        self.gridLayout.addWidget(self.DB_Port_LE, 4, 1, 1, 1)

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(self.horizontalSpacer_5, 17, 0, 1, 7)

        self.label_14 = QLabel(self.centralwidget)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setEnabled(False)
        self.gridLayout.addWidget(self.label_14, 15, 0, 1, 1)

        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        self.gridLayout.addWidget(self.label_7, 7, 0, 1, 7)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.gridLayout.addWidget(self.label, 9, 0, 1, 1)


        self.Channel_LE.setObjectName(u"Channel_LE")
        self.gridLayout.addWidget(self.Channel_LE, 8, 1, 1, 1)

        self.Channel_SpinBox.setObjectName(u"Channel_SpinBox")
        self.gridLayout.addWidget(self.Channel_SpinBox, 8, 5, 1, 1)

        self.label_12 = QLabel(self.centralwidget)
        self.label_12.setObjectName(u"label_12")
        self.gridLayout.addWidget(self.label_12, 13, 1, 1, 5)

        self.label_17 = QLabel(self.centralwidget)
        self.label_17.setObjectName(u"label_17")
        self.gridLayout.addWidget(self.label_17, 18, 2, 1, 1)

        self.DB_name_LE.setObjectName(u"DB_name_LE")
        self.gridLayout.addWidget(self.DB_name_LE, 1, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(self.horizontalSpacer_3, 6, 0, 1, 7)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.label_16 = QLabel(self.centralwidget)
        self.label_16.setObjectName(u"label_16")
        self.gridLayout.addWidget(self.label_16, 10, 0, 1, 1)

        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        self.gridLayout.addWidget(self.label_8, 8, 0, 1, 1)

        self.label_15 = QLabel(self.centralwidget)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setEnabled(False)
        self.gridLayout.addWidget(self.label_15, 16, 0, 1, 1)

        self.label_10 = QLabel(self.centralwidget)
        self.label_10.setObjectName(u"label_10")
        self.gridLayout.addWidget(self.label_10, 11, 7, 1, 1)


        self.Host_LE.setObjectName(u"Host_LE")
        self.gridLayout.addWidget(self.Host_LE, 3, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(811, 15, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(self.horizontalSpacer, 12, 0, 1, 7)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.DB_radio_bttn.setObjectName(u"DB_radio_bttn")
        self.gridLayout.addWidget(self.DB_radio_bttn, 0, 0, 1, 1)


        self.TimeoutSpinBox.setObjectName(u"TimeoutSpinBox")
        self.TimeoutSpinBox.setEnabled(False)
        self.gridLayout.addWidget(self.TimeoutSpinBox, 16, 1, 1, 1)


        self.Create_Plot_Bttn.setObjectName(u"Create_Plot_Bttn")
        self.gridLayout.addWidget(self.Create_Plot_Bttn, 18, 5, 1, 1)

        self.Condition_LE.setObjectName(u"Condition_LE")
        self.gridLayout.addWidget(self.Condition_LE, 10, 1, 1, 1)

        self.Table_LE.setObjectName(u"Table_LE")
        self.gridLayout.addWidget(self.Table_LE, 5, 1, 1, 1)

        self.Serial_radiobttn = QRadioButton(self.centralwidget)
        self.Serial_radiobttn.setObjectName(u"Serial_radiobttn")
        self.Serial_radiobttn.setEnabled(False)
        self.Serial_radiobttn.setCheckable(True)
        self.Serial_radiobttn.setAutoRepeatDelay(299)
        self.gridLayout.addWidget(self.Serial_radiobttn, 13, 0, 1, 1)

        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName(u"label_9")
        self.gridLayout.addWidget(self.label_9, 8, 4, 1, 1)


        self.PlotBox.setObjectName(u"PlotBox")
        self.gridLayout.addWidget(self.PlotBox, 18, 4, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Table name", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Port", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Port", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Baudrate", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-style:italic;\">Note: The columns of the table should contain an index column, the numerated channel columns as well as the following columnames: &quot;subject_id&quot; and &quot;condition&quot;</span></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Subject_id", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-style:italic;\">Check to choose Serial as Data source. </span><span style=\" font-style:italic; text-decoration: underline;\">This option is currently unavailable</span></p></body></html>", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Choose Plot", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"User", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Condition", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Channel name", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Timeout [ms]", None))
        self.label_10.setText("")
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Host/IP", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Database name", None))
        self.DB_radio_bttn.setText(QCoreApplication.translate("MainWindow", u"Database", None))
        self.Create_Plot_Bttn.setText(QCoreApplication.translate("MainWindow", u"Create Plot", None))
        self.Serial_radiobttn.setText(QCoreApplication.translate("MainWindow", u"Serial", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Number of Channels ", None))
        self.FsLabel.setText(QCoreApplication.translate("MainWindow",u"Frequecy [Hz] ",None))
    # retranslateUi