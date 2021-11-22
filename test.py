# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
from PyQt5.QtCore import pyqtSlot
import os
from preprocessing import *
from PyQt5.QtWidgets import QFileDialog
import os
import tkinter as tk
import cv2
import numpy as np
import threading

from tkinter import messagebox
from tkinter.filedialog import askopenfilename, askdirectory

from PyQt5.QtWidgets import QFileDialog

import json


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        self.window_name = 'Image'
        self.init_img_path = None
        self.colored_img_arr = None
        self.active_img = None
        self.adjusted_img_array = None
        self.adjusted_img_array_prev = None
        self.save_dir = None
        self.selected_imgs_paths = []
        self.initial_img_arr = None
        self.used_filters = {"current": [], "last": []}

        # *********************** IMPORT / EXPORT list **********************************
        self.filters = {}
        self.filters["gb_width"] = []
        self.filters["gb_height"] = []
        self.filters["gb_sigma"] = []
        self.filters["it_type"] = []
        self.filters["it_method"] = []
        self.filters["it_max"] = []
        self.filters["it_th"] = []
        self.filters["it_block"] = []
        self.filters["it_Cv"] = []
        self.filters["ce_th1"] = []
        self.filters["ce_th2"] = []
        self.filters["dil_width"] = []
        self.filters["dil_height"] = []
        self.filters["dil_iterations"] = []
        self.filters["ero_width"] = []
        self.filters["ero_height"] = []
        self.filters["ero_iterations"] = []

        self.json_filters = {}

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(803, 702)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 40, 161, 80))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.btn_selectimgs = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_selectimgs.setObjectName("btn_selectimgs")
        self.verticalLayout.addWidget(self.btn_selectimgs)
        self.btn_saveimgs = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_saveimgs.setObjectName("btn_saveimgs")
        self.verticalLayout.addWidget(self.btn_saveimgs)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 0, 791, 31))
        self.label.setObjectName("label")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(170, 40, 160, 80))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.radioBtn_orig = QtWidgets.QRadioButton(self.verticalLayoutWidget_2)
        self.radioBtn_orig.setObjectName("radioBtn_orig")
        self.verticalLayout_2.addWidget(self.radioBtn_orig)
        self.radioBtn_prep = QtWidgets.QRadioButton(self.verticalLayoutWidget_2)
        self.radioBtn_prep.setObjectName("radioBtn_prep")
        self.verticalLayout_2.addWidget(self.radioBtn_prep)
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(340, 40, 160, 80))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.btn_undo = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.btn_undo.setObjectName("btn_undo")
        self.verticalLayout_3.addWidget(self.btn_undo)
        self.btn_reset = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.btn_reset.setObjectName("btn_reset")
        self.verticalLayout_3.addWidget(self.btn_reset)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 140, 271, 251))
        self.groupBox.setObjectName("groupBox")
        self.gridLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 50, 241, 161))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.vS_gbheight = QtWidgets.QSlider(self.gridLayoutWidget)
        self.vS_gbheight.setMaximumSize(QtCore.QSize(15, 150))
        self.vS_gbheight.setMaximum(15)
        self.vS_gbheight.setOrientation(QtCore.Qt.Vertical)
        self.vS_gbheight.setObjectName("vS_gbheight")
        self.gridLayout.addWidget(self.vS_gbheight, 4, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 25))
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 2, 1, 1)
        self.vS_gbsigma = QtWidgets.QSlider(self.gridLayoutWidget)
        self.vS_gbsigma.setMaximumSize(QtCore.QSize(15, 150))
        self.vS_gbsigma.setMaximum(20)
        self.vS_gbsigma.setOrientation(QtCore.Qt.Vertical)
        self.vS_gbsigma.setObjectName("vS_gbsigma")
        self.gridLayout.addWidget(self.vS_gbsigma, 4, 4, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 4, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 4, 5, 1, 1)
        self.vslid_gbwidth = QtWidgets.QSlider(self.gridLayoutWidget)
        self.vslid_gbwidth.setMaximumSize(QtCore.QSize(15, 150))
        self.vslid_gbwidth.setMaximum(15)
        self.vslid_gbwidth.setOrientation(QtCore.Qt.Vertical)
        self.vslid_gbwidth.setObjectName("vslid_gbwidth")
        self.gridLayout.addWidget(self.vslid_gbwidth, 4, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 3, 4, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 4, 3, 1, 1)
        self.label_19 = QtWidgets.QLabel(self.groupBox)
        self.label_19.setGeometry(QtCore.QRect(110, 20, 47, 20))
        self.label_19.setObjectName("label_19")
        self.btn_gaus = QtWidgets.QPushButton(self.groupBox)
        self.btn_gaus.setGeometry(QtCore.QRect(60, 220, 131, 21))
        self.btn_gaus.setObjectName("btn_gaus")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(280, 140, 351, 251))
        self.groupBox_2.setObjectName("groupBox_2")
        self.comboBox_2 = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_2.setGeometry(QtCore.QRect(60, 20, 111, 21))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox.setGeometry(QtCore.QRect(220, 20, 111, 21))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setGeometry(QtCore.QRect(10, 20, 51, 21))
        self.label_4.setObjectName("label_4")
        self.label_10 = QtWidgets.QLabel(self.groupBox_2)
        self.label_10.setGeometry(QtCore.QRect(180, 20, 41, 21))
        self.label_10.setObjectName("label_10")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.groupBox_2)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 50, 331, 161))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.vS_itblock = QtWidgets.QSlider(self.gridLayoutWidget_2)
        self.vS_itblock.setMaximum(81)
        self.vS_itblock.setOrientation(QtCore.Qt.Vertical)
        self.vS_itblock.setObjectName("vS_itblock")
        self.gridLayout_2.addWidget(self.vS_itblock, 1, 4, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_13.setObjectName("label_13")
        self.gridLayout_2.addWidget(self.label_13, 1, 5, 1, 1)
        self.vS_itth = QtWidgets.QSlider(self.gridLayoutWidget_2)
        self.vS_itth.setMinimum(1)
        self.vS_itth.setMaximum(255)
        self.vS_itth.setOrientation(QtCore.Qt.Vertical)
        self.vS_itth.setObjectName("vS_itth")
        self.gridLayout_2.addWidget(self.vS_itth, 1, 2, 1, 1)
        self.vS_itCval = QtWidgets.QSlider(self.gridLayoutWidget_2)
        self.vS_itCval.setMaximum(80)
        self.vS_itCval.setOrientation(QtCore.Qt.Vertical)
        self.vS_itCval.setObjectName("vS_itCval")
        self.gridLayout_2.addWidget(self.vS_itCval, 1, 6, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_12.setObjectName("label_12")
        self.gridLayout_2.addWidget(self.label_12, 1, 3, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_16.setObjectName("label_16")
        self.gridLayout_2.addWidget(self.label_16, 0, 5, 1, 1)
        self.vS_itMax = QtWidgets.QSlider(self.gridLayoutWidget_2)
        self.vS_itMax.setMinimum(1)
        self.vS_itMax.setMaximum(255)
        self.vS_itMax.setOrientation(QtCore.Qt.Vertical)
        self.vS_itMax.setObjectName("vS_itMax")
        self.gridLayout_2.addWidget(self.vS_itMax, 1, 0, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_11.setObjectName("label_11")
        self.gridLayout_2.addWidget(self.label_11, 1, 1, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_14.setObjectName("label_14")
        self.gridLayout_2.addWidget(self.label_14, 0, 1, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_15.setObjectName("label_15")
        self.gridLayout_2.addWidget(self.label_15, 0, 3, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_17.setObjectName("label_17")
        self.gridLayout_2.addWidget(self.label_17, 1, 7, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_18.setObjectName("label_18")
        self.gridLayout_2.addWidget(self.label_18, 0, 7, 1, 1)
        self.btn_threshold = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_threshold.setGeometry(QtCore.QRect(110, 220, 141, 21))
        self.btn_threshold.setObjectName("btn_threshold")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 400, 201, 251))
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.groupBox_3)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(10, 50, 181, 161))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_20 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_20.setObjectName("label_20")
        self.gridLayout_3.addWidget(self.label_20, 1, 1, 1, 1)
        self.vs_ceTh1 = QtWidgets.QSlider(self.gridLayoutWidget_3)
        self.vs_ceTh1.setMaximum(500)
        self.vs_ceTh1.setOrientation(QtCore.Qt.Vertical)
        self.vs_ceTh1.setObjectName("vs_ceTh1")
        self.gridLayout_3.addWidget(self.vs_ceTh1, 1, 0, 1, 1)
        self.vs_ceTh2 = QtWidgets.QSlider(self.gridLayoutWidget_3)
        self.vs_ceTh2.setMaximum(500)
        self.vs_ceTh2.setOrientation(QtCore.Qt.Vertical)
        self.vs_ceTh2.setObjectName("vs_ceTh2")
        self.gridLayout_3.addWidget(self.vs_ceTh2, 1, 2, 1, 1)
        self.label_21 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_21.setObjectName("label_21")
        self.gridLayout_3.addWidget(self.label_21, 1, 3, 1, 1)
        self.label_22 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_22.setObjectName("label_22")
        self.gridLayout_3.addWidget(self.label_22, 0, 1, 1, 1)
        self.label_23 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_23.setObjectName("label_23")
        self.gridLayout_3.addWidget(self.label_23, 0, 3, 1, 1)
        self.btn_appyCanny = QtWidgets.QPushButton(self.groupBox_3)
        self.btn_appyCanny.setGeometry(QtCore.QRect(60, 220, 75, 23))
        self.btn_appyCanny.setObjectName("btn_appyCanny")
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setGeometry(QtCore.QRect(250, 400, 251, 251))
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayoutWidget_4 = QtWidgets.QWidget(self.groupBox_4)
        self.gridLayoutWidget_4.setGeometry(QtCore.QRect(10, 49, 218, 161))
        self.gridLayoutWidget_4.setObjectName("gridLayoutWidget_4")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.gridLayoutWidget_4)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_24 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_24.setObjectName("label_24")
        self.gridLayout_4.addWidget(self.label_24, 1, 1, 1, 1)
        self.vs_deWigth = QtWidgets.QSlider(self.gridLayoutWidget_4)
        self.vs_deWigth.setMaximum(15)
        self.vs_deWigth.setOrientation(QtCore.Qt.Vertical)
        self.vs_deWigth.setObjectName("vs_deWigth")
        self.gridLayout_4.addWidget(self.vs_deWigth, 1, 0, 1, 1)
        self.vs_deHeight = QtWidgets.QSlider(self.gridLayoutWidget_4)
        self.vs_deHeight.setMaximum(15)
        self.vs_deHeight.setOrientation(QtCore.Qt.Vertical)
        self.vs_deHeight.setObjectName("vs_deHeight")
        self.gridLayout_4.addWidget(self.vs_deHeight, 1, 2, 1, 1)
        self.vs_deIter = QtWidgets.QSlider(self.gridLayoutWidget_4)
        self.vs_deIter.setMaximum(15)
        self.vs_deIter.setOrientation(QtCore.Qt.Vertical)
        self.vs_deIter.setObjectName("vs_deIter")
        self.gridLayout_4.addWidget(self.vs_deIter, 1, 4, 1, 1)
        self.label_26 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_26.setObjectName("label_26")
        self.gridLayout_4.addWidget(self.label_26, 1, 5, 1, 1)
        self.label_25 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_25.setObjectName("label_25")
        self.gridLayout_4.addWidget(self.label_25, 1, 3, 1, 1)
        self.label_27 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_27.setObjectName("label_27")
        self.gridLayout_4.addWidget(self.label_27, 0, 1, 1, 1)
        self.label_28 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_28.setObjectName("label_28")
        self.gridLayout_4.addWidget(self.label_28, 0, 3, 1, 1)
        self.label_29 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_29.setObjectName("label_29")
        self.gridLayout_4.addWidget(self.label_29, 0, 5, 1, 1)
        self.btn_applyDil = QtWidgets.QPushButton(self.groupBox_4)
        self.btn_applyDil.setGeometry(QtCore.QRect(10, 220, 101, 21))
        self.btn_applyDil.setObjectName("btn_applyDil")
        self.btn_erosion = QtWidgets.QPushButton(self.groupBox_4)
        self.btn_erosion.setGeometry(QtCore.QRect(130, 220, 101, 21))
        self.btn_erosion.setObjectName("btn_erosion")
        self.label_30 = QtWidgets.QLabel(self.groupBox_4)
        self.label_30.setGeometry(QtCore.QRect(100, 20, 47, 14))
        self.label_30.setObjectName("label_30")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(510, 390, 211, 261))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.btn_import = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.btn_import.setObjectName("pushButton_3")
        self.verticalLayout_4.addWidget(self.btn_import)
        self.listWidget = QtWidgets.QListWidget(self.verticalLayoutWidget_4)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_4.addWidget(self.listWidget)
        self.btn_add = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.btn_add.setObjectName("btn_add")
        self.verticalLayout_4.addWidget(self.btn_add)
        self.btn_export = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.btn_export.setObjectName("pushButton_4")
        self.verticalLayout_4.addWidget(self.btn_export)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 803, 22))
        self.menubar.setObjectName("menubar")
        self.menuPreprocessing_app = QtWidgets.QMenu(self.menubar)
        self.menuPreprocessing_app.setObjectName("menuPreprocessing_app")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuPreprocessing_app.menuAction())

        self.retranslateUi(MainWindow)
        self.vslid_gbwidth.valueChanged['int'].connect(self.label_7.setNum)
        self.vS_gbheight.valueChanged['int'].connect(self.label_8.setNum)
        self.vS_gbsigma.valueChanged['int'].connect(self.label_9.setNum)
        self.vS_itMax.valueChanged['int'].connect(self.label_11.setNum)
        self.vS_itth.valueChanged['int'].connect(self.label_12.setNum)
        self.vS_itblock.valueChanged['int'].connect(self.label_13.setNum)
        self.vS_itCval.valueChanged['int'].connect(self.label_17.setNum)
        self.vs_ceTh1.valueChanged['int'].connect(self.label_20.setNum)
        self.vs_ceTh2.valueChanged['int'].connect(self.label_21.setNum)
        self.vs_deWigth.valueChanged['int'].connect(self.label_24.setNum)
        self.vs_deHeight.valueChanged['int'].connect(self.label_25.setNum)
        self.vs_deIter.valueChanged['int'].connect(self.label_26.setNum)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

#*********************** SETUP BTNS CLICKED ********************8
        self.btn_selectimgs.clicked.connect(lambda: self.getFileNames())
        self.btn_saveimgs.clicked.connect(lambda: self.save_active_img())
        self.btn_undo.clicked.connect(lambda: self.undo_last_change())
        self.btn_reset.clicked.connect(lambda: self.reset_image())
        self.btn_export.clicked.connect(lambda: self.export_params())
        self.btn_import.clicked.connect(lambda: self.import_params())
        self.btn_applyDil.clicked.connect(lambda: self.apply_morph("dilation"))
        self.btn_erosion.clicked.connect(lambda: self.apply_morph("erosion"))
        self.btn_gaus.clicked.connect(lambda: self.apply_gaussian_blur())
        self.btn_appyCanny.clicked.connect(lambda: self.apply_canny_edge())
        self.btn_threshold.clicked.connect(lambda: self.apply_threshold())
        self.radioBtn_orig.clicked.connect(lambda: self.change_img_preview(1))
        self.radioBtn_prep.clicked.connect(lambda: self.change_img_preview(2))




    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_selectimgs.setText(_translate("MainWindow", "Select images"))
        self.btn_saveimgs.setText(_translate("MainWindow", "Save images"))
        self.label.setText(_translate("MainWindow", "Preprocessing application"))
        self.label_2.setText(_translate("MainWindow", "Preview mode"))
        self.radioBtn_orig.setText(_translate("MainWindow", "Original"))
        self.radioBtn_prep.setText(_translate("MainWindow", "Preprocessed"))
        self.btn_undo.setText(_translate("MainWindow", "Undo"))
        self.btn_reset.setText(_translate("MainWindow", "Reset"))
        self.groupBox.setTitle(_translate("MainWindow", "Gaussian Blur"))
        self.label_5.setText(_translate("MainWindow", "Width"))
        self.label_3.setText(_translate("MainWindow", "Height"))
        self.label_7.setText(_translate("MainWindow", "0"))
        self.label_9.setText(_translate("MainWindow", "0"))
        self.label_6.setText(_translate("MainWindow", "Sigma"))
        self.label_8.setText(_translate("MainWindow", "0"))
        self.label_19.setText(_translate("MainWindow", "Kernel"))
        self.btn_gaus.setText(_translate("MainWindow", "Apply Gaussian Blur"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Image Thresholding"))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "Binary Inverse"))
        self.comboBox_2.setItemText(1, _translate("MainWindow", "Binary"))
        self.comboBox_2.setItemText(2, _translate("MainWindow", "Trunc"))
        self.comboBox_2.setItemText(3, _translate("MainWindow", "To Zero"))
        self.comboBox_2.setItemText(4, _translate("MainWindow", "To Zero Inverse"))
        self.comboBox_2.setItemText(5, _translate("MainWindow", "Otsu"))
        self.comboBox_2.setItemText(6, _translate("MainWindow", "Triangle"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Gausian C"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Mean C"))
        self.label_4.setText(_translate("MainWindow", "Method :"))
        self.label_10.setText(_translate("MainWindow", "Type :"))
        self.label_13.setText(_translate("MainWindow", "0"))
        self.label_12.setText(_translate("MainWindow", "0"))
        self.label_16.setText(_translate("MainWindow", "Block size"))
        self.label_11.setText(_translate("MainWindow", "0"))
        self.label_14.setText(_translate("MainWindow", "Max value"))
        self.label_15.setText(_translate("MainWindow", "Threshold"))
        self.label_17.setText(_translate("MainWindow", "0"))
        self.label_18.setText(_translate("MainWindow", "C value"))
        self.btn_threshold.setText(_translate("MainWindow", "Apply Thresholding"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Canny Edge"))
        self.label_20.setText(_translate("MainWindow", "0"))
        self.label_21.setText(_translate("MainWindow", "0"))
        self.label_22.setText(_translate("MainWindow", "Threshold 1"))
        self.label_23.setText(_translate("MainWindow", "Threshold 2"))
        self.btn_appyCanny.setText(_translate("MainWindow", "Apply canny "))
        self.groupBox_4.setTitle(_translate("MainWindow", "Dilate / Erode"))
        self.label_24.setText(_translate("MainWindow", "1"))
        self.label_26.setText(_translate("MainWindow", "1"))
        self.label_25.setText(_translate("MainWindow", "1"))
        self.label_27.setText(_translate("MainWindow", "Width"))
        self.label_28.setText(_translate("MainWindow", "Height"))
        self.label_29.setText(_translate("MainWindow", "Iterations"))
        self.btn_applyDil.setText(_translate("MainWindow", "Apply Dilatation"))
        self.btn_erosion.setText(_translate("MainWindow", "Apply Erosion"))
        self.label_30.setText(_translate("MainWindow", "Kernel"))
        self.btn_export.setText(_translate("MainWindow", "EXPORT PARAMS"))
        self.btn_add.setText(_translate("MainWindow", "ADD"))
        self.btn_import.setText(_translate("MainWindow", "IMPORT PARAMS"))
        self.menuPreprocessing_app.setTitle(_translate("MainWindow", "Preprocessing app"))


# ********************************** FUNCTIONS FOR BUTTONS *****************************************

    def getFileNames(self):
        filter = 'Data File (*.jpeg *.jpg *.tif);; Picture File (*.jpeg *.jpg)'
        response = QFileDialog.getOpenFileNames(
            parent=MainWindow,
            caption='Select a data file',
            directory=os.getcwd(),
            filter=filter,
        )
        if response:
            self.selected_imgs_paths = response[0]
            self.adjusted_img_array_prev = None
            self.image = cv2.imread(self.selected_imgs_paths[0])
            self.used_filters['current'] = []
            self.used_filters['last'] = []
            self.set_colored_img(self.image)
            self.set_grayscale_img(self.image)

            create_img_window(680, 700, 'Image')

            cv2.imshow(self.window_name, self.active_img)

        print(self.selected_imgs_paths)

    def set_initial_img(self, init_img_path):
        self.selected_imgs_paths = [init_img_path]
        self.initial_img_arr = cv2.imread(init_img_path)
        self.set_colored_img(self.initial_img_arr)
        self.set_grayscale_img(self.colored_img_arr)
        self.imgs_selected_text.set(f"Number of selected images: "
                                    f"{len(self.selected_imgs_paths)}")

#todo s radiobtns
    def change_img_preview(self, mod):
        if mod == 1:
            self.active_img = self.colored_img_arr
            cv2.imshow(self.window_name, self.active_img)
        if mod == 2:
            self.active_img = self.adjusted_img_array
            cv2.imshow(self.window_name, self.active_img)

    def undo_last_change(self):
        if self.adjusted_img_array_prev is not None:
            tmp_adj_img_array = self.adjusted_img_array
            self.adjusted_img_array = self.adjusted_img_array_prev
            self.adjusted_img_array_prev = tmp_adj_img_array
            tmp_current_filters = self.used_filters['current'].copy()
            self.used_filters['current'] = self.used_filters['last'].copy()
            self.used_filters['last'] = tmp_current_filters
        if self.radioBtn_prep.isChecked():
            self.active_img = self.adjusted_img_array
        cv2.imshow(self.window_name, self.active_img)

    def reset_image(self):
        self.adjusted_img_array_prev = self.adjusted_img_array
        self.used_filters['last'] = self.used_filters['current'].copy()
        self.set_grayscale_img(self.colored_img_arr)
        self.used_filters['current'] = self.used_filters['current'][0:1]
        if self.radioBtn_prep.isChecked():
            self.active_img = self.adjusted_img_array
        cv2.imshow(self.window_name, self.active_img)

    def set_colored_img(self, new_img_arr):
        self.colored_img_arr = new_img_arr
        self.active_img = self.colored_img_arr

    def set_grayscale_img(self, new_colored_img_arr):
        grayscale_fn = lambda img_array: cv2.cvtColor(img_array,
                                                      cv2.COLOR_BGR2GRAY)
        self.adjusted_img_array = grayscale_fn(new_colored_img_arr)
        self.used_filters['last'] = self.used_filters['current'].copy()
        self.used_filters['current'].append(grayscale_fn)

    def apply_morph(self, morph):
        self.adjusted_img_array_prev = self.adjusted_img_array
        kernel_width = int(self.vs_deWigth.value())
        kernel_height = int(self.vs_deHeight.value())
        iterations = int(self.vs_deIter.value())


        kernel = np.ones((kernel_height, kernel_width), np.uint8)
        if morph == "erosion":
            self.filters["ero_width"].append(kernel_width)
            self.filters["ero_height"].append(kernel_height)
            self.filters["ero_iterations"].append(iterations)
            erosion_fn = lambda img_array: \
                cv2.erode(img_array, kernel, iterations=iterations)
            self.adjusted_img_array = erosion_fn(self.adjusted_img_array)
            self.used_filters['last'] = self.used_filters['current'].copy()
            self.used_filters['current'].append(erosion_fn)
        elif morph == "dilation":
            self.filters["dil_width"].append(kernel_width)
            self.filters["dil_height"].append(kernel_height)
            self.filters["dil_iterations"].append(iterations)
            dilation_fn = lambda img_array: \
                cv2.dilate(img_array, kernel, iterations=iterations)
            self.adjusted_img_array = dilation_fn(self.adjusted_img_array)
            self.used_filters['last'] = self.used_filters['current'].copy()
            self.used_filters['current'].append(dilation_fn)
        self.update_img()
        cv2.imshow(self.window_name, self.active_img)

        #self.img_mode_choice.set(2)

    def update_img(self):
        self.active_img = self.adjusted_img_array

    def apply_canny_edge(self):
        self.adjusted_img_array_prev = self.adjusted_img_array
        threshold1 = int(self.vs_ceTh1.value())
        threshold2 = int(self.vs_ceTh2.value())
        self.filters["ce_th1"].append(threshold1)
        self.filters["ce_th2"].append(threshold2)
        canny_fn = lambda img_array: cv2.Canny(img_array,
                                               threshold1, threshold2)
        self.adjusted_img_array = canny_fn(self.adjusted_img_array)
        self.used_filters['last'] = self.used_filters['current'].copy()
        self.used_filters['current'].append(canny_fn)
        self.update_img()
       # self.img_mode_choice.set(2)

    def apply_threshold(self):
        # THRESH_BINARY = 0
        # THRESH_BINARY_INV = 1
        # THRESH_TRUNC = 2
        # THRESH_TOZERO = 3
        # THRESH_TOZERO_INV = 4
        # THRESH_OTSU = 8
        # THRESH_TRIANGLE = 16
        self.adjusted_img_array_prev = self.adjusted_img_array
        th_type = int(self.comboBox_2.currentIndex())
        th_method = int(self.comboBox.currentIndex())
        self.filters["it_type"].append(th_type)
        self.filters["it_method"].append(th_method)
        self.filters["it_max"].append(int(self.vS_itMax.value()))
        self.filters["it_th"].append(int(self.vS_itth.value()))
        self.filters["it_block"].append(self.vS_itblock.value())
        self.filters["it_Cv"].append(int(self.vS_itCval.value()))

        max_value = int(self.vS_itMax.value())
        # otsu
        if th_type == 5:
            at_type = 8
        # triangle
        elif th_type == 6:
            at_type = 16
        # if pixel has higher than threshold value = pixel will be 255 (white)
        if th_type == 0 or th_type == 1:
            at_fn = lambda img_array: \
                cv2.adaptiveThreshold(img_array, max_value,
                                      th_method, th_type,
                                      int(self.vS_itblock.value()),
                                      int(self.vS_itCval.value()))
            self.adjusted_img_array = at_fn(self.adjusted_img_array)
        else:
            at_fn = lambda img_array: \
                cv2.threshold(img_array, int(self.vS_itth.value()),
                              max_value, cv2.THRESH_BINARY + th_type)
            th, self.adjusted_img_array = at_fn(self.adjusted_img_array)
        self.update_img()
        self.used_filters['last'] = self.used_filters['current'].copy()
        self.used_filters['current'].append(at_fn)
        #self.img_mode_choice.set(2)
        cv2.imshow(self.window_name, self.active_img)

    def apply_gaussian_blur(self):
        self.adjusted_img_array_prev = self.adjusted_img_array
        kernel_width = int(self.vslid_gbwidth.value())
        kernel_height = int(self.vS_gbheight.value())
        sigma = int(self.vS_gbsigma.value())
        self.filters["gb_width"].append(kernel_width)
        self.filters["gb_height"].append(kernel_height)
        self.filters["gb_sigma"].append(sigma)

        gb_fn = lambda img_array: \
            cv2.GaussianBlur(img_array, (kernel_width, kernel_height), sigma)
        self.adjusted_img_array = gb_fn(self.adjusted_img_array)
        self.used_filters['last'] = self.used_filters['current'].copy()
        self.used_filters['current'].append(gb_fn)
        self.update_img()
        cv2.imshow(self.window_name, self.active_img)
        #self.img_mode_choice.set(2)

    def import_params(self):
        path = QFileDialog.getOpenFileName(
            parent=MainWindow,
            caption='Select a data file',
            directory=os.getcwd(),
        )
        path = path[0]
        with open(path) as f:
            self.json_filters = json.load(f)
        print(self.filters)
        #self.apply_json_filters()

    def apply_json_filters(self):
        # gaussian blur
        while (len(self.json_filters.get("gb_width")) > 0):
            self.gb_kwidth_scl.set(int(self.json_filters.get("gb_width").pop(0)))
            self.gb_kheight_scl.set(int(self.json_filters.get("gb_height").pop(0)))
            self.gb_sigma_scl.set(int(self.json_filters.get("gb_sigma").pop(0)))
            self.apply_gaussian_blur()
            print("dictionary  ", self.filters)
            print("json  ", self.json_filters)

    def export_params(self):
        # print(self.filters)
        # json_filters = json.dumps(self.filters)
        # f = open("filters.txt", "a")
        # f.write(json_filters)
        path = QFileDialog.getExistingDirectory(
            self,
            caption='Select a folder'
        )
        with open(os.path.join(path, "params.json"), 'w') as f:
            json.dump(self.filters, f)


    def save_active_img(self):
        preprocessed_imgs = []
        path =  QFileDialog.getExistingDirectory(
            self,
            caption='Select a folder'
        )
        print("toto je cesta: ", path)
        # filename = "/foo/bar/baz.jpg"
        # os.makedirs(os.path.dirname(filename), exist_ok=True)
        c = 0
        for img_filename in self.selected_imgs_paths:
            preprocessed = self.apply_filters_to_img(img_filename)
            preprocessed_imgs.append(preprocessed)
            # result = cv2.imwrite(path + img_filename + "_PREPROCESSED.jpg", preprocessed)
            result = cv2.imwrite(path + "\\image" + str(c) + "_PREPROCESSED.jpg", preprocessed)
            if result == True:
                print("Files saved successfully")
            else:
                print("Files saved unsuccessfully")
            c += 1

    def apply_filters_to_img(self, img_path):
        img = cv2.imread(img_path)
        for filter_fn in self.used_filters['current']:
            img = filter_fn(img)
            # some thresholding methods return tuple with threshold value
            # we want just the image
            if type(img) is tuple:
                img = img[1]
        return img

    def create_img_window(width=680, height=700, name='Image'):
        cv2.namedWindow(name, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
        cv2.resizeWindow(name, width, height)
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
