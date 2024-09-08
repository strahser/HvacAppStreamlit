
class NetworkPressureConstants:
	"""define names of columns, calculated functions values
    """
	branch_columns = [
		"S_ID",
		"m_idx",
		"sys_flow_column",
		"pcx",
		"pcy",
	]
	route_columns = [
		"m_idx",
		"shift_idx",
		"sum_column",
		"x_intersect",
		"y_intersect",
	]
	filtered_columns = [
		"S_Name",
		"from",
		"to",
		"distance",
		"power",
		"flow",
		"diameter",
		"velocity",
		"Renolds",
		"lambda",
		"line_pressure",
		'full_line_pressure',
		"dinamic_pressure",
		'k_local_pressure',
		'full_dinamic_pressure',
		"full_pressure",
	]
	new_columns = [
		"from",
		"to",
		"power",
		"from_x",
		"from_y",
	]

	calculation_dict: dict = {
		"flow": lambda x: x["seting_builder"].flow,
		"k_local_pressure": lambda x: x["seting_builder"].get_k_local_pressure(),
		"diameter": lambda x: x["seting_builder"].choose_standard_diameter(),
		"velocity": lambda x: x["seting_builder"].drop_pressure.get_velocity(),
		"Renolds": lambda x: x["seting_builder"].drop_pressure.get_renolds_number(),
		"lambda": lambda x: x["seting_builder"].drop_pressure.get_lamda_turbulence(),
		"line_pressure": lambda x: x["seting_builder"].drop_pressure.get_pressure_line_drop(),
		'dinamic_pressure': lambda x: x["seting_builder"].drop_pressure.get_pressure_dynamic_drop(),
		"full_dinamic_pressure": lambda x: x["seting_builder"].drop_pressure.get_full_dynamic_drop_pressure(
			x["k_local_pressure"])
	}