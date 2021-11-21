import os
import tkinter as tk
import cv2
import numpy as np
import threading

from tkinter import messagebox
from tkinter.filedialog import askopenfilename, askdirectory

from PyQt5.QtWidgets import QFileDialog

import json


def create_img_window(width=680, height=700, name='Image'):
    cv2.namedWindow(name, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow(name, width, height)


class Preprocessing(object):
    def __init__(self):
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

    def set_initial_img(self, init_img_path):
        self.selected_imgs_paths = [init_img_path]
        self.initial_img_arr = cv2.imread(init_img_path)
        self.set_colored_img(self.initial_img_arr)
        self.set_grayscale_img(self.colored_img_arr)
        self.imgs_selected_text.set(f"Number of selected images: "
                                    f"{len(self.selected_imgs_paths)}")

    def change_img_preview(self):
        if self.img_mode_choice.get() == 1:
            self.active_img = self.colored_img_arr
        else:
            self.active_img = self.adjusted_img_array

    def undo_last_change(self):
        if self.adjusted_img_array_prev is not None:
            tmp_adj_img_array = self.adjusted_img_array
            self.adjusted_img_array = self.adjusted_img_array_prev
            self.adjusted_img_array_prev = tmp_adj_img_array
            tmp_current_filters = self.used_filters['current'].copy()
            self.used_filters['current'] = self.used_filters['last'].copy()
            self.used_filters['last'] = tmp_current_filters
        if self.img_mode_choice.get() == 2:
            self.active_img = self.adjusted_img_array

    def reset_image(self):
        self.adjusted_img_array_prev = self.adjusted_img_array
        self.used_filters['last'] = self.used_filters['current'].copy()
        self.set_grayscale_img(self.colored_img_arr)
        self.used_filters['current'] = self.used_filters['current'][0:1]
        if self.img_mode_choice.get() == 2:
            self.active_img = self.adjusted_img_array

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
        kernel_width = int(self.dil_ero_kwidth_scl.get())
        kernel_height = int(self.dil_ero_kheight_scl.get())
        iterations = int(self.dil_ero_iter_scl.get())
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
        self.img_mode_choice.set(2)

    def update_img(self):
        self.active_img = self.adjusted_img_array

    def apply_canny_edge(self):
        self.adjusted_img_array_prev = self.adjusted_img_array
        threshold1 = int(self.canny_thrsh1_scl.get())
        threshold2 = int(self.canny_thrsh2_scl.get())
        self.filters["ce_th1"].append(threshold1)
        self.filters["ce_th2"].append(threshold2)
        canny_fn = lambda img_array: cv2.Canny(img_array,
                                               threshold1, threshold2)
        self.adjusted_img_array = canny_fn(self.adjusted_img_array)
        self.used_filters['last'] = self.used_filters['current'].copy()
        self.used_filters['current'].append(canny_fn)
        self.update_img()
        self.img_mode_choice.set(2)

    def apply_threshold(self):
        # THRESH_BINARY = 0
        # THRESH_BINARY_INV = 1
        # THRESH_TRUNC = 2
        # THRESH_TOZERO = 3
        # THRESH_TOZERO_INV = 4
        # THRESH_OTSU = 8
        # THRESH_TRIANGLE = 16
        self.adjusted_img_array_prev = self.adjusted_img_array
        at_type = self.at_type_cb.current()
        self.filters["it_type"].append(at_type)
        # todo pozriet return type self.at_method_cb
        self.filters["it_method"].append(self.at_method_cb.get())
        self.filters["it_max"].append(int(self.at_max_val_scl.get()))
        self.filters["it_th"].append(int(self.at_thrsh_val_scl.get()))
        self.filters["it_block"].append(self.at_block_size_scl.get())
        self.filters["it_Cv"].append(int(self.at_c_scl.get()))

        max_value = int(self.at_max_val_scl.get())
        # otsu
        if at_type == 5:
            at_type = 8
        # triangle
        elif at_type == 6:
            at_type = 16
        # if pixel has higher than threshold value = pixel will be 255 (white)
        if at_type == 0 or at_type == 1:
            at_fn = lambda img_array: \
                cv2.adaptiveThreshold(img_array, max_value,
                                      self.at_method_cb.current(), at_type,
                                      int(self.at_block_size_scl.get()),
                                      int(self.at_c_scl.get()))
            self.adjusted_img_array = at_fn(self.adjusted_img_array)
        else:
            at_fn = lambda img_array: \
                cv2.threshold(img_array, int(self.at_thrsh_val_scl.get()),
                              max_value, cv2.THRESH_BINARY + at_type)
            th, self.adjusted_img_array = at_fn(self.adjusted_img_array)
        self.update_img()
        self.used_filters['last'] = self.used_filters['current'].copy()
        self.used_filters['current'].append(at_fn)
        self.img_mode_choice.set(2)

    def apply_gaussian_blur(self):
        self.adjusted_img_array_prev = self.adjusted_img_array
        kernel_width = int(self.gb_kwidth_scl.get())
        kernel_height = int(self.gb_kheight_scl.get())
        sigma = int(self.gb_sigma_scl.get())
        self.filters["gb_width"].append(kernel_width)
        self.filters["gb_height"].append(kernel_height)
        self.filters["gb_sigma"].append(sigma)

        gb_fn = lambda img_array: \
            cv2.GaussianBlur(img_array, (kernel_width, kernel_height), sigma)
        self.adjusted_img_array = gb_fn(self.adjusted_img_array)
        self.used_filters['last'] = self.used_filters['current'].copy()
        self.used_filters['current'].append(gb_fn)
        self.update_img()
        self.img_mode_choice.set(2)

    def import_params(self):
        with open('data.json') as f:
            self.json_filters = json.load(f)
        print(self.filters)
        self.apply_json_filters()

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
        with open('data.json', 'w') as f:
            json.dump(self.filters, f)

    def apply_and_save(self):
        all_imgs_path = "resources/dataset/"
        for img_filename in self.selected_imgs_paths:
            img_path = all_imgs_path + img_filename
            save_path = os.path.dirname(__file__) + \
                        "/resources/dataset_preprocessed/"
            img = self.apply_filters_to_img(img_path)
            cv2.imwrite(save_path + img_filename, img)

    def save_active_img(self):
        preprocessed_imgs = []
        path = askdirectory()
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


    def select_imgs(self):
        selected_imgs_paths = list(tk.filedialog.askopenfilenames(
        initialdir=os.path.join(
                 os.path.dirname(os.path.realpath(__file__))),
        title="Select file",
        filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*"))))
        if selected_imgs_paths:
            self.selected_imgs_paths = selected_imgs_paths
            self.adjusted_img_array_prev = None
            self.imgs_selected_text.set(f"Number of selected images: "
                                        f"{len(self.selected_imgs_paths)}")
            img = cv2.imread(self.selected_imgs_paths[0])
            self.used_filters['current'] = []
            self.used_filters['last'] = []
            self.set_colored_img(img)
            self.set_grayscale_img(img)
            self.img_mode_choice.set(1)
            if cv2.getWindowProperty('Image', 0) != 0:
                create_img_window(680, 700, 'Image')
                threading.Thread(target=self.update_opencv_img,
                                 daemon=True).start()

    def on_closing(self):
        if tk.messagebox.askokcancel("Exit", "Do you really want to quit?"):
            self.root_window.destroy()

    def start_gui(self):
        if self.initial_img_arr is not None:
            create_img_window(680, 700, 'Image')
            threading.Thread(target=self.update_opencv_img,
                             daemon=True).start()
        self.root_window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root_window.mainloop()

    def update_opencv_img(self):
        if not self.selected_imgs_paths:
            return
        if cv2.getWindowProperty('Image', 0) >= 0:
            cv2.imshow("Image", self.active_img)
            self.root_window.after(100, self.update_opencv_img)

    def getFileNames(self, parent):
        file_filter = 'Data File (*.jpeg *.jpg *.tif);; Excel File (*.jpeg *.jpg)'
        response = QFileDialog.getOpenFileNames(
            parent=parent,
            caption='Select a data file',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter='Excel File (*.jpeg *.jpg)'
        )
        print(response)


