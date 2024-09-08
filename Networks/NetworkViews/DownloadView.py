import zipfile
import io
import streamlit as st
from Networks.PloteNetwork.PlotDataFromSession import create_data_frame_from_session, create_svg_from_session
from Networks.Render.Render import render_jinja_template, render_word_template
from library_hvac_app.DbFunction.pandas_custom_function import df_to_excel_in_memory

from library_hvac_app.list_custom_functions import flatten
from Networks.PloteNetwork.FilteredNetworkData import FilteredNetworkData


def create_download_layout(network_plots: dict):
	with st.expander(f'downloads'):
		download_checkbox = st.checkbox("Download Data?")
		if download_checkbox:
			svg_data = flatten(create_svg_from_session(network_plots).values())
			html_data = render_jinja_template(svg_data=svg_data)
			df_dict = create_data_frame_from_session(network_plots)
			filtered_df = [val.filter(FilteredNetworkData.filtered_columns) for val in df_dict.values()]
			docx_data = render_word_template(list(df_dict.keys()), filtered_df)
			excel_data = df_to_excel_in_memory(list(df_dict.values()),
			                                   list(df_dict.keys()),
			                                   index=False,
			                                   convert_to_table=True,
			                                   )
			st.download_button(label='📥 Download Excel',
			                   data=excel_data,
			                   file_name="excel_sheets.xlsx", )
			st.download_button(label='📥 Download Docx',
			                   data=docx_data,
			                   file_name="docx_sheets.docx", )
			st.download_button(label='📥 Download SVG',
			                   data=html_data,
			                   file_name="svg_data.svg")
			download_zip_svg_figs_list(svg_data)


def download_zip_svg_figs_list(list_of_svg: list[str], file_name: str = "plot", ):
	with io.BytesIO() as buffer:
		with zipfile.ZipFile(buffer, "w") as zip:
			for en, f_ in enumerate(list_of_svg):
				if f_ is not None:
					# zip.writestr(f"{file_name}_{en + 1}.jpg", res1)
					zip.writestr(f"plot_{en + 1}.html", f_)
		buffer.seek(0)
		st.download_button(
			label="📥 Download Plots ZIP",
			data=buffer,  # StreamlitDownloadFunctions buffer
			file_name=f"{file_name}.zip"
		)
