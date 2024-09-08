from streamlit_elements import dashboard, mui, html, nivo,sync, event
from DashBoard.Components.Paper import _create_title_for_paper
def _create_card(table_name):
	with mui.Card(key="test",
	              sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"},
	              elevation=3):
		mui.CardHeader(
			title="TITLE",
			subheader="subhider",
			avatar=mui.Avatar("MBS", sx={"bgcolor": "red"}),
			action=mui.IconButton(mui.icon.MoreVert),
			className="draggable",
		)
	
def _create_card_media(table_name):
	with mui.Paper(key=f"Chart of {table_name}",
	               sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"},
	               elevation=1):
		_create_title_for_paper(table_name)
		mui.CardMedia(
			component="img",
			image=f"data:image/jpeg;base64,{_create_chart_from_df(table_name)}",
			alt="Where you save image wtf?",
		)