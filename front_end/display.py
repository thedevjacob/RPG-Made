import streamlit as st
from management.files import get_all_save_names

DEFAULT_SAVE_CHOICE_TEXT = 'Select a save'

class Window:
    def __init__(self):
        st.title('RPG Chatbot')
        self.sidebar = Sidebar()

class Sidebar:
    def __init__(self):
        self.selected_save = DEFAULT_SAVE_CHOICE_TEXT
        self._all_saves = (DEFAULT_SAVE_CHOICE_TEXT,) + get_all_save_names()
    def __enter__(self):
        st.sidebar.title("Settings")
        self.selected_save = st.sidebar.selectbox("Save files", self._all_saves)
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        return self

    def get_selected_save(self) -> str:
        return self.selected_save
