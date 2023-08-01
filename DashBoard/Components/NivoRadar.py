def _create_nivo_radar(table_name :str):
	df = pd.read_sql(f"select * from {table_name}", con=SqlConnector.conn_sql)
	numeric_columns = df.select_dtypes(include=np.number).columns.tolist()
	
	with st.sidebar:
		st.markdown(f"#### Select Columns for {table_name.replace('_' ,' ').title()}")
		select_keys = st.multiselect(f"Columns for {table_name}" ,numeric_columns,
		                             default=numeric_columns[0],
		                             key=f"{MenuChapters.dash_board} radar chart {table_name} select_keys",
		                             label_visibility="collapsed"
		                             )
	data = df.to_dict("records")
	try:
		with mui.Paper(key=f"Chart of {table_name}",
		               sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"},
		               elevation=1):
			_create_title_for_paper(table_name)
			nivo.Radar(
				data=data,
				keys=select_keys,
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
	except Exception as e:
		st.error(e)