
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
from HUI import Ui_Form
from collections import deque
from statistics import mean
import pyqtgraph.exporters
import os
import tempfile
from distutils.dir_util import copy_tree



default_kernel = np.array([[0, 1, 0],
                        [1, 0, 1],
                        [0, 1, 0]])



class RT_Heatmap(QWidget):
    """
    class representing a custom Widget containing a Heatmap plot and input widgets
    """

    close_request = pyqtSignal(str)

    def __init__(self, stream, mtx_form, feature_name = 'MAV', fs = 2400, step = 0, min_len = 1, max_len = 1000,  kernel = default_kernel):
        """
        _constructor
        Initialises all the widgets and connects them to their corresponding functions/slots
        :param stream: A Data_stram object
        :param mtx_form: A matrix containing the channel config information
        :param feature_name: A default feature name
        :param fs: A default sampling frequency
        :param step: default plot interval
        :param min_len: min selectable window length
        :param max_len: max selectable window length
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


        # Creating all the widgets necessary for the GUI
        self.win = pg.GraphicsLayoutWidget()
        # # self.win.show()  ## show widget alone in its own window
        self.setWindowTitle('EMG Heatmap')
        self.view = self.win.addViewBox()
        self.view.setAspectLocked(True)

        l = QHBoxLayout()

        # Setting up Colors
        blue, red = Color('black'), Color('yellow')
        colors = blue.range_to(red, 256)
        colors_array = np.array([np.array(color.get_rgb()) * 255 for color in colors])
        look_up_table = colors_array.astype(np.uint8)

        # Creating image
        self.img = pg.ImageItem(border='w')
        self.img.setLookupTable(look_up_table)
        self.img.setOpts(axisOrder='row-major')
        self.view.addItem(self.img)

        self.updateTime = ptime.time()
        self.fps = 0
        tm = [self.step] * 100
        self.intrvl = deque(tm)

        # Creating Colorbar
        self.img.setLookupTable(look_up_table)
        self.color_bar = ColorLegendItem(imageItem=self.img, showHistogram=True, label='sample')  # 2021/01/20 add label
        self.win.addItem(self.color_bar)
        self.update_img()
        self.color_bar.autoScaleFromImage()

        l.addWidget(self.win)
        self.form = QWidget()
        self.ui_form = Ui_Form()
        self.ui_form.setupUi(self.form)

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

        ## Setting up the Color option
        self.ui_form.ColorBox.setInsertPolicy(QComboBox.NoInsert)
        self.ui_form.ColorBox.addItems(["yellow", "white", "green", "blue", "red","orange","violet","snow","lightyellow"])



        self.ui_form.sv_file.setEnabled(False)
        self.ui_form.StrtButton.setEnabled(True)
        self.ui_form.StpButton_2.setEnabled(False)
        self.ui_form.CnclButton_3.setEnabled(True)

        self.ui_form.StrtButton.clicked.connect(self.start_recording)
        self.ui_form.StpButton_2.clicked.connect(self.stop_recording)
        self.ui_form.FilterBox.currentTextChanged.connect(self.update_filter)
        self.ui_form.window_sizeBox.valueChanged.connect(self.update_winLen)
        self.ui_form.step_sizeBox.valueChanged.connect(self.update_step)
        self.ui_form.ColorBox.currentTextChanged.connect(self.update_color)
        self.ui_form.StrtButton.clicked.connect(self.start_recording)
        self.ui_form.StpButton_2.clicked.connect(self.stop_recording)
        self.ui_form.sv_file.clicked.connect(self.save_file)
        self.ui_form.CnclButton_3.clicked.connect(self.cancel_recording)


        # Defining an exporter for the recorded images
        self.exporter = pg.exporters.ImageExporter(self.view)
        self.temp_dir = tempfile.TemporaryDirectory()
        self.path = self.temp_dir.name
        print(self.path)
        self.cnt = 0

        # Creating all the timers and connection them to their corresponding function
        self.timer_thred = QTimer()
        self.timer_thred.setTimerType(Qt.PreciseTimer)
        self.timer_thred.setInterval(self.step)
        self.timer_thred.start()
        self.timer = QTimer()
        self.timer.setTimerType(Qt.PreciseTimer)
        self.timer.setInterval(self.step)
        self.timer.timeout.connect(self.update_img)
        self.timer.start()


    def thread_record(self):
        """
        Exports the current image to the temporary file
        :return: No return
        """
        self.exporter.export(self.path + "/img{}.jpg".format(self.cnt) ,False , False)
        self.cnt = self.cnt + 1
        #self.save_request.emit(self.exporter)


    def start_recording(self):
        """
        Slot that starts the recording if button is pushed
        :return: No return
        """
        self.ui_form.StrtButton.setEnabled(False)
        self.ui_form.StpButton_2.setEnabled(True)
        self.timer_thred.timeout.connect(self.thread_record)


    def stop_recording(self):
        """
        Slot that stops recording if button is pushed
        :return: No return
        """
        self.ui_form.StpButton_2.setEnabled(False)
        self.timer_thred.timeout.disconnect(self.thread_record)
        self.ui_form.sv_file.setEnabled(True)


    def save_file(self):
        """
        Slot that saves the recorded temporary file to the location chosen by the file dialog if corresponding button
        is pushed
        :return: No return
        """
        name = QtGui.QFileDialog.getSaveFileName()
        if(name[0] != ''):
            os.mkdir(name[0])
            copy_tree(self.path, name[0])
            print(name)
            print("Saving file")
            self.temp_dir.cleanup()
            self.ui_form.StrtButton.setEnabled(True)
            self.ui_form.sv_file.setEnabled(False)

    def cancel_recording(self):
        """
        Slot that cancels/deletes the current recording if corresponding button is pushed
        :return: No return
        """
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Cancel last Recording")
        dlg.setText("Are you sure you want to cancel the last recording without saving ?")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dlg.setIcon(QMessageBox.Question)
        button = dlg.exec_()
        if button == QMessageBox.Yes:
            self.temp_dir.cleanup()
            self.ui_form.StrtButton.setEnabled(True)
            self.ui_form.sv_file.setEnabled(False)


    def update_winLen(self):
        """
        Slot that updates the window length attribute if the corresponding widget value changes
        :return: No return
        """
        g = int(self.ui_form.window_sizeBox.value() * (self.fs/1000) + 1)
        self.stream.set_winLen(g)
        self.update_img()
        self.color_bar.autoScaleFromImage()
        print("Update window length")
        print(self.stream.window_length)

    def update_step(self):
        """
        Slot that updates the step size attribute if the corresponding widget value changes
        :return: No return
        """
        self.timer.setInterval(self.ui_form.step_sizeBox.value())
        self.update_img()
        self.color_bar.autoScaleFromImage()
        print("Update step size")


    def update_filter(self):
        """
        Slot that updates the filter attribute if the corresponding widget text changes
        :return: No return
        """
        self.feature_name = self.ui_form.FilterBox.currentText()
        self.update_img()
        self.color_bar.autoScaleFromImage()


    def update_color(self):
        """
        Slot that updates the color attribute if the corresponding widget text changes
        :return: No return
        """
        c1, c2 = Color('black'), Color(self.ui_form.ColorBox.currentText())
        colors = c1.range_to(c2, 256)
        colors_array = np.array([np.array(color.get_rgb()) * 255 for color in colors])
        look_up_table = colors_array.astype(np.uint8)
        self.img.setLookupTable(look_up_table)
        self.update_img()
        self.color_bar.setImageItem(self.img)
        print("Update color")

    def get_imgMatrix(self,v):
        """
        Creates an image matrix with the values from a given array/list v and the channel/sensor configuration
        :param v: array/list of channel/sensor values
        :return: an image matrix where the channel values are set at the correct position in a matrix
        """
        r_mtx = np.zeros((len(self.mtx_form), len(self.mtx_form[0])))
        for m in range(len(self.mtx_form)):
            for n in range(len(self.mtx_form[0])):
                if(self.mtx_form[m][n] != 0 and v !=[]):
                    r_mtx[m][n] = v[int(self.mtx_form[m][n]) - 1]
                else:
                    r_mtx[m][n] = 0
        return r_mtx

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

    def update_img(self):
        """
        Most central function of the class. It requests new data from the DB and then updates the image. In order for
        the image to be constantly updated and therefore create a real-time video animation, a timer calls this function
        at currently defined interval steps
        :return:
        """
        window = self.stream.get_Window()
        #timestamp = window['index'].to_numpy()[0] / 100000
        #dt_object = datetime.fromtimestamp(timestamp)
        window = window.set_index('index')
        y = FE.MFE(window.to_numpy().transpose(), [FE.DefinedFeatures().features[self.feature_name]], self.fs)
        mtx = self.get_imgMatrix(y)
        cnv = sgn.convolve2d(mtx, self.kernel, boundary='wrap', mode='same') / self.kernel.sum()
        output = mtx.copy()
        output[mtx == 0] = cnv[mtx == 0]
        #print("%0.1f fps" % self.fps)
        self.img.setImage(np.rot90(output.T,1))


        now = ptime.time()
        fps2 = 1.0 / (now - self.updateTime)
        self.intrvl.append(now-self.updateTime)
        self.intrvl.popleft()
        print(mean(self.intrvl))
        self.updateTime = now
        self.fps = self.fps * 0.9 + fps2 * 0.1



