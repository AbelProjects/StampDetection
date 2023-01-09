import numpy as np
from numpy import ndarray
import cv2
import image_utils


class ImageObject:

    def __init__(self, matrix: ndarray = None, file_path: str = None):
        if file_path:
            matrix: ndarray = cv2.imread(file_path)
            if matrix is not None:
                self.file_path = file_path
                self.matrix = matrix
            else:
                raise ValueError("File doesn't exists or not supported")

        elif matrix is not None:
            if isinstance(matrix, ndarray):
                self.matrix = matrix
                self.file_path = None
            else:
                raise TypeError('matrix parameter should has ndarray type')

        else:
            raise ValueError("Can't create Image Class without inputs")
        self.is_fitted_stamp = False
        self.circles = None
        self.stamp_flg = None
        self.boxes = None

    def save_image(self, file_path: str) -> None:
        cv2.imwrite(file_path, self.matrix)

    def show_image(self):
        image_utils.image_imshow(self.matrix)

    def find_stamps(self) -> None:
        self.circles = image_utils.image_find_stamps(self.matrix)
        self.is_fitted_stamp = True
        self.stamp_flg = image_utils.is_stamped_from_circles(self.circles)
        self.boxes = image_utils.squares_from_circles(self.circles)

    def show_stamp_image(self):
        if self.circles is None:
            raise ValueError("Please find stamps before show them")
        image_utils.image_imshow(image_utils.image_draw_circles(self.matrix, self.circles))


