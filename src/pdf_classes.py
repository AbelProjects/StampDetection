import numpy as np
from image_classes import ImageObject
from functools import reduce
import cv2
import os
import fitz
from imageio.v2 import imread


class PdfObject:

    def __init__(self, file_path: str):
        if file_path.split('.')[-1].lower() == 'pdf':
            self.file_path = file_path
        else:
            raise ValueError(f'{file_path} is not a pdf file!')
        self.images = {}
        self.is_fitted_stamp = False
        self.stamp_flg = None

    def get_images(self):
        dpi = 200 
        zoom = dpi / 72
        magnify = fitz.Matrix(zoom, zoom) 
        doc = fitz.open(self.file_path)
        images = {}
        for page in doc:
            pix = page.get_pixmap(matrix=magnify)  
            pix.save(f"page-{page.number}.png")
            img = imread(f"page-{page.number}.png")
            img = np.asarray(img)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            images[page.number] = ImageObject(matrix=img)
            os.remove(f"page-{page.number}.png")
        self.images = images

    def find_stamps(self):
        if not self.images:
            self.get_images()
        for key in self.images.keys():
            self.images[key].find_stamps()
        self.is_fitted_stamp = True
        self.stamp_flg = reduce(lambda x, y: x or y, [x.stamp_flg for x in self.images.values()])
        self.n_stamps = reduce(lambda x, y: x + y, [x.n_stamps for x in self.images.values()])

