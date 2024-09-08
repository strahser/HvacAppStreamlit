import io
import zipfile
from datetime import datetime
import plotly
import streamlit as st
from plotly import graph_objs as go


class DownloadPlotter:
    def __init__(self):
        self.fig = go.Figure()

    def download_plt_html(self):
        today = datetime.now()
        with io.BytesIO() as buffer:
            # Write the zip file to the buffer
            width = st.session_state["Scheme plot_width"]
            height = st.session_state["Scheme plot_height"]
            with zipfile.ZipFile(buffer, "w") as zip:
                res1 = plotly.io.to_image(self.fig, "pdf", width=width, height=height, scale=1.5)
                res2 = plotly.io.to_image(self.fig, "jpg", width=width, height=height, scale=1.5)
                res3 = plotly.io.to_html(self.fig, include_plotlyjs="cdn", default_width=width, default_height=height)
                zip.writestr(f"Scheme_{today}.pdf", res1)
                zip.writestr(f"Scheme_{today}.jpg", res2)
                zip.writestr(f"Scheme_{today}.html", res3)
                buffer.seek(0)
            btn = st.download_button(
                label="Download ZIP",
                data=buffer,  # StreamlitDownloadFunctions buffer
                file_name=f"Scheme_{today}.zip"
            )
