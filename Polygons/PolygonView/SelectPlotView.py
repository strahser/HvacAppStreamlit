import streamlit as st
from Session.StatementConfig import StatementConstants
import pandas as pd
from streamlit_tree_select import tree_select


class SelectPlotView:
    def __init__(self,key: str):
        self.key = key
        self.node_key = f"{self.key} select plot view"
        self._add_data_to_session(self.node_key)
        self.level_plots = st.session_state[StatementConstants.levels_plots]

    def create_checkboxes_plot_view(self):
        nodes = self._create_plot_nodes()
        with st.expander("Select Plot Level"):
            self.selected_levels = tree_select(nodes,
                                               check_model="leaf",
                                               key=self.node_key,
                                               checked=st.session_state[self.node_key]["checked"])["checked"]
            if self.selected_levels:
                    return True
            else:
                return False

    def _create_plot_nodes(self):
        nodes = [{"label": level, "value": level} for level in self.level_plots.keys()]
        return nodes

    @staticmethod
    def _add_data_to_session(node_key):
        if node_key not in st.session_state:
            st.session_state[node_key] = {}
            if "checked" not in st.session_state[node_key]:
                st.session_state[node_key]["checked"] = []