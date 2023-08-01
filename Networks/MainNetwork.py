import os
import inspect
import sys
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, root_dir)

from Upload.UploadLayout import UploadLayout
from Networks.ControlNetwork.NetworkPressureLayout import *

def create_network_plote(upload_layout:UploadLayout):
    if (
        upload_layout.revit_file_upload
        and upload_layout.file_json_upload
        and upload_layout.setting_file_upload
    ):
        upload_layout.get_files_from_memory()
        main_network = NetworkPressureLayout(
            upload_layout.revit_export,
            upload_layout.json_file,
            upload_layout.medium_property,
        )
        show_network = st.button("Show Network")
        if show_network:
            main_network.create_df_and_plote_layout()
