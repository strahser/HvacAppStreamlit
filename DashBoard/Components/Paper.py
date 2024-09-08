from streamlit_elements import dashboard, mui, html, nivo


def _create_title_for_paper(table_name):
	mui.Typography(table_name,
	               variant="h5",
	               align="center",
	               css={
		               "backgroundColor": "hotpink",
		               "&:hover": {
			               "color": "lightgreen"
		               },
	               },
	               )
