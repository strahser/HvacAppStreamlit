from Session.StatementInit import *
from MultipleApp import MultipleApp
from StaticData.CSS import CssStyle
from StaticData.AppConfig import MenuChapters, MenuIcons
from streamlit_option_menu import option_menu

import streamlit_nested_layout
# pip install git+https://github.com/joy13975/streamlit-nested-layout.git
# icons https://icons.getbootstrap.com/icons/calculator-fill/
# https://bimhvac.streamlit.app/

st.set_page_config(layout="wide")


def create_multiple_app():
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

	def run_upp():
		multy_app = MultipleApp()
		multy_app.create_upload_data()

		for name in MenuChapters.menu_list:
			if getattr(MenuChapters, name) == selected2:
				att = getattr(multy_app, name)
				st.session_state["mainHydralitMenuComplex"] = getattr(MenuChapters, name)
				att()
	run_upp()


StatementInit()
create_multiple_app()
CssStyle.run()
