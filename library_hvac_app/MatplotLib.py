import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import io


def _draw_as_table(df: pd.DataFrame, pagesize: tuple) -> plt:
	alternating_colors = [['white'] * len(df.columns), ['lightgray'] * len(df.columns)] * len(df)
	alternating_colors = alternating_colors[:len(df)]
	fig, ax = plt.subplots(figsize=pagesize)
	ax.axis('tight')
	ax.axis('off')
	the_table = ax.table(cellText=df.values,
	                     rowLabels=df.index,
	                     colLabels=df.columns,
	                     rowColours=['lightblue'] * len(df),
	                     colColours=['lightblue'] * len(df.columns),
	                     cellColours=alternating_colors,
	                     loc='center')
	return fig


def dataframe_to_pdf(df: pd.DataFrame, pdf: PdfPages, numpages=(1, 1), pagesize=(11, 8.5)):
	nh, nv = numpages
	rows_per_page = len(df) // nh
	cols_per_page = len(df.columns) // nv
	for i in range(0, nh):
		for j in range(0, nv):
			page = df.iloc[(i * rows_per_page):min((i + 1) * rows_per_page, len(df)),
			       (j * cols_per_page):min((j + 1) * cols_per_page, len(df.columns))]
			fig = _draw_as_table(page, pagesize)
			if nh > 1 or nv > 1:
				# Add a part/page number at bottom-center of page
				fig.text(0.5, 0.5 / pagesize[0],
				         "Part-{}x{}: Page-{}".format(i + 1, j + 1, i * nv + j + 1),
				         ha='center', fontsize=8)
			pdf.savefig(fig, bbox_inches='tight')
			plt.close()


mybuffer = io.BytesIO()
df = pd.DataFrame([[1, 2, 3], [7, 0, 3], [1, 2, 2]], columns=['col1', 'col2', 'col3'])
with PdfPages(mybuffer) as pdf:
	df.plot()
	pdf.savefig()
	plt.close()
	df.plot(kind='bar')
	pdf.savefig()
	plt.close()
	dataframe_to_pdf(df, pdf)
mybuffer.seek(0)
