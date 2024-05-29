import json


def organize_file(save_file: str, player_choices: str) -> None:
    # create the base file format
    _base_formatting()

    # organize with the player choices
    _organize_player_data(save_file, player_choices)


def remember_response(response: str, response_type: str) -> None:
    with open('info_file.json', 'r+') as file:
        formatted_file = json.load(file)

        formatted_file['history'][f'{response_type}_responses'].append(response)

        # go to the beginning of file
        file.seek(0)
        json.dump(formatted_file, file, indent=4)
        file.truncate()


def get_history() -> list:
    formatted_choices = _format_history('player')
    formatted_responses = _format_history('bot')

    formatted_history = [item for pair in zip(formatted_choices, formatted_responses) for item in pair]
    formatted_history.append(formatted_choices[-1])
    formatted_history = _get_constant_and_control() + formatted_history

    return formatted_history


def _get_constant_and_control() -> list:
    formatted_constant_and_control = []

    with open('info_file.json', 'r') as file:
        formatted_file = json.load(file)
        constant = {"role": "system", "content": formatted_file['constant']}
        control = {"role": "system", "content": formatted_file['control']}

        formatted_constant_and_control.append(constant)
        formatted_constant_and_control.append(control)

    return formatted_constant_and_control


def _base_formatting() -> None:
    with open('info_file.json', 'w') as file:
        file.write(open('info_save.json', 'r').read())


def _organize_player_data(save_file: str, player_choices: str) -> None:
    with open('info_file.json', 'r+') as file:
        formatted_file = json.load(file)

        formatted_file['save_file'] = save_file
        formatted_file['control'] = player_choices

        # go to the beginning of file
        file.seek(0)
        json.dump(formatted_file, file, indent=4)
        file.truncate()


def _format_history(response_type: str) -> list:
    role = "user"
    formatted_history = []

    if response_type == 'bot':
        role = "assistant"

    with open('info_file.json', 'r') as file:
        formatted_file = json.load(file)
        responses = formatted_file['history'][f'{response_type}_responses']

    for response in responses:
        formatted_history.append({"role": role, "content": response})

    return formatted_history
