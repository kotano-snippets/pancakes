import bot
import pytest

def test_start_message():
    message = message.chat.id('Что вы хотите приготовить?')
    assert 'Что вы хотите приготовить?' == bot.start_message(message)

def test_help_message():
