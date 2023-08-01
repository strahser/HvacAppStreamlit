from Session.AutoloadSession import condition_session_save, _state
import json
from Session.StatementConfig import StatementConstants


class JsonSessionExportFromStatic:
	def _save_json(self):
		with open('../../data.json', 'r') as fp:
			load = json.load(fp)
		save_file = condition_session_save(load)
		with open('../../data.json', 'w') as fp:
			json.dump(save_file, fp, indent=4)

	def _load_json(self):
		with open('../../data.json', 'r') as fp:
			load = json.load(fp)
			condition_session_save(load, False)

	def create_autoload(self):
		if _state.get("selected_app") != _state.get(StatementConstants.mainHydralitMenuComplex):
			self._load_json()
		elif _state.get("selected_app") == _state.get(StatementConstants.mainHydralitMenuComplex):
			self._save_json()
