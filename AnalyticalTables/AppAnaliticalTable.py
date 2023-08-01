from AnalyticalTables.AnalyticalControls.MainAnalyticalTableControl import *
from Upload.UploadLayout import UploadLayout
from StaticData.AppConfig import MenuChapters


def main_analytical_tabel(upload_layout: UploadLayout):
	AnalyticalTableControl(upload_layout, key=MenuChapters.analytics)