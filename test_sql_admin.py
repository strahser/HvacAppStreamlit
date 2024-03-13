import streamlit as st
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

from streamlit_sqlalchemy import StreamlitAlchemyMixin

Base = declarative_base()


class ExampleModel(Base, StreamlitAlchemyMixin):
	__tablename__ = "example"

	id = Column(Integer, primary_key=True)
	name = Column(String)


# Initialize the connection
CONNECTION = st.connection("example_db", type="sql")
Base.metadata.create_all(CONNECTION.engine)
StreamlitAlchemyMixin.st_initialize(CONNECTION)

# Create CRUD tabs
ExampleModel.st_crud_tabs()
