import streamlit as st
import management.files as files
import management.ai_api as ai_api

DEFAULT_SAVE_CHOICE_TEXT = 'Select a save'
_ALL_AI_MODELS = ai_api.get_all_ai_models()


class Window:
    def __init__(self):
        st.title('RPG Chatbot')
        self.sidebar = Sidebar()

class Sidebar:
    def __init__(self):
        self.selected_save = DEFAULT_SAVE_CHOICE_TEXT
        self.selected_ai_model = files.get_selected_ai_model()
        self._all_ai_models = (self.selected_ai_model, ) + _ALL_AI_MODELS
        self._all_saves = (DEFAULT_SAVE_CHOICE_TEXT, ) + files.get_all_save_names()
    def __enter__(self):
        st.sidebar.title("Settings")
        self.selected_ai_model = st.sidebar.selectbox("AI models", self._all_ai_models)
        self.selected_save = st.sidebar.selectbox("Save files", self._all_saves)
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        return self

    def get_selected_save(self) -> str:
        return self.selected_save
    def set_ai_model(self, new_ai_model: str) -> None:
        self.selected_ai_model = new_ai_model
        files.select_ai_model(new_ai_model)

