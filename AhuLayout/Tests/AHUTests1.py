
from AhuLayout.Layouts.AHUConstruct import *
from AhuLayout.Layouts.ExportLayouts import *
import streamlit as st
from DataForTest import *


# print(data_for_layout.get_context_dictionary()['ahu_equipment_property'])
render_data = RenderHTML(
    data_for_layout, "result.html"
)._get_equipment_data_for_render()

st.subheader("all table ")
[st.dataframe(val) for val in (concate_df.load_correct_excel_sheets_pd())]
st.subheader("all table concate")
st.write(ahu_construct.df_concat)
st.subheader("power")
st.write(ahu_construct.add_he_power())
st.subheader("temperature")
st.write(ahu_construct.add_he_temperature())
st.subheader("pumps")
st.write(ahu_construct.add_pumps())
st.subheader("fans")
st.write(ahu_construct.add_fan())
st.subheader("add spaces")
st.write(ahu_merge_blocks.system_column_name)
st.write(ahu_merge_blocks.add_spaces_names_to_system())
st.subheader("merge blocks")
st.write(ahu_merge_blocks.merge_blocks())
st.subheader("sort blocks")
st.write(ahu_merge_blocks.sort_merge_table())

# st.subhead('melt table')
# print(ahu_merge_blocks.create_melt_table())
# st.subhead('melt table add key ')
# print(ahu_merge_blocks.add_key_to_melt_table())
st.subheader("pivot table")
st.write(ahu_merge_blocks.create_pivot_table())
st.subheader("res dict")
st.write(filtred_equipment.ahu_df.columns)
st.subheader("eq names")
st.write(filtred_equipment.picture_list)

plot = CreatePlotID(filtred_equipment.ahu_df, AhuData.ahu_plot)
st.write(plot.get_plots_dictionary(), unsafe_allow_html=True)
st.write(plot.show_concat_plot(), unsafe_allow_html=True)
st.write(plot.transpose_input_df(), unsafe_allow_html=True)



            



# 111
