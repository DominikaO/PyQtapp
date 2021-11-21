import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QPushButton, QFileDialog, QVBoxLayout


class MyApp():


    def getFileName(self):
        file_filter = 'Data File (*.xlsx *.csv *.dat);; Excel File (*.xlsx *.xls)'
        response = QFileDialog.getOpenFileName(
            parent=QWidget,
            caption='Select a data file',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter='Excel File (*.xlsx *.xls)'
        )
        print(response)
        return response[0]

    def getFileNames(self):
        file_filter = 'Data File (*.xlsx *.csv *.dat);; Excel File (*.xlsx *.xls)'
        response = QFileDialog.getOpenFileNames(
            parent=QWidget,
            caption='Select a data file',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter='Excel File (*.xlsx *.xls)'
        )
        return response[0]

    def getDirectory(self):
        response = QFileDialog.getExistingDirectory(
            self,
            caption='Select a folder'
        )
        return response

    def getSaveFileName(self):
        file_filter = 'Data File (*.xlsx *.csv *.dat);; Excel File (*.xlsx *.xls)'
        response = QFileDialog.getSaveFileName(
            parent=self,
            caption='Select a data file',
            directory='Data File.dat',
            filter=file_filter,
            initialFilter='Excel File (*.xlsx *.xls)'
        )
        print(response)
        return response[0]

