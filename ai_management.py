import openai
import file_management


def get_bot_response(save_name: str, player_choice: str, ai_model: str) -> tuple:
    # store the player choice in history
    _store_player_choice(save_name, player_choice)

    ai_bot = openai.OpenAI()

    response = ai_bot.chat.completions.create(
        model=ai_model,
        messages=file_management.get_history(save_name)
    )

    # store the bot response in history
    tokens_used = response.usage.total_tokens
    bot_response = str(response.choices[0].message.content)
    _store_bot_response(save_name, bot_response)

    return bot_response, tokens_used


def _store_player_choice(save_name: str, player_choice: str) -> None:
    # store the player response in history
    file_management.remember_response(save_name, player_choice, 'player')


def _store_bot_response(save_name: str, bot_response: str) -> None:
    # store the bot response in history
    file_management.remember_response(save_name, bot_response, 'bot')
