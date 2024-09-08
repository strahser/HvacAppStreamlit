import streamlit as st
from streamlit_ace import st_ace, KEYBINDINGS, LANGUAGES, THEMES


def _get_config():
	config = dict(
		placeholder=st.text_input("Editor placeholder", value="SELECT name FROM sqlite_master WHERE type='table' "),
		value="SELECT name FROM sqlite_master WHERE type='table' ",
		language=st.selectbox("Language mode", options=LANGUAGES, index=LANGUAGES.index("sql")),
		theme=st.selectbox("Theme", options=THEMES, index=THEMES.index("xcode")),
		keybinding=st.selectbox("Keybinding mode", options=KEYBINDINGS, index=3),
		font_size=st.slider("Font size", 5, 24, 14),
		tab_size=st.slider("Tab size", 1, 8, 4),
		show_gutter=st.checkbox("Show gutter", value=True),
		show_print_margin=st.checkbox("Show print margin", value=False),
		wrap=st.checkbox("Wrap enabled", value=False),
		auto_update=st.checkbox("Auto update", value=False),
		readonly=st.checkbox("Read-only", value=False),
		min_lines=20,
		key="ace",
	)
	return config


def AceEditorView(value_: str = "SELECT name FROM sqlite_master WHERE type='table' "):
	st.subheader("Editor Window")
	return st_ace(
		value=value_,
		placeholder="Type Query ",
		language="sql",
		key="ace")
