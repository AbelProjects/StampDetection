import numpy as np
import pdf2image
from image_classes import ImageObject
from functools import reduce
import cv2


class PdfObject:

    def __init__(self, file_path: str):
        if file_path.split('.')[-1].lower() == 'pdf':
            self.file_path = file_path
        else:
            raise ValueError(f'{file_path} is not a pdf file!')
        self.images = None
        self.is_fitted_stamp = False
        self.stamp_flg = None

    def get_images(self):
        pages = pdf2image.convert_from_path(self.file_path)
        images = {}
        for i in range(len(pages)):
            img = np.asarray(pages[i])
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            images[i] = ImageObject(matrix=img)
        self.images = images

    def find_stamps(self):
        for key in self.images.keys():
            self.images[key].find_stamps()
        self.is_fitted_stamp = True
        self.stamp_flg = reduce(lambda x, y: x or y, [x.stamp_flg for x in self.images.values()])

