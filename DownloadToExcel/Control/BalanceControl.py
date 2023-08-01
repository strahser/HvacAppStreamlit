from DownloadToExcel.View.BalanceView import *

from DownloadToExcel.Model.StatementCategoryModel import *


class BalanceControl:
	def __init__(self):
		balance_view = BalanceView()
		if balance_view.create_balance_view_button:
			StatementCategoryModel.create_balance_view()

