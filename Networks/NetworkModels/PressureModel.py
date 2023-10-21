from dataclasses import dataclass, field, asdict


@dataclass
class PressureModel:
	S_Name: str
	from_branch: str
	to_branch: str
	distance: float
	flow: float= field(init=False)
	branch_type: str= field(init=False)
	diameter: int = field(init=False)
	velocity: float = field(init=False)
	Reynolds: float = field(init=False)
	lambda_pressure: float = field(init=False)
	line_pressure: float = field(init=False)
	full_line_pressure: float = field(init=False)
	dynamic_pressure: float = field(init=False)
	k_local_pressure: float = field(init=False)
	full_dynamic_pressure: float = field(init=False)
	full_pressure: float = field(init=False)
