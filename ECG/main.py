from PyQt4 import QtGui,QtCore
import sys
import GUI
import numpy as np
import pyqtgraph
import process
import time
import pyqtgraph.exporters
import webbrowser

class ExampleApp(QtGui.QMainWindow, GUI.Ui_MainWindow):
    def __init__(self, parent=None):
        pyqtgraph.setConfigOption('background', '#000000') #before loading widget
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)
        self.ECG.plotItem.showGrid(True, True, 0.7)
        self.pushButton_2.clicked.connect(self.saveFig)
        self.pushButton.clicked.connect(self.website)
        stamp=" ECG PROGRAM BY MATI ETHIOPIA"
        self.stamp = pyqtgraph.TextItem(stamp,anchor=(-.01,1),color=(150,150,150),
                                        fill=pyqtgraph.mkBrush('#000000'))
        self.ear = process.Ear(chunk=int(100))
        # self.ear = input.Ear(chunk=int(100), device=5) # use audio input device 5
        if len(self.ear.valid_input_devices()):
            self.ear.stream_start()
            self.label.setText(self.ear.msg)
            self.update()

    def closeEvent(self, event):
        self.ear.close()
        event.accept()

    def saveFig(self):
        fname="ECG_%d.png"%time.time()
        exp = pyqtgraph.exporters.ImageExporter(self.ECG.plotItem)
        exp.parameters()['width'] = 1000
        exp.export(fname)
        print("saved",fname)

    def update(self):
        t1,timeTook=time.time(),0
        if len(self.ear.data) and not self.pushButton_3.isChecked():
            freqHighCutoff=0
            if self.spinBox.value()>0:
                freqHighCutoff=self.spinBox.value()
            data=self.ear.getFiltered(freqHighCutoff)
            if self.checkBox.isChecked():
                data=np.negative(data)
            if self.checkBox_2.isChecked():
                self.Yscale=np.max(np.abs(data))*1.1
            self.ECG.plotItem.setRange(xRange=[0,self.ear.maxMemorySec],
                            yRange=[-self.Yscale,self.Yscale],padding=0)
            self.ECG.plot(np.arange(len(data))/float(self.ear.rate),data,clear=True,
                            pen=pyqtgraph.mkPen(color='g'),antialias=True)
            self.ECG.plotItem.setTitle(self.lineEdit.text(),color=(150,150,150))
            self.stamp.setPos(0,-self.Yscale)
            self.ECG.plotItem.addItem(self.stamp)
            timeTook=(time.time()-t1)*1000
            print("plotting took %.02f ms"%(timeTook))
        msTillUpdate=int(self.ear.chunk/self.ear.rate*1000)-timeTook
        QtCore.QTimer.singleShot(max(0,msTillUpdate), self.update)

    def website(self):
        webbrowser.open("http://www.dec.edu.et")

if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    app.exec_()
