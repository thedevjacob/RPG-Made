import file_management
import ai_management

CONTEXT_STOP_WORD = 'DONE'
AI_MODEL_GPT_3 = 'gpt-3.5-turbo'
AI_MODEL_GPT_4 = 'gpt-4'


def get_ai_model() -> str:
    model_choice = None

    while True:
        ai_gpt_3_keywords = ["3", "gpt3", "1", "gpt3.5", "3.5turbo", "gpt3.5turbo"]
        ai_gpt_4_keywords = ["4", "gpt4", "2"]

        print("Enter AI model.")
        print("  1) GPT 3.5 Turbo\n  2) GPT 4\n")

        ai_choice = input(" >>> ").lower()
        ai_choice = ai_choice.replace(" ", "").replace("-", "").replace(")", "").replace(".5", "").lower()

        if ai_choice in ai_gpt_3_keywords:
            model_choice = AI_MODEL_GPT_3
        elif ai_choice in ai_gpt_4_keywords:
            model_choice = AI_MODEL_GPT_4
        else:
            print("INVALID MODEL.")
            continue
        break
    print("Selected", model_choice, "\b.")
    return model_choice


def get_save_name() -> str:
    print("Enter save name.")
    return input(" >>> ")


def get_game_context() -> str:
    print(f"Please type your game context and type {CONTEXT_STOP_WORD} when you're finished. Example:")
    print(f""" example: 'My character is trying to survive an alien invasion! 
           My goal is to survive the invasion and get to safety.
           I am currently on a spaceship trying to escape. 
           There are many aliens around me.
           {CONTEXT_STOP_WORD}'""")

    context = ''

    line = 0
    while line != -1:
        line += 1
        context_line = input(f"CONTEXT LINE {line} >>> ")

        if context_line.strip().upper() != CONTEXT_STOP_WORD:
            context += context_line.strip() + ' '
        else:
            line = -1

    return context


def give_choice_get_response(save_name: str, ai_model: str) -> tuple:
    # get player choice
    player_choice = _get_choice()
    # get bot response
    bot_response = ai_management.get_bot_response(save_name, player_choice, ai_model)

    return bot_response


def decide_dev_mode() -> bool:
    dev_mode_on_choices = ["y", "yes", "on", "okay", "alright", "please", "ok"]

    print("DEV MODE ON?")
    dev_mode_input = input(" >>> ").lower()

    return dev_mode_input in dev_mode_on_choices


def _get_choice() -> str:
    return input(f"You: ")
