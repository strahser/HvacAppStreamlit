import streamlit as st
from Session.AutoloadSession import AutoloadSession
from Session.UploadSessionSettingControl import UploadSessionSettingControl
from Session.StatementConfig import StatementConstants
from Upload.UploadView import UploadView
from Upload.UploadLayout import UploadLayout
from DashBoard.DashBoardMain_ import dashboard_main
from AnalyticalTables.AppAnaliticalTable import main_analytical_tabel
from Polygons.PolygonApp import polygon_main
from PrincipalSchems.ViewControls import SchemeMain
from IFC.Homepage import main as ifc_main
from InsertTerminalsPandas.AppInsertTerminals import insert_terminals_main
from AhuLayout.AppAhuLayout import MainAHU
from DownloadToExcel.Control.DownloadControl import DownloadControl
from StaticData.AppConfig import MenuChapters
from Networks.MainNetwork import create_network_plot


class MultipleApp:
	def __init__(self):
		self.condition_excel = self._check_db_exist()

	def create_upload_data(self):
		with st.expander("__Input data show__."):
			self.upload_view = UploadView()
			self.upload_view.get_upload_layout()
			self.upload_layout = UploadLayout(self.upload_view)
			self.upload_layout.get_files_from_memory()
			self.condition_json = self.upload_layout.json_file
			AutoloadSession.autoload()

	@staticmethod
	def _check_db_exist():
		if st.session_state[StatementConstants.table_db][StatementConstants.all_tables_db]:
			return True

	def dash_board(self):
		tab1, tab2 = st.tabs(["Dashboard", "SQL"])
		with tab1:
			dashboard_main(self.upload_layout)
		with tab2:
			if self.condition_excel:
				main_analytical_tabel(self.upload_layout)

	def Networks(self):
		create_network_plot(self.upload_layout, key=MenuChapters.Networks)

	@staticmethod
	def ifc_dash_board():
		ifc_main()

	def polygons(self):
		if self.condition_excel and self.condition_json:
			polygon_main(self.upload_layout, key=MenuChapters.polygons)
		else:
			st.warning("no loaded file json polygons")

	def scheme(self):
		if self.condition_excel and self._check_db_exist:
			schem_main = SchemeMain(self.upload_layout, key=MenuChapters.scheme)
			schem_main.main()

	def ahu(self):
		MainAHU(self.upload_layout, key=MenuChapters.ahu)

	def terminals(self):
		if self.condition_excel and self.condition_json:
			insert_terminals_main(self.upload_layout, key=MenuChapters.terminals)
		else:
			st.warning("no loaded file json polygons")

	def analytics(self):
		if self.condition_excel:
			main_analytical_tabel(self.upload_layout)

	def download(self):
		UploadSessionSettingControl.load_session_download()
		if self.condition_excel:
			DownloadControl(self.upload_layout)

# def hydralit_style_app():
# 	app = hy.HydraApp(title="HVAC BIM SOLUTION")
# 	multy_app = MultipleApp()
# 	multy_app.create_upload_data()

# 	@app.addapp(title=MenuChapters.input_data, icon=MenuIcons.input_data)
# 	def input_data():
# 		multy_app.session_data()

# 	@app.addapp(title=MenuChapters.ifc_dash_board, icon=MenuIcons.polygons)
# 	def polygons():
# 		multy_app.ifc_dash_board()

# 	@app.addapp(title=MenuChapters.polygons, icon=MenuIcons.polygons)
# 	def polygons():
# 		multy_app.polygons()

# 	@app.addapp(title=MenuChapters.scheme, icon=MenuIcons.scheme)
# 	def scheme():
# 		multy_app.scheme()

# 	@app.addapp(title=MenuChapters.ahu, icon=MenuIcons.ahu)
# 	def ahu():
# 		multy_app.ahu()

# 	@app.addapp(title=MenuChapters.terminals, icon=MenuIcons.terminals)
# 	def terminals():
# 		multy_app.terminals()

# 	@app.addapp(title=MenuChapters.analytics, icon=MenuIcons.analytics)
# 	def analytics():
# 		multy_app.analytics()

# 	@app.addapp(title=MenuChapters.download, icon=MenuIcons.download)
# 	def download():
# 		multy_app.download()

# 	app.run()
