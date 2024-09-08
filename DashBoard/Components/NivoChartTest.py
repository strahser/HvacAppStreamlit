def _create_nivo_line_chart(table_name: str):
	df = pd.read_sql(f"select * from {table_name}", con=SqlConnector.conn_sql)
	# df['S_ID'] = df['S_ID'].astype("string")
	df = df.fillna("")
	columns_x = df.columns
	numeric_columns = df.select_dtypes(include=np.number).columns.tolist()
	with st.sidebar:
		header = f"#### Select Columns for Line Chart column {table_name.replace('_', ' ').title()}"
		st.markdown(header)
		select_keys_x = st.selectbox(header, columns_x,
		                             key=f"{MenuChapters.dash_board} line chart {table_name} select_keys_x",
		                             label_visibility="collapsed"
		                             )
		select_keys_y = st.selectbox(header, numeric_columns,
		                             key=f"{MenuChapters.dash_board} line chart {table_name} select_keys_y",
		                             label_visibility="collapsed"
		                             )
	
	def _plt_bar():
		grid = make_grid(4, 6)
		fig, ax = plt.subplots()
		ax.bar(df[select_keys_x], df[select_keys_y])
		with grid[0][0]:
			st.write("Max Data")
			df1 = df.groupby(select_keys_x, as_index=False).agg(select_keys_y).max()
			st.write(df1)
		with grid[0][1]:
			i = StringIO()
			fig.savefig(i, format="svg")
			fig_plt = px.bar(df, x=select_keys_x, y=select_keys_y)
			st.write(i.getvalue(), unsafe_allow_html=True)
		with grid[1][0]:
			st.write("Sum Data")
			df1 = df.groupby(select_keys_x, as_index=False).agg(select_keys_y).sum()
			st.write(df1)
		with grid[1][1]:
			st.plotly_chart(fig_plt)
	
	def _plt_scatter():
		grid = make_grid(4, 6)
		df_standard = df[[select_keys_x, select_keys_y]]
		with grid[0][0]:
			st.write("Standard Data")
			st.write(df_standard)
		
		with grid[0][1]:
			fig_plt = px.scatter(df, x=select_keys_x, y=select_keys_y)
			st.plotly_chart(fig_plt)
		with grid[1][0]:
			st.write("Max Data")
			df1 = df.groupby(select_keys_x, as_index=False).agg(select_keys_y).max()
			st.write(df1)
		with grid[1][1]:
			fig_plt = px.scatter(df1, x=select_keys_x, y=select_keys_y)
			st.plotly_chart(fig_plt)