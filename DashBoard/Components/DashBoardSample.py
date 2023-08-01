from uuid import uuid4
from abc import ABC, abstractmethod
from streamlit_elements import dashboard, mui, html, nivo
from contextlib import contextmanager
from streamlit import session_state as state
from streamlit_elements import elements, sync, event
from types import SimpleNamespace
from Upload.Session.StatementConfig import StatementConstants
import streamlit as st
from SQL.SqlModel.SqlConnector import SqlConnector
import pandas as pd

def _create_dashboard_grid(table_name: str):
	columns, rows = get_db_table(table_name)

	def _handle_edit(params):
		print(params)

	with mui.Paper(key=table_name,
	               sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"},
	               elevation=1):
		mui.Typography(table_name,
		               variant="h5",
		               css={
			               "backgroundColor": "hotpink",
			               "&:hover": {
				               "color": "lightgreen"
			               },
		               },
		               align="center"
		               )
		mui.DataGrid(
			columns=columns,
			rows=rows,
			pageSize=5,
			rowsPerPageOptions=[6],
			checkboxSelection=True,
			disableSelectionOnClick=False,
			onCellEditCommit=_handle_edit,

		)

def _create_dashboard_card():
	with mui.Card(key="test",
	              sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"},
	              elevation=3):
		mui.CardHeader(
			title="Shrimp and Chorizo Paella",
			subheader="September 14, 2016",
			avatar=mui.Avatar("MBS", sx={"bgcolor": "red"}),
			action=mui.IconButton(mui.icon.MoreVert),
			className="draggable",
		)

		with mui.CardContent(sx={"flex": 1}):
			mui.Typography("test")

		mui.CardMedia(
			component="img",
			height=194,
			image="https://mui.com/static/images/cards/paella.jpg",
			alt="Paella dish",
		)

def _create_nivo_card():
	DATA = [
		{"taste": "fruity", "chardonay": 93, "carmenere": 61, "syrah": 114},
		{"taste": "bitter", "chardonay": 91, "carmenere": 37, "syrah": 72},
		{"taste": "heavy", "chardonay": 56, "carmenere": 95, "syrah": 99},
		{"taste": "strong", "chardonay": 64, "carmenere": 90, "syrah": 30},
		{"taste": "sunny", "chardonay": 119, "carmenere": 94, "syrah": 103},
	]
	keys = ["chardonay", "carmenere", "syrah"],
	with mui.Box(sx={"height": 500}):
		nivo.Radar(
			data=DATA,
			keys=keys,
			indexBy="taste",
			valueFormat=">-.2f",
			margin={"top": 70, "right": 80, "bottom": 40, "left": 80},
			borderColor={"from": "color"},
			gridLabelOffset=36,
			dotSize=10,
			dotColor={"theme": "background"},
			dotBorderWidth=2,
			motionConfig="wobbly",
			legends=[
				{
					"anchor": "top-left",
					"direction": "column",
					"translateX": -50,
					"translateY": -40,
					"itemWidth": 80,
					"itemHeight": 20,
					"itemTextColor": "#999",
					"symbolSize": 12,
					"symbolShape": "circle",
					"effects": [
						{
							"on": "hover",
							"style": {
								"itemTextColor": "#000"
							}
						}
					]
				}
			],
			theme={
				"background": "#FFFFFF",
				"textColor": "#31333F",
				"tooltip": {
					"container": {
						"background": "#FFFFFF",
						"color": "#31333F",
					}
				}
			}
		)


class Dashboard:
	DRAGGABLE_CLASS = "draggable"

	def __init__(self):
		self._layout = []

	def _register(self, item):
		self._layout.append(item)

	@contextmanager
	def __call__(self, **props):
		# Draggable classname query selector.
		props["draggableHandle"] = f".{Dashboard.DRAGGABLE_CLASS}"

		with dashboard.Grid(self._layout, **props):
			yield

	class Item(ABC):

		def __init__(self, board, x, y, w, h, **item_props):
			self._key = str(uuid4())
			self._draggable_class = Dashboard.DRAGGABLE_CLASS
			self._dark_mode = True
			board._register(dashboard.Item(self._key, x, y, w, h, **item_props))

		def _switch_theme(self):
			self._dark_mode = not self._dark_mode

		@contextmanager
		def title_bar(self, padding="5px 15px 5px 15px", dark_switcher=True):
			with mui.Stack(
					className=self._draggable_class,
					alignItems="center",
					direction="row",
					spacing=1,
					sx={
						"padding": padding,
						"borderBottom": 1,
						"borderColor": "divider",
					},
			):
				yield

				if dark_switcher:
					if self._dark_mode:
						mui.IconButton(mui.icon.DarkMode, onClick=self._switch_theme)
					else:
						mui.IconButton(mui.icon.LightMode, sx={"color": "#ffc107"}, onClick=self._switch_theme)

		@abstractmethod
		def __call__(self):
			"""Show elements."""
			raise NotImplementedError


class Card(Dashboard.Item):
	DEFAULT_CONTENT = (
		"This impressive paella is a perfect party dish and a fun meal to cook "
		"together with your guests. Add 1 cup of frozen peas along with the mussels, "
		"if you like."
	)

	def __call__(self, content):
		with mui.Card(key=self._key,
		              sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"},
		              elevation=1):
			mui.CardHeader(
				title="Shrimp and Chorizo Paella",
				subheader="September 14, 2016",
				avatar=mui.Avatar("MBS", sx={"bgcolor": "red"}),
				action=mui.IconButton(mui.icon.MoreVert),
				className=self._draggable_class,
			)
			mui.CardMedia(
				component="img",
				height=194,
				image="https://mui.com/static/images/cards/paella.jpg",
				alt="Paella dish",
			)

			with mui.CardContent(sx={"flex": 1}):
				mui.Typography(content)


class DataGrid(Dashboard.Item):

	def _handle_edit(self, params):
		print(params)

	def __call__(self, columns, rows):
		# try:
		# 	data = json.loads(json_data)
		# except json.JSONDecodeError:
		# 	data = self.DEFAULT_ROWS

		with mui.Paper(key=self._key,
		               sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"},
		               elevation=1):
			with self.title_bar(padding="10px 15px 10px 15px", dark_switcher=False):
				mui.icon.ViewCompact()
				mui.Typography("Data grid")
			with mui.Box(sx={"flex": 1, "minHeight": 0}):
				mui.DataGrid(
					columns=columns,
					rows=rows,
					pageSize=5,
					rowsPerPageOptions=[5],
					checkboxSelection=True,
					disableSelectionOnClick=True,
					onCellEditCommit=self._handle_edit,
				)


def MainDashBoard():
	st.title("Main Dashboard")
	if not state[StatementConstants.SimpleNamespace]:
		board = Dashboard()
		w = SimpleNamespace(
			data_grid=DataGrid(board, 6, 13, 6, 7, minH=4),
			dashboard=board,
			card=Card(board, 6, 7, 3, 7, minW=2, minH=4),
		)
		state[StatementConstants.SimpleNamespace] = w
	else:
		w = state[StatementConstants.SimpleNamespace]
	with elements("Main"):
		event.Hotkey("ctrl+s", sync(), bindInputs=True, overrideDefault=True)
		with w.dashboard(rowHeight=57):
			w.data_grid(*get_db_table("revit_export"))
			w.card("Card")


def get_db_table(table_name: str):
	df = pd.read_sql(f"select * from {table_name}", con=SqlConnector.conn_sql)
	df["id"] = df.index
	columns = [{"field": col} for col in df.columns]
	rows = df.to_dict("records")
	return columns, rows
