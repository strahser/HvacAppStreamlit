import streamlit as st
import matplotlib.pyplot as plt

def _create_chart_max_mpl(self):
	titles = [["Max Bar", "Count Scatter"], ["Count Hist", "Max Pie"]]
	st.subheader("Max and Count Charts")
	fig, ax = plt.subplots(figsize=(12, 12), nrows=2, ncols=2)
	ax[0, 0].scatter(self.df_to_revit[self.select_keys_x], self.df_to_revit[self.select_keys_y])
	ax[0, 1].hist(self.df_to_revit[self.select_keys_x])
	ax[1, 0].bar(self.x_max, self.y_max)
	ax[1, 1].pie(self.y_max, labels=self.x_max, autopct='%.2f%%')
	for en_row, row in enumerate(titles):
		for en_col, col in enumerate(row):
			ax[en_row][en_col].set_title(col)
			ax[en_row][en_col].set_xlabel(f'{self.select_keys_x}')
			ax[en_row][en_col].set_ylabel(f'{self.select_keys_y}')
	return self._save_to_svg(fig)
