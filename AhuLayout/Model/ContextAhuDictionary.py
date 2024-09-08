import pandas as pd
from dataclasses import dataclass, field


@dataclass
class ContextAhuDictionary:
	system_name: str = None
	ahu_equip_name: list = None
	ahu_pictures: list = None
	ahu_property: str = None
	ahu_excel_df: pd.DataFrame = None
