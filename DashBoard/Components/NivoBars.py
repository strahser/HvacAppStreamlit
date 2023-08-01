
def _plt_bar():
	df1 = df.groupby(select_keys_x, as_index=False).agg(select_keys_y).sum()
	col1, col2 = st.columns([4, 12])
	with col1:
		st.write(df1)
	with col2:
		fig_plt = px.line(df1, x=select_keys_x, y=select_keys_y)
		st.plotly_chart(fig_plt)
		
	with mui.Paper(key=f" Line Chart of {table_name}",
	               sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"},
	               elevation=1):
			# max_y = float(df[select_keys_y].max())
			_create_title_for_paper(table_name)
			data = [{"x":x_key,"v":y_key }for x_key,y_key in zip(df[select_keys_x],df[select_keys_y])]
			nivo.Bar(
			id=f"{MenuChapters.dash_board} line chart {table_name}",
				width=500,
			height = 400,
			data = data,
			keys = ["v"],
			# maxValue = max_y,
			padding = 0.6,
			margin = {
				"top": 10,
				"right": 10,
				"bottom": 36,
				"left": 36
			},
			indexBy = "x",
			borderRadius = 2,
		)