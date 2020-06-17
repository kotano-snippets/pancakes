import bot
import pytest
from unittest.mock import Mock
import json


# Вписываете сюда свой message.chat.id
# Чтобы его узнать запустите бота с коммандой /start
# и найдите chat id в консоли

test_id = 1111111

msg = Mock()
msg.chat.id = test_id
msg.text = 'test'


def test_start_message():
    answer = bot.start_message(msg)
    assert 'Что вы хотите приготовить?' == answer.text


def test_help_message():
    e = 'Для того, чтобы увидеть доступные рецепты, выберите категорию блюда'
    r = bot.help_message(msg)
    assert e == r.text


def test_keyboard_recipes():
    r = bot.keyboard_recipes(0, 5)
    exp = [
        [{'text': 'Луковый суп'}],
        [{'text': 'Сырный cyп по-французски'}],
        [{'text': 'Куриный суп с рисом'}],
        [{'text': 'Сырный суп с креветками'}],
        [{'text': 'Острый испанский суп с колбасками'}],
        [{'text': 'Вернуться к выбору категории'}]]
    assert r.keyboard == exp


def test_recipe_and_photo_response(monkeypatch):
    msg.text = 'Рандомный рецепт'

    def mockf(*arg):
        return recipes[first]

    monkeypatch.setattr(bot.random, 'choice', mockf)

    with open('recipes.json', 'r', encoding='utf-8') as recipe:
        recipes = json.load(recipe)
        tpl = sorted(recipes.keys(), key=lambda x: x[0])
        first = tpl[0]

    r = bot.recipe_and_photo_response(msg)
    assert r.text == recipes[first]
