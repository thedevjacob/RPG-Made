import time
import input_management
import file_management

TEXT_SPEED = 0.05


def run():
    # AI Model: Either GPT 3.5 Turbo or GPT 4
    gpt_model = input_management.get_ai_model()
    print("")
    # DEV MODE: Display tokens on response from bot
    dev_mode = input_management.decide_dev_mode()
    print("")
    # PLAYER NAME: Player's username for displaying their messages
    name = input_management.get_save_name()
    print("")
    # CONTEXT: User's specifications for RPG game set-up
    context = input_management.get_game_context()
    print("")

    # Creates a file with all the user's info
    file_management.organize_file(name, context)

    print('------------------------\n')

    while True:
        try:
            bot_response = input_management.give_choice_get_response(gpt_model)
            _deliver_response(bot_response, dev_mode)
        except KeyboardInterrupt:
            print("\n-=+=-\nGame exited, save interrupted. Latest save may be minimally corrupted.\n-=+=-")
            break



def _deliver_response(response: tuple, dev_mode: bool) -> None:
    title = "RESPONSE: "
    if dev_mode:
        title += f"{{tokens used = {response[1]}}}"
    print(title, end='\n')
    for character in response[0]:
        time.sleep(TEXT_SPEED)
        print(character, end='', flush=True)
    print('\n')


if __name__ == '__main__':
    run()
