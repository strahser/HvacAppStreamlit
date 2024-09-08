from library_hvac_app.docx_custom_function import RenderDocx
from AhuLayout.Model.LabelsModel import InputTableLabels


class RenderAhuDocx(RenderDocx):
	def __init__(self, InputTableNames: InputTableLabels):
		self.InputTableNames = InputTableNames
		super().__init__()

	def __add_pictures_ahu_table(self, context_dictionary):
		self.doc_file.add_picture_table(
			context_dictionary.ahu_equip_name,
			context_dictionary.ahu_pictures,
			self.InputTableNames.filter_pivot_table,
		)

	def add_context_to_file(self, context_dictionary):
		self.doc_file.document.add_heading(
			f'{self.InputTableNames.heading} {context_dictionary.system_name}',
			level=1)
		self.__add_pictures_ahu_table(context_dictionary)

		self.doc_file.add_doctable(
			context_dictionary.ahu_property,
			self.InputTableNames.ahu_equipment_property,
		)
		self.doc_file.add_doctable(
			context_dictionary.ahu_excel_df,
			self.InputTableNames.ahu_equipment_table_name,
		)

		self.doc_file.add_page_break()
