import streamlit as st


class ExceptionWriter:
	def exception_name_and_flow(self=None):
		st.error(f"No flow in space! {self}")

	def exception_wall_offset(data=None):
		st.error(f"wrong polygon offset! \n {data}")
