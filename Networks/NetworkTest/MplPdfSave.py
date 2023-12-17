from matplotlib.backends.backend_pdf import PdfPages

figs_list = st.session_state[StatementConstants.network_plots][NetworkSessionConstants.temp_fig_data]
image = io.BytesIO()
pdf = PdfPages(image)
for k, figures in figs_list.items():
	for fig in figures:
		dpi = fig.get_dpi()
		figureSize = fig.get_size_inches()
		# Создаем рамку вокруг графика.
		# Это не обязательно, но так удобнее вырезать распечатанный график ножницами.
		pdf.savefig(fig)

# Сохранение файла
pdf.close()
image.seek(0)