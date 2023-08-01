import pandas as pd


class TextWorkerForPlote:
	def __init__(self, _df: pd.DataFrame) -> None:
		"""concate prefix suffix and column value. add <br> between multivalued"""
		self._df = _df
		self._df["text"] = ""

	def concat_value_with_prefix(self, prefix: str, suffix: str,
	                             column_name: list):
		convert_prefix = self.__convert_string_to_list(prefix)
		convert_suffix = self.__convert_string_to_list(suffix)
		self.__check_prefix_suffix_len_options(convert_prefix, convert_suffix,
		                                       column_name)
		return self._df

	@staticmethod
	def _round_for_str(val):
		try:
			res = round(val)
		except:
			res = val
		return res

	def __convert_string_to_list(self, string_list: list) -> list:
		return string_list.split(",") if isinstance(string_list,
		                                            str) else string_list

	def __check_prefix_suffix_len_options(self, convert_prefix, convert_suffix,
	                                      column_name):
		if len(convert_prefix) == len(convert_suffix) and len(
				convert_prefix) == len(column_name):
			return self.__add_apply_function_eq(convert_prefix, convert_suffix,
			                                    column_name)
		elif len(convert_prefix) == len(column_name):
			return self.__add_apply_function_pref_val(convert_prefix,
			                                          convert_suffix,
			                                          column_name)
		elif len(convert_suffix) == len(column_name):
			return self.__add_apply_function_suffix_val(convert_prefix,
			                                            convert_suffix,
			                                            column_name)
		else:
			return self.__add_apply_function_val(convert_prefix, convert_suffix,
			                                     column_name)

	def __concat_strings_for_df(self,
	                            prefix: str = None,
	                            suffix: str = None,
	                            value: any = None):
		if prefix and suffix and value:
			return f"{prefix} {str(self._round_for_str(value))} {suffix}"
		elif prefix and value:
			return f"{prefix} {str(self._round_for_str(value))}"
		elif suffix and value:
			return f"{str(self._round_for_str(value))} {suffix}"
		else:
			return str(self._round_for_str(value))

	def __add_apply_function_eq(self, convert_prefix, convert_suffix,
	                            column_name):
		for prf, suf, col in zip(convert_prefix, convert_suffix, column_name):
			self._df['temp_str'] = self._df.apply(
				lambda df: self.__concat_strings_for_df(prf, suf, df[col]),
				axis=1)
			self._df["text"] = self._df["text"].astype(str).str.cat(
				self._df['temp_str'], sep="<br>")
			self._df = self._df.drop(columns=['temp_str'])
		return self._df

	def __add_apply_function_pref_val(self, convert_prefix, convert_suffix,
	                                  column_name):
		for prf, col in zip(convert_prefix, column_name):
			self._df['temp_str'] = self._df.apply(
				lambda df: self.__concat_strings_for_df(prefix=prf,
				                                        value=df[col]),
				axis=1)
			self._df["text"] = self._df["text"].astype(str).str.cat(
				self._df['temp_str'], sep="<br>")
			self._df = self._df.drop(columns=['temp_str'])
		return self._df

	def __add_apply_function_suffix_val(self, convert_prefix, convert_suffix,
	                                    column_name):
		for prf, col in zip(convert_suffix, column_name):
			self._df['temp_str'] = self._df.apply(
				lambda df: self.__concat_strings_for_df(suffix=prf,
				                                        value=df[col]),
				axis=1)
			self._df["text"] = self._df["text"].astype(str).str.cat(
				self._df['temp_str'], sep="<br>")
			self._df = self._df.drop(columns=['temp_str'])
		return self._df

	def __add_apply_function_val(self, convert_prefix, convert_suffix,
	                             column_name):
		for col in column_name:
			self._df['temp_str'] = self._df.apply(
				lambda df: self.__concat_strings_for_df(value=df[col]),
				axis=1)
			self._df["text"] = self._df["text"].astype(str).str.cat(
				self._df['temp_str'], sep="<br>")
			self._df = self._df.drop(columns=['temp_str'])
		return self._df

	@property
	def df(self):
		return self._df
