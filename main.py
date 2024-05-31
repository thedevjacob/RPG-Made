import time
from management import files, input


TEXT_SPEED = 0.05


def run():
    # AI Model: Either GPT 3.5 Turbo or GPT 4
    gpt_model = input.get_ai_model()
    print("")
    # DEV MODE: Display tokens on response from bot
    dev_mode = input.decide_dev_mode()
    print("")
    # PLAYER NAME: Player's username for displaying their messages
    save_name = input.get_save_name()
    print("")
    # CONTEXT: User's specifications for RPG game set-up
    if not files.does_save_already_exist(save_name):
        context = input.get_game_context()
        print("")
        # Creates a file with all the user's info
        files.organize_file(save_name, context)

        print(f"------ CREATING NEW SAVE '{save_name}' ------\n")
    else: print(f"------ OPENING EXISTING SAVE '{save_name}' ------\n")

    while True:
        try:
            bot_response = input.give_choice_get_response(save_name, gpt_model)
            _deliver_response(bot_response, dev_mode)
        except KeyboardInterrupt:
            print(f"\n-=+=-\nGame exited, program interrupted. Save for '{save_name}' may be corrupted.\n-=+=-")
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
