import sqlite3

from SqlDynamicCalculator.Controls.TableColumnsSelectorControl import (
	TableColumnsSelectorControl, SqlConnector, UploadLayout, st
)
from InputView.SelectedTreeInputView import SelectedTreeInputView
from SqlDynamicCalculator.View.SelectedJoinedTableView import SelectedJoinedTableView
from SqlDynamicCalculator.Models.JoinMainTableModel import JoinMainTableModel
from SqlDynamicCalculator.Models.JoinedTableListModel import JoinedTableListModel
from SqlDynamicCalculator.CategoryDb import TableNameConstants
from Session.StatementConfig import StatementConstants
from StaticData.AppConfig import MenuChapters, StaticVariable
from InputView.NodesView import ViewNodes


class JoinedTableControl:
	def __init__(self, upload_layout: UploadLayout, conn: sqlite3.Connection = SqlConnector.conn_sql, ) -> None:
		"""Populate Data with JOIN Balance View"""
		self.selected_specify_table_index_list = None
		self.selected_columns_parsing_to_string = None
		self.table_selected_dict: dict[str, str] = {}
		self.upload_layout = upload_layout
		self.number_of_table = self.__check_number_joined_table()
		self.conn = conn

	def populate_model_and_index_join_view(self) -> JoinMainTableModel:
		"""add fields from view to model JoinMainTableModel"""
		joined_table_index = JoinMainTableModel()
		tables = self.table_selected_dict.keys()
		for key in tables:
			joined_table_model = JoinedTableListModel()
			if TableNameConstants.main_table in str(key):
				_main_selected_view = SelectedJoinedTableView(key, self.table_selected_dict, self.conn,
				                                              number_of_tables=self.number_of_table)
				joined_table_index.main_table_name = _main_selected_view.joined_table_name_left
			else:
				join_table_view = SelectedJoinedTableView(key, self.table_selected_dict, self.conn)
				for attr_name in joined_table_model.__annotations__.keys():
					attr_value = getattr(join_table_view, attr_name)
					setattr(joined_table_model, attr_name, attr_value)
				joined_table_index.joined_table_list.append(joined_table_model)
		return joined_table_index

	def create_join_table_columns(self):
		self.selected_columns_parsing_to_string = ",\n".join(self._create_main_and_joined_tables())

	def _choose_main_table_for_join(self, index_: int, _table: TableColumnsSelectorControl):
		if index_ + 1 == 1:
			self.table_selected_dict[TableNameConstants.main_table] = _table.selected_sheet
		return self.table_selected_dict

	def _choose_joined_table(self, index_: int, _table: TableColumnsSelectorControl) -> dict[str, str]:
		if index_ + 1 >= 2:
			self.table_selected_dict[f"{TableNameConstants.joined_table}{index_}"] = _table.selected_sheet
		return self.table_selected_dict

	def _create_main_and_joined_tables(self) -> [str]:
		# add tables to table_selected_dict
		columns_string_list = []
		for i in range(self.number_of_table):
			_table = TableColumnsSelectorControl(self.upload_layout, conn=self.conn, key=i + 1)
			_columns_string = self.__check_selected_table(_table, i)

			self._choose_main_table_for_join(i, _table)
			self._choose_joined_table(i, _table)
			columns_string_list.append(_columns_string)
		return columns_string_list

	def __check_selected_table(self, _table, en) -> str:
		if self.selected_tables:
			return _table.get_columns_for_query(self.selected_tables[en])
		else:
			return _table.get_columns_for_query()

	def _create_select_box_view(self):
		selected_data = SelectedTreeInputView(header="Select book and sheets",
		                                      key=f"{MenuChapters.analytics} {StatementConstants.select_join_table}")
		selected = selected_data.create_select_tree()
		return selected

	def __check_number_joined_table(self):
		selected_tables = self._create_select_box_view()
		all_tables_and_views = ViewNodes(
			key=f"{MenuChapters.analytics} {StatementConstants.select_join_table} all tables")
		all_tables_and_views.create_tree_view_options("All tables")
		all_tables_and_views_tree = all_tables_and_views.table_tree
		self.selected_tables = []
		if isinstance(all_tables_and_views_tree, list):
			self.selected_tables.extend(all_tables_and_views_tree)
		if isinstance(selected_tables, list):
			self.selected_tables.extend(selected_tables)
		if self.selected_tables:
			return len(self.selected_tables)
		else:
			return 1
