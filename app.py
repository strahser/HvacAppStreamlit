import streamlit as st
from Session.StatementInit import StatementInit
from StaticData.CSS import CssStyle
from StaticData.AppConfig import MenuChapters, MenuIcons
from streamlit_option_menu import option_menu
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
from Networks.MainNetwork import create_network_plot
import streamlit_nested_layout


# pip install git+https://github.com/joy13975/streamlit-nested-layout.git
# icons https://icons.getbootstrap.com/icons/calculator-fill/
# https://bimhvac.streamlit.app/


class MultipleApp:
	def __init__(self):
		self.condition_excel = self._check_db_exist()

	def create_upload_data(self):
		with st.expander("__Input data show__."):
			upload_view = UploadView()
			upload_view.get_upload_layout()
			self.upload_layout = UploadLayout(upload_view)
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
			st.warning("no loaded file json polygons or excel files")

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

	def download(self):
		UploadSessionSettingControl.load_session_download()
		if self.condition_excel:
			DownloadControl(self.upload_layout)


def create_multiple_app():
	StatementInit()
	selected2 = option_menu(
		"HVAC BIM SOLUTION",
		options=MenuChapters.get_buttons(),
		icons=MenuIcons.get_icons(),
		menu_icon="cast",
		default_index=0,
		orientation="horizontal",
		styles=CssStyle.menu_styles
	)
	st.session_state["previous_view"] = selected2
	multy_app = MultipleApp()
	multy_app.create_upload_data()
	for name in MenuChapters.menu_list:
		if getattr(MenuChapters, name) == selected2:
			att = getattr(multy_app, name)
			st.session_state["mainHydralitMenuComplex"] = getattr(MenuChapters, name)
			att()


create_multiple_app()
CssStyle.run()
