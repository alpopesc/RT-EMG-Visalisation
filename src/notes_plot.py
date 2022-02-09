from PyQt5 import QtGui
from PyQt5.QtCore import QTimer, Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QComboBox, QFileDialog,QMessageBox,QDialog
from colour import Color
import numpy as np
from DB_stream import DB_stream
import pyqtgraph as pg
from pgcolorbar.colorlegend import ColorLegendItem
import bioml.Feature_Extraction as FE
import scipy.signal as sgn
import pyqtgraph.ptime as ptime
from LUI import Ui_Form
from collections import deque
from statistics import mean
import pyqtgraph.exporters
import os
import tempfile
from distutils.dir_util import copy_tree
from collections import deque
from scipy.fft import fft
from scipy.fft import fftfreq
import scipy




default_kernel = np.array([[0, 1, 0],
                        [1, 0, 1],
                        [0, 1, 0]])

def butter_bandpass(lowcut, highcut, fs, order=2):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = scipy.signal.butter(order, [low, high], btype='band')
    return b, a



class RT_Lineplot(QWidget):
    """
    class representing a custom Widget containing a Heatmap plot and input widgets
    """

    close_request = pyqtSignal(str)

    def __init__(self, stream, mtx_form, feature_name = 'MAV', fs = 2400, step = 0, min_len = 1, max_len = 10000,  kernel = default_kernel):
        """
        constuctor
        Initialises all the widgets and connects them to their corresponding functions/slots
        :param stream: A Data_stram object
        :param mtx_form: A matrix containing the channel config information
        :param feature_name: A default feature name
        :param fs: A default sampling frequency
        :param step: default plot interval
        :param min_len: min choosable window length
        :param max_len: max choosable windwo length
        :param kernel: convoltion kernel
        """
        print("preinitialisation beginning")
        super().__init__()
        print("preinitialisation complete")
        self.stream = stream
        self.feature_name = feature_name
        self.fs = fs
        self.step = step
        self.kernel = kernel
        self.mtx_form = mtx_form
        self.EMG = deque(np.zeros(1000))
        self.EMG_F = deque(np.zeros(1000))
        self.Time = deque(np.zeros(1000))



        l = QHBoxLayout()

        self.Lineplot_widget = pg.PlotWidget(title = "EMG Lineplot")
        x1_axis = self.Lineplot_widget.getAxis('bottom')
        x1_axis.setLabel(text='Time [s]')
        y1_axis = self.Lineplot_widget.getAxis('left')
        y1_axis.setLabel(text='Voltage [mV]')

        self.Fourier1_widget = pg.PlotWidget(title = "Fourier")
        x1_axis = self.Fourier1_widget.getAxis('bottom')
        x1_axis.setLabel(text='Frequency [Hz]')
        y1_axis = self.Fourier1_widget.getAxis('left')
        y1_axis.setLabel(text='Amplitude')

        self.Fourier2_widget = pg.PlotWidget(title = "smooth Fourier")
        x1_axis = self.Fourier2_widget.getAxis('bottom')
        x1_axis.setLabel(text='Frequency [Hz]')
        y1_axis = self.Fourier2_widget.getAxis('left')
        y1_axis.setLabel(text='Amplitude')


        l.addWidget(self.Lineplot_widget)
        l.addWidget(self.Fourier1_widget)


        # Creating plots
        self.Lineplot = self.Lineplot_widget.getPlotItem().plot()
        self.Fourier1_plot = self.Fourier1_widget.getPlotItem().plot()
        self.Fourier2_plot = self.Fourier2_widget.getPlotItem().plot()


        self.updateTime = ptime.time()
        self.fps = 0
        tm = [self.step] * 100
        self.intrvl = deque(tm)


        self.form = QWidget()
        self.ui_form = Ui_Form()
        self.ui_form.setupUi(self.form)

        ##Setting up ChannelBox
        self.ui_form.ChannelBox.setInsertPolicy(QComboBox.NoInsert)
        channels = list(self.stream.get_Window().columns)
        self.channel = channels[1]
        for i in channels[1:]:
            self.ui_form.ChannelBox.addItem(str(i))


        # Setting up the FilterBox
        self.all_feat = FE.DefinedFeatures()
        self.ui_form.FilterBox.setInsertPolicy(QComboBox.NoInsert)
        tmp = self.all_feat.get_existing_features()
        for i in tmp:
            self.ui_form.FilterBox.addItem(i.name)

        ## Setting up the Window length option
        self.ui_form.window_sizeBox.setMinimum(min_len)
        self.ui_form.window_sizeBox.setMaximum(max_len)
        self.ui_form.window_sizeBox.setValue(int(self.stream.get_winLen() * (1000/self.fs)))

        ## Setting up the step option
        self.ui_form.step_sizeBox.setMinimum(0)
        self.ui_form.step_sizeBox.setMaximum(max_len)
        self.ui_form.step_sizeBox.setValue(self.step)

        ## Setting up the Window length option
        l.addWidget(self.form)
        self.form.show()
        self.setLayout(l)

        self.ui_form.ChannelBox.currentTextChanged.connect(self.update_channel)
        self.ui_form.FilterBox.currentTextChanged.connect(self.update_filter)
        self.ui_form.window_sizeBox.valueChanged.connect(self.update_winLen)
        self.ui_form.step_sizeBox.valueChanged.connect(self.update_step)

        # Creating all the timers and connection them to their corresponding function
        self.timer_thred = QTimer()
        self.timer_thred.setTimerType(Qt.PreciseTimer)
        self.timer_thred.setInterval(self.step)
        self.timer_thred.start()
        self.timer = QTimer()
        self.timer.setTimerType(Qt.PreciseTimer)
        self.timer.setInterval(self.step)
        self.timer.timeout.connect(self.update_plt)
        self.timer.start()


    def update_channel(self):
        """
        Slot that updates the displayed channel
        :return: No return
        """
        self.channel = self.ui_form.ChannelBox.currentText()
        self.update_plt()

    def update_winLen(self):
        """
        Slot that updates the window length attribute if the corresponding widget value changes
        :return: No return
        """
        g = int(self.ui_form.window_sizeBox.value() * (self.fs/1000) + 1)
        self.stream.set_winLen(g)
        self.update_plt()
        print("Update window length")
        print(self.stream.window_length)

    def update_step(self):
        """
        Slot that updates the step size attribute if the corresponding widget value changes
        :return: No return
        """
        self.timer.setInterval(self.ui_form.step_sizeBox.value())
        self.update_plt()
        print("Update step size")


    def update_filter(self):
        """
        Slot that updates the filter attribute if the corresponding widget text changes
        :return: No return
        """
        self.feature_name = self.ui_form.FilterBox.currentText()
        self.update_plt()





    def closeEvent(self, event):
        """
        Overwritten function that sends a signal if the window is to be closed (red x is clicked). This signal
        is then used in the MainWindow class to delete the widget.
        :param event:
        :return: No return
        """
        print("User has clicked the red x on the main window")
        self.close_request.emit("desallocate_window")
        event.accept()

    def update_plt(self):
        """
        Most central function of the class. It requests new data from the DB and then updates the image. In order for
        the image to be constantly updated and therefore create a real-time video animation, a timer calls this function
        at currently defined interval steps
        :return:
        """
        window = self.stream.get_Window()
        window2 = window
        window2 = window2.set_index('index')



        #print(window["HA-2015.08.05_channel1"])
        #window2 = window2.set_index('index')
        #y = FE.MFE(self.seq_notchFilter(window.to_numpy().transpose()), [FE.DefinedFeatures().features[self.feature_name]], self.fs)
        #yf = fft(y)
        #xf = fftfreq(len(yf),1/self.fs)


        #kk = window2.to_numpy().transpose()[0][::-1]
        kk = window[self.channel]


        #print("%0.1f fps" % self.fps)


        now = ptime.time()
        #self.EMG.append(y[1])
        #self.EMG.popleft()
        tau = now-self.updateTime
        self.Time.append(tau)
        self.Time = deque(np.array(self.Time)-tau)
        self.Time.popleft()

        #self.Lineplot.setData(list(np.linspace(0,len(kk)-1, len(kk))), list(kk))
        self.Fourier1_plot.setData(list(fftfreq(len(kk),1/2400)[:len(kk)//2]), list(abs(fft(kk)[:len(kk)//2])))
        #self.Fourier1_plot.setData(list(fftfreq(len(self.EMG), 1 / 2400)[:len(self.EMG) // 2]), list(abs(fft(self.EMG)[:len(self.EMG) // 2])))

        fps2 = 1.0 / (now - self.updateTime)
        self.intrvl.append(now-self.updateTime)
        self.intrvl.popleft()
        print(mean(self.intrvl))
        self.updateTime = now
        self.fps = self.fps * 0.9 + fps2 * 0.1

    def seq_notchFilter(self, vec):
        """This function could be used to filter out harmonic frequencies However it is still problematic. The problem
            probaly lies in choosing right quality factor. Also it might be better to filter out the sequences at the root
            meaning filtering out the frequencies before they are uploaded to the database"""
        ## Note that the chosen frequency are based purely on empirically found values. Multiples of 50 Hz.
        fs = np.array([100,150,250,350,450,550])
        for i in range(len(vec)):
            for e in fs:
                b,a = sgn.iirnotch(e,e/1000,2400)
                vec[i] = sgn.lfilter(b,a,np.array(vec[i]))
        return vec


    def comb_filter(self,vec):
        pass



if __name__ == '__main__':
    import ast
    mtx = np.array([[0, 0, 0, 0, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 8, 0, 7, 0, 6, 0, 5, 0, 4, 0, 3],
                    [16, 0, 15, 0, 14, 0, 13, 0, 12, 0, 11, 0, 10, 0],
                    [0, 23, 0, 22, 0, 21, 0, 20, 0, 19, 0, 18, 0, 17],
                    [30, 0, 29, 0, 28, 0, 27, 0, 26, 0, 25, 0, 24, 0],
                    [0, 36, 0, 35, 0, 34, 0, 33, 0, 32, 0, 31, 0, 0],
                    [0, 0, 42, 0, 41, 0, 40, 0, 39, 0, 38, 0, 37, 0],
                    [0, 48, 0, 47, 0, 46, 0, 45, 0, 44, 0, 43, 0, 0],
                    [0, 0, 53, 0, 52, 0, 51, 0, 50, 0, 49, 0, 0, 0],
                    [0, 0, 0, 58, 0, 57, 0, 56, 0, 55, 0, 54, 0, 0],
                    [0, 0, 63, 0, 62, 0, 61, 0, 60, 0, 59, 0, 0, 0]])

    app = QApplication([])
    general_param = {}
    with open('default_par.txt', 'r') as f:
        s = f.read()
        general_param = ast.literal_eval(s)

    stream = DB_stream(general_param)
    win = RT_Lineplot(stream, mtx, fs=2400)
    win.show()
    app.exec_()