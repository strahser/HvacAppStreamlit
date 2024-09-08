from dataclasses import dataclass, field
from dict_to_dataclass import DataclassFromDict, field_from_dict


@dataclass()
class CardDimensions(DataclassFromDict):
	w: int = field_from_dict()
	h: int = field_from_dict()
	x: int = field_from_dict()
	y: int = field_from_dict()
	i: str = field_from_dict()
