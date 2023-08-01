from DataForTest import *

docx_file_path = 'A3_template.docx'


context_dict = data_for_layout.get_context_dictionary()
render_docx = RenderDocx(data_for_layout)
render_docx._open_docx_file(docx_file_path)
document = Document(docx_file_path)
footer =  document.sections[0].footer
footer.paragraphs[1].text = "My header text"
for paragraph in footer.paragraphs:    
    print(paragraph.text) # or whatever you have in mind
# render_docx.add_all_context_to_file(['E01'])
render_docx.add_pivot_table()
render_docx.save(docx_file_path)

