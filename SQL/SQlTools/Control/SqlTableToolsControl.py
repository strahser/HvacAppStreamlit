from SQL.SQlTools.SqlOperations.SqlCRUDOperation import *
from SQL.SQlTools.View.SQLToolsView import *
from st_mui_dialog import st_mui_dialog

from SQL.SqlControl.SqlStaticTabs.SqlStaticTabDataControl import SqlStaticTabDataControl
from Session.StatementConfig import StatementConstants
from Session.UpdateDbSession import UpdateDbSession


class SqlTableToolsControl:
    """create CRUD SQL Operations """

    def __init__(self,
                 init_df: pd.DataFrame,
                 filtered_df: pd.DataFrame,
                 table_name: str,
                 ):
        """init_df for view columns,filtered_df for select id, table_name for SQL """
        self.table_name = table_name
        self._init_df = init_df
        self._filtered_df = filtered_df
        self._sql_crud_control = SqlCRUDOperation(table_name)
        self._table_add_data_view = SQLToolsView(self._init_df, self.table_name)

    def create_crud_operation(self):
        self._table_add_data_view.create_sql_tools_panel()
        self._create_column()
        self._delete_column()
        self._add_data_to_column()
        self._delete_table_or_view()

    def _create_column(self):
        if self._table_add_data_view.create_column_checkbox:
            self._table_add_data_view.create_column_view()
            self._sql_crud_control.create_column(self._table_add_data_view)

    def _delete_column(self):
        if self._table_add_data_view.delete_column_checkbox:
            self._table_add_data_view.delete_column_view()
            self._sql_crud_control.drop_column(self._table_add_data_view)

    def _add_data_to_column(self):
        if self._table_add_data_view.add_data_to_column_checkbox:
            self._table_add_data_view.add_data_to_column_view()
            _filtered_df = self._get_filtered_df_id()
            self._sql_crud_control.add_data_to_column(_filtered_df, self._table_add_data_view)

    def _get_filtered_df_id(self):
        """concat agg table checkboxes"""
        if not self._filtered_df.empty:
            _filtered_df = self._filtered_df[self._table_add_data_view.id_column].to_list()
            _filtered_df = [str(val) for val in _filtered_df if val]
            return _filtered_df
        else:
            return []

    def _delete_table_or_view(self):
        if self._table_add_data_view.delete_table_checkbox:
            self._table_add_data_view.create_delete_tables_buttons()
            if self._table_add_data_view.delete_table_db_button:
                try:
                    self._sql_crud_control.delete_exist_table(self.table_name)
                    st.success(f"Table {self.table_name} was deleted")
                except Exception as e:
                    st.warning(e)
                finally:
                    UpdateDbSession.Update_sql_sessionData()
            if self._table_add_data_view.delete_view_db_button:
                view_sql_query_model = st.session_state[StatementConstants.view_sql_query_model]
                try:
                    self._sql_crud_control.delete_exist_View(self.table_name)
                    for key, val in view_sql_query_model.items():
                        if key == self.table_name:
                            del view_sql_query_model[key]
                            break
                    st.success(f"View {self.table_name} was deleted")
                except Exception as e:
                    st.warning(e)
                finally:
                    UpdateDbSession.Update_sql_sessionData()
