from dataclasses import dataclass


@dataclass
class CategoryDb:
	heat_loss: str = "Heat Loss"
	heat_adding: str = "Heat Adding"
	air_exhaust: str = "Air Exhaust"
	air_supply: str = "Air Supply"
	other_category:str = "Other Category"


class TableNameConstants:
	main_table = "main_table"
	joined_table = "joined_table"
	how_to_join = ["LEFT JOIN", "RIGHT JOIN", "INNER JOIN", "FULL JOIN", "CROSS JOIN"]
