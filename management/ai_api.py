import openai
from management.files import get_history, remember_response

MAX_TOKENS = 100


def get_bot_response(save_name: str, player_choice: str, ai_model: str) -> tuple:
    # store the player choice in history
    _store_player_choice(save_name, player_choice)

    ai_bot = openai.OpenAI()

    response = ai_bot.chat.completions.create(
        model=ai_model,
        messages=get_history(save_name),
        max_tokens=MAX_TOKENS
    )

    # store the bot response in history
    tokens_used = response.usage.completion_tokens
    bot_response = str(response.choices[0].message.content)
    _store_bot_response(save_name, bot_response)

    return bot_response, tokens_used


def get_all_ai_models() -> list:
    all_models = openai.OpenAI().models.list()
    all_models = [model.id for model in all_models.data if 'gpt' in model.id]
    return all_models


def _store_player_choice(save_name: str, player_choice: str) -> None:
    # store the player response in history
    remember_response(save_name, player_choice, 'player')


def _store_bot_response(save_name: str, bot_response: str) -> None:
    # store the bot response in history
    remember_response(save_name, bot_response, 'bot')
