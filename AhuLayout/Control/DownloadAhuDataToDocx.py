import io
from AhuLayout.Control.RenderAhuDocx import RenderAhuDocx
from AhuLayout.Model.ContextAhuDictionary import ContextAhuDictionary
import streamlit as st


def download_ahu_data_to_docx(ahu_list: list,
                              path_to_template: str,
                              ContextAhuDictionary: ContextAhuDictionary,
                              InputTableNames,
                              project_number="project_number"):
	render_docx = RenderAhuDocx(InputTableNames)
	render_docx.create_or_open_docx_file(path_to_template)
	render_docx.change_footer_text(new_text=project_number, footer_number=0)
	for ahu in ahu_list:
		context_dictionary = ContextAhuDictionary
		context_dictionary.system_name = ahu.system_name
		context_dictionary.ahu_equip_name = ahu.list_ahu_labels
		context_dictionary.ahu_pictures = ahu.list_ahu_pictures
		context_dictionary.ahu_property = ahu.list_ahu_property.reset_index(drop=True).reset_index().fillna("")
		context_dictionary.ahu_excel_df = ahu.excel_df.fillna("")
		render_docx.add_context_to_file(context_dictionary)
	# Create in-memory buffer
	file_stream = io.BytesIO()
	# Save the .docx to the buffer
	render_docx.save(file_stream)
	# Reset the buffer's file-pointer to the beginning of the file
	file_stream.seek(0)
	st.download_button(label='📥 Download docx files',
	                   data=file_stream,
	                   file_name="AhuData.docx")
