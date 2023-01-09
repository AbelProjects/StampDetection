import os
import shutil
import image_utils
from pdf_classes import PdfObject
from image_classes import ImageObject
from pathlib import Path


class FolderEngine:

    def __init__(self, folder_path: str):
        """

        :param folder_path: absolute path with pdf documents
        """
        self.folder_path = folder_path
        pathlist = Path(self.folder_path).rglob('*.pdf')
        self.pdf_docs = {}

        for pdf_path in pathlist:
            pdf_name = doc_name = str(pdf_path).split(os.sep)[-1]
            self.pdf_docs[pdf_name] = PdfObject(str(pdf_path))

        self.is_fitted_stamp = False


    def find_stamps(self):
        """
        This fucntion finds stamps in all pdf documents in folder
        :return: None
        """
        for pdf_name in self.pdf_docs.keys():
            self.pdf_docs[pdf_name].find_stamps()
        self.is_fitted_stamp = True


    def make_stamp_folders(self, folders_path: str = None,
                         folder_stamped_name: str = 'stamped',
                         folder_not_stamped_name: str = 'not_stamped',
                         move_files=False) -> None:
        """

        :param folders_path: absolute path to place where 2 folders will be maked
        :param folder_stamped_name: name of folder with stamped files
        :param folder_not_stamped_name: name of folder with not stamped files
        :return:
        """

        self._create_folders(folders_path=folders_path,
                             folder_stamped_name=folder_stamped_name,
                             folder_not_stamped_name = folder_not_stamped_name)
        if not self.is_fitted_stamp:
            self.find_stamps()

        self._move_or_copy_all_files_by_stamp(move_files)


    def _create_folders(self, folders_path: str = None,
                         folder_stamped_name: str = 'stamped',
                         folder_not_stamped_name: str = 'not_stamped') -> None:
        if not folders_path:
            folders_path = self.folder_path
        self.folder_stamped_path = os.path.join(folders_path,folder_stamped_name)
        self.folder_not_stamped_path = os.path.join(folders_path, folder_not_stamped_name)
        Path(self.folder_stamped_path).mkdir(parents=True, exist_ok=True)
        Path(self.folder_not_stamped_path).mkdir(parents=True, exist_ok=True)


    def _copy_file_by_stamp(self, file_name: str) -> None:
        file_source = os.path.join(self.folder_path, file_name)
        file_dst_folder = self.folder_stamped_path if self.pdf_docs[file_name].stamp_flg else self.folder_not_stamped_path
        file_dst = os.path.join(file_dst_folder, file_name)
        shutil.copyfile(src=file_source, dst=file_dst)

    def _move_file_by_stamp(self, file_name: str) -> None:
        file_source = os.path.join(self.folder_path, file_name)
        file_dst_folder = self.folder_stamped_path if self.pdf_docs[file_name].stamp_flg else self.folder_not_stamped_path
        file_dst = os.path.join(file_dst_folder, file_name)
        shutil.move(file_source, file_dst)

    def _copy_all_files_by_stamp(self):
        for file_name in self.pdf_docs.keys():
            self._copy_file_by_stamp(file_name)

    def _move_all_files_by_stamp(self):
        for file_name in self.pdf_docs.keys():
            self._move_file_by_stamp(file_name)

    def _move_or_copy_all_files_by_stamp(self, move_files):
        if move_files:
            self._move_all_files_by_stamp()
        else:
            self._copy_all_files_by_stamp()
