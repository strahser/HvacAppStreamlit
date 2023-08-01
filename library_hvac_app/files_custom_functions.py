import os,io, zipfile
import pickle
import json
import pandas as pd
from Polygons.PolygonPlot.PolygonMergeStatic import MergedIdProperty

def create_zip_from_directory(file_path):
    data = io.BytesIO()
    with zipfile.ZipFile(data, mode='w') as zipf:
        for file_to_zip in os.listdir(file_path):
            file_to_zip_full_path = os.path.join(file_path, file_to_zip)
            zipf.write(filename=file_to_zip_full_path, arcname=file_to_zip)
    data.seek(0)
    return data

def create_tree_folders(root_dir:os.path,subfolders:list=[]):
    """return new folders from list of folders names (encloser folders)

    Args:
        root_dir (os.path): base path
        subfolders (list): subpath
    """
    if subfolders:

        for folder_ in subfolders:
            join_path = os.path.join(root_dir,folder_)
            os.makedirs(join_path,exist_ok=True)
        new_path = os.path.join(root_dir,*subfolders)
        return new_path
    else:
        os.makedirs(root_dir,exist_ok=True)
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
        with open(self.file_path, "w", encoding='utf-8') as write_file:
            json.dump(self.data, write_file, indent=4, ensure_ascii=False)

    def to_html(self):
        with open(self.file_path, "w", encoding="utf-8") as write_file:
            write_file.writelines('<meta charset="UTF-8">\n')
            write_file.write(self.data)


class Loader:
    def __init__(self, data_path,idx=MergedIdProperty.json_id) -> None:
        """load json and json to pd.df

        Args:
            data_path (_type_): _description_
        """
        self.data_path = data_path
        self.idx = idx

    def load_json(self):
        with open(self.data_path, "r") as read_file:
            data = json.load(read_file)
        return data

    def load_json_pd(self, idx='S_ID'):
        if isinstance(self.data_path, dict):
            df = pd.DataFrame.from_dict(self.data_path)
        else:
            df = pd.read_json(self.data_path)
        df = df.T
        df = df.rename_axis(idx).reset_index()
        df[self.idx] = df[self.idx].astype(str)
        return df


def write_pickle_save(pickle_file_path: os.path,object_to_save):

    with open(pickle_file_path, 'wb') as f:
        pickle.dump(object_to_save, f)


def write_pickle_read(pickle_file_path:os.path):
    with open(pickle_file_path, 'rb') as f:
        data_new = pickle.load(f)
    return data_new


def get_files_by_excitation_in_folder(mydir_:os.path,excitation:str):
    """find files in folder

    Args:
        mydir_ (str): "/mydir"
        excitation (os.path): ".xlsx"

    Returns:
        _type_: _description_
    """
    file_list = []
    for file_ in os.listdir(mydir_):
        if file_.endswith(excitation):
            excel_file =  os.path.join(mydir_, file_)
            file_list.append(excel_file)
    return file_list
