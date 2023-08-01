from dataclasses import dataclass
from StaticData.AppConfig import MenuChapters
import enum


class TreeKeysModel(enum.Enum):
	table_choosing: str = f"{MenuChapters.dash_board} table_choosing"
	chart_choosing: str = f"{MenuChapters.dash_board} chart_choosing"
