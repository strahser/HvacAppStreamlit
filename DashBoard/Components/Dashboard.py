from streamlit_elements import dashboard, mui, html, nivo, sync, event, elements
import streamlit as st

from Session.StatementConfig import StatementConstants


def handle_layout_change(updated_layout):
	# print(updated_layout)
	st.session_state[StatementConstants.CardDimensions] = updated_layout
	return updated_layout


class DashboardLayout:
	def __init__(self, list_off: list[str]):
		self._list_off = list_off
		self.layout = self._create_layout()

	def _create_layout(self):
		if st.session_state[StatementConstants.CardDimensions]:
			layout = [dashboard.Item(**val) for val in st.session_state[StatementConstants.CardDimensions]]
			return layout
		else:
			layout = [
				# Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
				dashboard.Item(
					name, 0, 0, 3, 1, isDraggable=True, moved=True, isResizable=True
				) for name in self._list_off

			]
			return layout


def create_dashboard(layout: DashboardLayout, dashboard_name: str = "dashboard1"):
	with elements(dashboard_name):
		with dashboard.Grid(layout.layout, onLayoutChange=handle_layout_change):
			for name in layout.layout:
				_create_paper(name)
			if radar_chart_choosing:
				for name in radar_chart_choosing:
					_create_card(name)
