import display
import chat_input

def start():
    window = display.Window()

    with window.sidebar as sb:
        sb.set_ai_model(sb.selected_ai_model)
        selected_save = sb.get_selected_save()

        if selected_save != display.DEFAULT_SAVE_CHOICE_TEXT:
            chat = chat_input.Chat()
            print(chat)

if __name__ == '__main__':
    start()
