from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow,QMessageBox
from DB_stream import DB_stream

from MUI import Ui_MainWindow
from map_input import HM_input_dialog
from RT_Heatmap import RT_Heatmap
from RT_Lineplot import RT_Lineplot
from RT_Lineplot_Raw import RT_Lineplot_Raw
from RT_Fourier_Raw import RT_Fourier_Raw
import numpy as np
import ast


class MainWindow(QMainWindow):
    """
    MainWindow Class:
    The class defines the main window from which all the plots shall be coordinated. At the moment the data can only be
    extracted from a Database. The parameters needed to connect to a DB are first set to the default values that
    correspond to the values saved from the last execution (saved to default_par.txt). One could still change the
    parameters using the GUI. Once the Create_plot button is pressed all the parameters are saved and passed to the
    DB_stream class to initiate a connection with the DB. If successful a Plot is created according to the inputs.
    For a Serial(Arduino) datasource implementation one would have to add separate default
    parameter_file and slightly change the code (some if statements) etc. Additionally one would also have to add a Serial
    stream class as an Attribute. This class is not coded yet but could be a child of the Data_stream class.
    """
    def __init__(self):
        """
        _constructor
        Define all the widget and initialise the layout from MUI.py (python version of UI-file). Further
        the default parameters needed to create a data stream are loaded from default_par.txt to a dictionary.
        Additionaly all the signals are connected to their corresponding function(slot).
        """
        super().__init__()

        self.ui_form = Ui_MainWindow()
        self.ui_form.setupUi(self)

        #Loading default parameters from default_par.txt
        self.general_param = {}
        with open('default_par.txt', 'r') as f:
            s = f.read()
            self.general_param = ast.literal_eval(s)

        #Creating the a dictionary with the different plots and their corresponding function
        self.plots = {}
        self.plots["Heatmap"] = self.create_Hmap
        self.plots["Lineplot"] = self.create_Lplot
        self.plots["Lineplot_Raw"] = self.create_LRplot
        self.plots["Fourier_Raw"] = self.create_Fplot


        #Adding all the plot option to the W
        self.ui_form.PlotBox.addItems(list(self.plots.keys()))

        #Setting the textfield to the default values

        self.ui_form.DB_Port_LE.setValidator(QtGui.QIntValidator())
        self.ui_form.DB_radio_bttn.setChecked(True)
        self.ui_form.FsSpin.setRange(1, 1000000)
        self.ui_form.Create_Plot_Bttn.clicked.connect(self.create_plot)

        self.ui_form.DB_name_LE.setText(self.general_param["dbparam"]["dbname"])
        self.ui_form.User_LE.setText(self.general_param["dbparam"]["user"])
        self.ui_form.Host_LE.setText(self.general_param["dbparam"]["host"])
        self.ui_form.DB_Port_LE.setText(str(self.general_param["dbparam"]["port"]))
        self.ui_form.Table_LE.setText(self.general_param["tbname"])
        self.ui_form.Subject_id_LE.setText(self.general_param["subj"])
        self.ui_form.Condition_LE.setText(self.general_param["cdt_nb"])
        self.ui_form.Channel_LE.setText(self.general_param["channels"][0][:-1])
        self.ui_form.Channel_SpinBox.setValue(len(self.general_param["channels"]))
        self.ui_form.FsSpin.setValue(int(self.general_param["Fs"]))


        self.stream = None
        self.H_map = None   ##For multiple plots a vector of H_map would be a better idea. However multiplrocessing would be needed too.
        self.L_map = None
        self.LR_map = None
        self.F_map = None


    def set_DBparams(self):
        """
        Updates the parameter dictionary 'self.general_param' with the values form widgets. Note that if the serial
        optionality is added then one could also rename the function and set the serial parameters here too.
        :return: No return
        """
        if(self.ui_form.DB_radio_bttn.isChecked()):
            self.general_param["dbparam"]["dbname"] = self.ui_form.DB_name_LE.text()
            self.general_param["dbparam"]["user"] = self.ui_form.User_LE.text()
            self.general_param["dbparam"]["host"] = self.ui_form.Host_LE.text()
            self.general_param["dbparam"]["port"] = int(self.ui_form.DB_Port_LE.text())
            self.general_param["tbname"] = self.ui_form.Table_LE.text()
            self.general_param["subj"] = self.ui_form.Subject_id_LE.text()
            self.general_param["cdt_nb"] = self.ui_form.Condition_LE.text()
            self.general_param["Fs"] = self.ui_form.FsSpin.value()

            channels = []
            self.nb_chn = self.ui_form.Channel_SpinBox.value()
            for i in range(1, self.nb_chn+1):
                channels.append(self.ui_form.Channel_LE.text() + str(i))
            self.general_param["channels"] = channels

        print(self.general_param)



    def establish_connection(self):
        """
        Tries to initialise a DB_stream, in other words tries to establish a DB conncetion with given params
        At the moment only possible with DB_stream. Note if a serial optionality is added one could set self.stream
        to a serial stream class under an if condition.
        :return: No return
        """
        try:
            self.stream = DB_stream(self.general_param)
        except:
            wrn = QMessageBox(self)
            wrn.setWindowTitle("Connection Error")
            wrn.setText("Connection not possible. Check the parameters and your Internet connection")
            wrn.setIcon(QMessageBox.Critical)
            button = wrn.exec_()
            print(self.stream)
            return False
        return True

    def create_plot(self):
        """
        Creates a plot corresponding to the option chosen with GUI. At the moment there are only to type of plots. But
        one could always add other types of plot by adding them to the plot_dictionary with their corresponding function.
        :return: No return
        """
        self.plots[self.ui_form.PlotBox.currentText()]()


    def create_Hmap(self):
        """
        Creates a Heatmap with the given input
        :return: No return
        """
        self.set_DBparams()
        self.update_parFile()
        if (self.establish_connection()):
            m = HM_input_dialog.get_inp_matrix(self.nb_chn)
            if (m.size > 0 and np.any(m) and self.H_map is None):
                self.H_map = RT_Heatmap(self.stream, m, fs = self.ui_form.FsSpin.value())
                self.H_map.show()
                self.H_map.close_request.connect(self.close_Hmap)


    def close_Hmap(self):
        """
        Closes heatmap plot
        :return: No return
        """
        self.H_map.close
        self.H_map = None

    def create_Lplot(self):
        """
        Creates a Lineplot
        :return: No return
        """
        self.set_DBparams()
        self.update_parFile()
        if (self.establish_connection()):
            self.L_map = RT_Lineplot(self.stream, fs = self.ui_form.FsSpin.value())
            self.L_map.show()
            self.L_map.close_request.connect(self.close_Lplot)

    def close_Lplot(self):
        """
        Closes a Lineplot
        :return: No return
        """
        self.L_map.close
        self.L_map = None

    def create_LRplot(self):
        """
        Creates a Lineplot_raw
        :return: No return
        """
        self.set_DBparams()
        self.update_parFile()
        if (self.establish_connection()):
            self.LR_map = RT_Lineplot_Raw(self.stream, fs=self.ui_form.FsSpin.value())
            self.LR_map.show()
            self.LR_map.close_request.connect(self.close_LRplot)

    def close_LRplot(self):
        """
        Closes a Lineplot_raw
        :return: No return
        """
        self.LR_map.close
        self.LR_map = None

    def create_Fplot(self):
        """
        Creates a Fourier plot
        :return: No return
        """
        self.set_DBparams()
        self.update_parFile()
        if (self.establish_connection()):
            self.F_map = RT_Fourier_Raw(self.stream, fs=self.ui_form.FsSpin.value())
            self.F_map.show()
            self.F_map.close_request.connect(self.close_Fplot)

    def close_Fplot(self):
        """
        Closes a Fourierplot
        :return: No return
        """
        self.F_map.close
        self.F_map = None

    def update_parFile(self):
        """
        Saves the used parameters (DB option) to default_par.txt. So that the parameters can be defaulted with the same
        values for the next use.
        :return: No return
        """
        print(self.general_param)
        with open('default_par.txt', 'w') as f:
            f.write(str(self.general_param))



