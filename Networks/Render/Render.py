import inspect
import os
import io
import pandas as pd
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(parent_dir)
from library_hvac_app.docx_custom_function import DocxConfig
from library_hvac_app.list_custom_functions import to_list
from jinja2 import Environment, FileSystemLoader


class NetworkHtmlConfig:
	path_to_template = os.path.join(parent_dir, "static", "A3_template.docx")


def render_word_template(title_list: list[str], df_list: list[pd.DataFrame])->io.BytesIO:
	title_list = to_list(title_list)
	df_list = to_list(df_list)
	doc_file = DocxConfig()
	doc_file.open_file(NetworkHtmlConfig.path_to_template)
	for df, title in zip(df_list, title_list):
		if not df.empty and title:
			t = title.replace("_", " ")
			doc_file.document.add_heading(t, 2)
			doc_file.add_doctable(df)
	file_stream = io.BytesIO()
	# Save the .docx to the buffer
	doc_file.save(file_stream)
	# Reset the buffer's file-pointer to the beginning of the file
	file_stream.seek(0)
	return file_stream


def render_jinja_template(**kwargs):
	template_dict = os.path.join(parent_dir, "Static")
	environment = Environment(loader=FileSystemLoader(template_dict))
	template = environment.get_template("PlotHtml.html")
	content = template.render(kwargs)
	return content
