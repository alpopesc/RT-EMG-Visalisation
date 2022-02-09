# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designerkyzFjN.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(254, 281)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(6)
        self.FilterBox = QComboBox(Form)
        self.FilterBox.setObjectName(u"FilterBox")
        self.FilterBox.setEnabled(True)

        self.gridLayout.addWidget(self.FilterBox, 3, 1, 1, 1)

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setEnabled(True)

        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)

        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setEnabled(True)

        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)

        self.step_sizeBox = QSpinBox(Form)
        self.step_sizeBox.setObjectName(u"step_sizeBox")
        self.step_sizeBox.setEnabled(True)

        self.gridLayout.addWidget(self.step_sizeBox, 2, 1, 1, 1)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setEnabled(True)

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.StpButton_2 = QPushButton(Form)
        self.StpButton_2.setObjectName(u"StpButton_2")
        self.StpButton_2.setEnabled(True)

        self.gridLayout.addWidget(self.StpButton_2, 5, 1, 1, 1)

        self.ColorBox = QComboBox(Form)
        self.ColorBox.setObjectName(u"ColorBox")
        self.ColorBox.setEnabled(True)

        self.gridLayout.addWidget(self.ColorBox, 4, 1, 1, 1)

        self.StrtButton = QPushButton(Form)
        self.StrtButton.setObjectName(u"StrtButton")
        self.StrtButton.setEnabled(True)

        self.gridLayout.addWidget(self.StrtButton, 5, 0, 1, 1)

        self.CnclButton_3 = QPushButton(Form)
        self.CnclButton_3.setObjectName(u"CnclButton_3")
        self.CnclButton_3.setEnabled(True)

        self.gridLayout.addWidget(self.CnclButton_3, 6, 0, 1, 1)

        self.window_sizeBox = QSpinBox(Form)
        self.window_sizeBox.setObjectName(u"window_sizeBox")
        self.window_sizeBox.setEnabled(True)

        self.gridLayout.addWidget(self.window_sizeBox, 1, 1, 1, 1)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setEnabled(True)

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.sv_file = QPushButton(Form)
        self.sv_file.setObjectName(u"sv_file")

        self.gridLayout.addWidget(self.sv_file, 6, 1, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Filter", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Color", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Step size [ms]", None))
        self.StpButton_2.setText(QCoreApplication.translate("Form", u"Stop recording", None))
        self.StrtButton.setText(QCoreApplication.translate("Form", u"Start recording", None))
        self.CnclButton_3.setText(QCoreApplication.translate("Form", u"Cancel", None))
        self.label.setText(QCoreApplication.translate("Form", u"Window size [ms]", None))
        self.sv_file.setText(QCoreApplication.translate("Form", u"Save file", None))
    # retranslateUi







