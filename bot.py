import telebot
from telebot import types
from telebot import apihelper
import json
import random

TOKEN = '962602884:AAEcPP9rnK9licJSo_g_4OkksXkSfmXAgbk'

# apihelper.proxy = {'https': 'socks5://94.103.81.38:1088'}
apihelper.proxy = {'https': 'socks5://107.170.42.147:11978'}  # USA

bot = telebot.TeleBot(TOKEN, apihelper.proxy)

keyboard_category = telebot.types.ReplyKeyboardMarkup(
    True)  # Создание клавиатуры с категориями блюд
keyboard_category.add('Первое блюдо', 'Второе блюдо',
                      'Салат', 'Десерт', 'Рандомный рецепт')


@bot.message_handler(commands=['start'])
# Выдача пользователю ответа на нажатие команды start и клавиатуры с категориями блюд
def start_message(message):
    print('\nchat id:', message.chat.id)
    return bot.send_message(message.chat.id, 'Что вы хотите приготовить?',
                            reply_markup=keyboard_category)


@bot.message_handler(commands=['help'])
# Выдача пользователю ответа на нажатие команды help и клавиатуры с категориями блюд
def help_message(message):
    return bot.send_message(message.chat.id,
                            'Для того, чтобы увидеть доступные рецепты, выберите категорию блюда',
                            reply_markup=keyboard_category)


def keyboard_recipes(start, end):  # Создание клавиатур с названиями блюд
    """create keyboards with recipes of dishes"""

    # Создание основы для клавиатур с названиями блюд
    keyboard_base = types.ReplyKeyboardMarkup(True)

    # Открытие файла recipes.json для чтения
    with open('recipes.json', 'r', encoding='utf-8') as keyboard:
        # Загрузка данных из файла в словарь keyboards
        keyboards = json.load(keyboard)

    for key in list(keyboards)[start:end]:
        # Преобразование словаря keyboards в список, создание среза из значений списка и итерация по нему
        # Создание клавиатуры из значений среза: start - начало среза, end - конец среза
        keyboard_base.add(key)

    # Добавление кнопки 'Вернуться к выбору категории'
    keyboard_base.row('Вернуться к выбору категории')

    return keyboard_base


@bot.message_handler(content_types=['text'])
# Выдача рецептов блюд различных категорий с фотографиями
def recipe_and_photo_response(message):
    """return recipes of dishes with photos"""

    # Открытие файла recipes.json для чтения
    with open('recipes.json', 'r', encoding='utf-8') as recipe:
        # Загрузка данных из файла в словарь recipes
        recipes = json.load(recipe)

    # Открытие файла photos.json для чтения
    with open('photos.json', 'r', encoding='utf-8') as photo:
        photos = json.load(photo)  # Загрузка данных из файла в словарь photos
    
    if message.text == 'Вернуться к выбору категории':
        # Выдача пользователю клавиатуры с категориями блюд при нажатии на кнопку 'Вернуться к выбору категории'
        bot.send_message(message.chat.id, 'Выберите категорию',
                            reply_markup=keyboard_category)

    elif message.text == 'Первое блюдо':
        # Выдача пользователю вопроса и клавиатуры с вариантами рецептов при нажатии кнопки "Первое блюдо"
        bot.send_message(message.chat.id, 'Какой супчик вы хотите сварить?',
                         reply_markup=keyboard_recipes(0, 10))

    elif message.text == 'Второе блюдо':
        # Выдача пользователю вопроса и клавиатуры с вариантами рецептов при нажатии кнопки "Второе блюдо"
        bot.send_message(message.chat.id, 'Что из второго желаете попробовать?',
                         reply_markup=keyboard_recipes(11, 20))

    elif message.text == 'Салат':
        # Выдача пользователю вопроса и клавиатуры с вариантами рецептов при нажатии кнопки "Салат"
        bot.send_message(message.chat.id, 'Какой салатик вы решили отведать?',
                         reply_markup=keyboard_recipes(21, 30))

    elif message.text == 'Десерт':
        # Выдача пользователю вопроса и клавиатуры с вариантами рецептов при нажатии кнопки "Десерт"
        bot.send_message(message.chat.id, 'Каким десертом полакомитесь?',
                         reply_markup=keyboard_recipes(31, 40))

    # Выдача случайного рецепта с фото при нажатии кнопки "Рандомный рецепт"
    elif message.text == 'Рандомный рецепт':
        random_recipe = random.choice(list(recipes.values()))
        # Генерация рандомного рецепта из значений словаря recipes
        r = bot.send_message(message.chat.id, random_recipe)
        
        # XXX: Нахождение файла по ID невозможно для новых пользователей.
        # используйте bot.send_photo(message.chat.id, open('image.png'))

        # bot.send_photo(message.chat.id, photos['{}'.format(
        #     random_recipe[:random_recipe.find('`')])])
        return r
        # В сгенирированном рандомном рецепте находит все симфолы до знака '`' и отделяет их от остального текста,
        # затем по полученному значению как по ключу находит фото рецепта в словаре photos

    try:
        bot.send_message(message.chat.id, recipes['{}'.format(message.text)])
        # В словаре recipes по ключу (кнопки клавиатуры) находит выбранный пользователем рецепт
        bot.send_photo(message.chat.id, photos['{}'.format(message.text)])
        # В словаре photos по ключу (кнопки клавиатуры) находит фото выбранного пользователем рецепта
    except KeyError:  # В случае не нахождения ключа в словарях recipes и photos
        # return recipe_and_photo_response
        pass


if __name__ == '__main__':
    bot.polling(none_stop=True, timeout=60)
