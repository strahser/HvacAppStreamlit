from dataclasses import dataclass
import pandas as pd
import streamlit as st


@dataclass()
class SystemPropertyModel:
	system_flow: float = None
	system_name: str = None


class LayoutOptions:
	one_level = 'one level'
	all_levels = 'all levels'
	detail_view = 'detail view'
	table_query = 'Table Query'

class LabelListStatic:
	label_list = ["space id column", "space name column", "space area column", "space level column"]
	attr_list = ["S_ID", "S_Name", "S_area", "S_level"]
