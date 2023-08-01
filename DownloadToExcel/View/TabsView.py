import streamlit as st


class TabsView:
	def __init__(self):
		self.balance_view_tab, self.download_view_tab, self.other_category_tab = st.tabs(
			["Balance View","Download", "Other Category"]
		)

