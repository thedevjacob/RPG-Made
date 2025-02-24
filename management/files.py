import json
from pathlib import Path


SAVE_FILE_DIR = Path('management')
SAVE_FILE_NAME = Path('../info_save.json')
SAVE_PATH = SAVE_FILE_DIR / SAVE_FILE_NAME
LAW = "You are a roleplay game bot. Player's words are character's actions/thoughts. 'Quoted' text is character speech, asterisked actions. Consider past choices, environment, and available resources. Keep responses very short, ALWAYS within ONE or TWO sentences at all times. Never list off choices. Only answer questions with bare minimum. No 'What would you like to do?' prompt. Never, ever control the player's character or tell them what to do."


def organize_file(save_file: str, player_choices: str, ai_model: str) -> None:
    # create the base file format
    _base_formatting()

    # organize with the player choices
    _organize_player_data(save_file, player_choices, ai_model)


def does_save_already_exist(save_file: str):
    _ensure_file_exists()

    return save_file in get_all_save_names()

def remember_response(save_file: str, response: str, response_type: str) -> None:
    with open(SAVE_PATH, 'r+') as file:
        formatted_file = json.load(file)

        if "history" not in formatted_file['SAVES'][save_file]:
            formatted_file['SAVES'][save_file]['history'] = {"player_responses": [], "bot_responses": []}
        formatted_file['SAVES'][save_file]['history'][f'{response_type}_responses'].append(response)

        # go to the beginning of file
        file.seek(0)
        json.dump(formatted_file, file, indent=4)
        file.truncate()


def get_history(save_name: str) -> list:
    formatted_choices = _format_history(save_name, 'player')
    formatted_responses = _format_history(save_name, 'bot')

    formatted_history = [item for pair in zip(formatted_choices, formatted_responses) for item in pair]
    formatted_history.append(formatted_choices[-1])
    formatted_history = _get_constant_and_control() + formatted_history

    return formatted_history


def increment_tokens(save_name: str, num_tokens: str) -> None:
    with open(SAVE_PATH, 'r+') as file:
        formatted_file = json.load(file)
        formatted_file['SAVES'][save_name]['total_tokens_used'] += int(num_tokens)

        # go to the beginning of file
        file.seek(0)
        json.dump(formatted_file, file, indent = 4)
        file.truncate()


def select_ai_model(selected_ai_model: str) -> None:
    with open(SAVE_PATH, 'r+') as file:
        formatted_file = json.load(file)
        formatted_file['AI_MODEL'] = selected_ai_model

        # go to the beginning of file
        file.seek(0)
        json.dump(formatted_file, file, indent = 4)
        file.truncate()


def get_existing_ai_model(save_name: str) -> str:
    with open(SAVE_PATH, 'r') as file:
        formatted_file = json.load(file)
        return formatted_file['SAVES'][save_name]['ai_model']


def get_all_save_names() -> tuple:
    with open(SAVE_PATH, 'r') as file:
        formatted_file = json.load(file)
        
        all_saves = tuple(save_name for save_name in formatted_file['SAVES'].keys())
        return all_saves


def get_selected_ai_model() -> str:
    with open(SAVE_PATH, 'r') as file:
        formatted_file = json.load(file)
        return formatted_file['AI_MODEL']

def _get_constant_and_control() -> list:
    formatted_constant_and_control = []

    with open(SAVE_PATH, 'r') as file:
        formatted_file = json.load(file)
        constant = {"role": "system", "content": formatted_file['LAW']}
        control = {"role": "system", "content": formatted_file['LAW']}

        formatted_constant_and_control.append(constant)
        formatted_constant_and_control.append(control)

    return formatted_constant_and_control


def _base_formatting() -> None:
    with open(SAVE_PATH, 'r+') as file:
        if file.read() == "":
            json.dump({
                "LAW": LAW,
            }, file)

def _organize_player_data(save_name: str, player_choices: str, ai_model: str) -> None:
    with open(SAVE_PATH, 'r+') as file:
        formatted_file = json.load(file)

        formatted_file['SAVES'][save_name] = { }
        formatted_file['SAVES'][save_name]['control'] = player_choices
        formatted_file['SAVES'][save_name]['ai_model'] = ai_model
        formatted_file['SAVES'][save_name]['total_tokens_used'] = 0

        # go to the beginning of file
        file.seek(0)
        json.dump(formatted_file, file, indent=4)
        file.truncate()


def _format_history(save_name: str, response_type: str) -> list:
    role = "user"
    formatted_history = []

    if response_type == 'bot':
        role = "assistant"

    with open(SAVE_PATH, 'r') as file:
        formatted_file = json.load(file)
        responses = formatted_file['SAVES'][save_name]['history'][f'{response_type}_responses']

    for response in responses:
        formatted_history.append({"role": role, "content": response})

    return formatted_history

def _ensure_file_exists() -> None:
    try:
        file = open(SAVE_PATH, 'x', encoding='utf-8')
        formatted_law = {
            'LAW' : LAW,
            'AI_MODEL': '',
            'SAVES': {}
        }
        json.dump(formatted_law, file, ensure_ascii=False, indent=4)
        file.close()
    except FileExistsError:
        pass
