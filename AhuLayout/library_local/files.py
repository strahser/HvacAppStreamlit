import os, io, zipfile
import pickle
import json
import pandas as pd
import pathlib
from library_hvac_app.pandas import result_to_excel_add_table


def create_tree_folders(root_dir: os.path, subfolders: list = []):
    """return new folders from list of folders names (encloser folders)

    Args:
        root_dir (os.path): base path
        subfolders (list): subpath
    """
    if subfolders:

        for folder_ in subfolders:
            join_path = os.path.join(root_dir, folder_)
            os.makedirs(join_path, exist_ok=True)
        new_path = os.path.join(root_dir, *subfolders)
        return new_path
    else:
        os.makedirs(root_dir, exist_ok=True)
        return root_dir


class Writer:
    def __init__(self, file_path, data) -> None:
        """
        write file to html,json by file path (endwith file extation)
        """
        self.file_path = file_path
        self.data = data

    def write_file(self):
        if self.file_path.endswith(".json"):
            self.to_json()
        elif self.file_path.endswith(".html"):
            self.to_html()
        else:
            print("wrong file format")
        return self.file_path

    def to_json(self):
        with open(self.file_path, "w", encoding="utf-8") as write_file:
            json.dump(self.data, write_file, indent=4, ensure_ascii=False)

    def to_html(self):
        with open(self.file_path, "w", encoding="utf-8") as write_file:
            write_file.writelines('<meta charset="UTF-8">\n')
            write_file.write(self.data)


class Loader:
    def __init__(
        self,
        data_path,
    ) -> None:
        """load json and json to pd.df

        Args:
            data_path (_type_): _description_
        """
        self.data_path = data_path

    def load_json(self):
        with open(self.data_path, "r") as read_file:
            data = json.load(read_file)
        return data

    def load_json_pd(self, idx="S_ID"):
        df = pd.read_json(self.data_path)
        df = df.T
        df = df.rename_axis(idx).reset_index()
        df[idx] = df[idx].astype(str)
        return df


def write_pickle(pickle_file_path: os.path, object_to_save):

    with open(pickle_file_path, "wb") as f:
        pickle.dump(object_to_save, f)


def read_pickle(pickle_file_path: os.path):
    with open(pickle_file_path, "rb") as f:
        data_new = pickle.load(f)
    return data_new


def get_files_by_excitation_in_folder(mydir_: os.path, excitation: str):
    """finde files in folder

    Args:
        mydir_ (str): "/mydir"
        excitation (os.path): ".xlsx"

    Returns:
        _type_: _description_
    """
    file_list = []
    for file_ in os.listdir(mydir_):
        if file_.endswith(excitation):
            excel_file = os.path.join(mydir_, file_)
            file_list.append(excel_file)
    return file_list


def create_folder(directory_path: str):
    pathlib.Path(directory_path).mkdir(parents=True, exist_ok=True)


class DownLoadFoldersCreate:
    def __init__(self, folder_path, suffix='') -> None:
        self.folder_path = f"{folder_path}_{suffix}"
        self.suffix = suffix

    def create_temp_folder(self):
        full_path = os.path.join(self.folder_path)
        create_folder(full_path)
        return full_path

    def create_temp_tree_folder(self, subfolders: list):
        create_tree_folders(self.folder_path, subfolders)

    def create_zip_from_directory(self, folder_path):
        data = io.BytesIO()
        with zipfile.ZipFile(data, mode="w") as zipf:
            for file_to_zip in os.listdir(folder_path):
                file_to_zip_full_path = os.path.join(folder_path, file_to_zip)
                zipf.write(filename=file_to_zip_full_path, arcname=file_to_zip)
        data.seek(0)
        return data

    def create_zip_file_from_temp(self):
        data_file = self.create_zip_from_directory(self.create_temp_folder())
        return data_file


class DownloadDataCreate:
    def __init__(self, data_dict: dict,extantion:str='svg'):
        """save file from dict (file name:file data) 

        Args:
            data_dict (dict): (file name:file data) 
            extantion (str): svg,html
        """
        self.data_dict = data_dict
        self.extantion = extantion

    def save_temp_files_svg_or_html(self, temp_folder):


        for file_key, file_value in self.data_dict.items():
            svg_file_full_name = f"_{file_key}.{self.extantion}"
            svg_path = os.path.join(temp_folder, svg_file_full_name)
            svg_file = open(svg_path, mode="w")
            svg_file.write(file_value)
            svg_file.close()

    def save_temp_files_xls(self):
        excel_file_name = f"Network_pressure_tables_{self.sys_name_prefix}.xlsx"
        excel_path = os.path.join(self.create_temp_folder(), excel_file_name)
        result_to_excel_add_table(self.data_for_saving.get_df_list(), excel_path)
