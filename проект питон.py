import requests
import random
import telebot
from bs4 import BeautifulSoup as b
import lxml.html
import re
from telebot import types

URL = "https://www.anekdot.ru/last/good/"
API_KEY='5228876217:AAGIFmwsiS0Qgq5CtA9bt21MFeKdNK1hZiA'
def parser(url):
    r = requests.get(url)
    soup = b(r.text, 'html.parser')
    anekdots = soup.find_all('div', class_='text')
    return [c.text for c in anekdots]

list_of_jokes = parser(URL)
random.shuffle(list_of_jokes)

bot = telebot.TeleBot(API_KEY)

URL1 = "https://my-calend.ru/holidays"
def parser(url1):
    r = requests.get(url1)
    # print(r.text)
    soup = b(r.text, 'html.parser')
    soup = soup.select_one(".holidays-items")
    congratulations = soup.find_all('li')
    congratulations = [c.text for c in congratulations if len(c.text) > 4]
    reg = re.compile('[^а-яА-Я ]')
    for i in range(len(congratulations)):
        congratulations[i] = reg.sub('', congratulations[i]).strip()
    return congratulations

list_of_holiday = parser(URL1)
random.shuffle(list_of_holiday)


@bot.message_handler(commands=['start'])
def anek(message):
    keyboard = types.InlineKeyboardMarkup()
    key_jokes = types.InlineKeyboardButton(text='Анекдот', callback_data='joke')
    keyboard.add(key_jokes)

    key_holiday = types.InlineKeyboardButton(text='Праздник', callback_data='holiday')
    keyboard.add(key_holiday)

    key_zodiac = types.InlineKeyboardButton(text='Знак зодиака', callback_data='zodiac')
    keyboard.add(key_zodiac)


    msg = bot.send_message(message.chat.id, "Привет! Выбери из списка", reply_markup=keyboard)


def send_hello_or_holiday(message):
    if message.text == "Анекдот":
        msg = bot.send_message(message.chat.id, 'Тогда введи любую цифру:')
        bot.register_next_step_handler(msg, jokes)
    else:
        msg = bot.send_message(message.chat.id, 'Тогда вевди любую цифру:')
        bot.register_next_step_handler(msg, holiday)


def jokes(message):
    if message.text.lower() in '123456789':
        bot.send_message(message.chat.id, list_of_jokes[0])
        del list_of_jokes[0]


def holiday(message):
    if message.text.lower() in '123456789':
        photos = 4
        bot.send_message(message.chat.id, list_of_holiday[0])
        photo = open(f'img/image{random.randint(0,photos-1)}.jpg','rb')
        bot.send_photo(message.chat.id, photo)
        del list_of_holiday[0]

def zodiak(message):
    # Готовим кнопки

    keyboard = types.InlineKeyboardMarkup()
    msg = bot.send_message(message.chat.id, text='Выбери свой знак зодиака', reply_markup=keyboard)

first = ["Сегодня — идеальный день для новых начинаний.",
         "Оптимальный день для того, чтобы решиться на смелый поступок!",
         "Будьте осторожны, сегодня звёзды могут повлиять на ваше финансовое состояние.",
         "Лучшее время для того, чтобы начать новые отношения или разобраться со старыми.",
         "Плодотворный день для того, чтобы разобраться с накопившимися делами."]

second = ["Но помните, что даже в этом случае нужно не забывать про", "Если поедете за город, заранее подумайте про",
          "Те, кто сегодня нацелен выполнить множество дел, должны помнить про",
          "Если у вас упадок сил, обратите внимание на",
          "Помните, что мысли материальны, а значит вам в течение дня нужно постоянно думать про"]

second_add = ["отношения с друзьями и близкими.",
              "работу и деловые вопросы, которые могут так некстати помешать планам.",
              "себя и своё здоровье, иначе к вечеру возможен полный раздрай.",
              "бытовые вопросы — особенно те, которые вы не доделали вчера.",
              "отдых, чтобы не превратить себя в загнанную лошадь в конце месяца."]

third = ["Злые языки могут говорить вам обратное, но сегодня их слушать не нужно.",
         "Знайте, что успех благоволит только настойчивым, поэтому посвятите этот день воспитанию духа.",
         "Даже если вы не сможете уменьшить влияние ретроградного Меркурия, то хотя бы доведите дела до конца.",
         "Не нужно бояться одиноких встреч — сегодня то самое время, когда они значат многое.",
         "Если встретите незнакомца на пути — проявите участие, и тогда эта встреча посулит вам приятные хлопоты."]


# Метод, который получает сообщения и обрабатывает их

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    # Если написали «Привет»

    if message.text == "Привет":
        bot.send_message(message.from_user.id, "\nПиши /start и поехали")


    elif message.text == "/help":

        bot.send_message(message.from_user.id, "Напиши Привет")

    else:

        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


# Обработчик нажатий на кнопки

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):


    # Если нажали на одну из 12 кнопок — выводим гороскоп

    if call.data == "zodiac":
        # Пишем приветствие

        keyboard = types.InlineKeyboardMarkup()

        key_oven = types.InlineKeyboardButton(text='Овен', callback_data='1')
        keyboard.add(key_oven)

        key_telec = types.InlineKeyboardButton(text='Телец', callback_data='1')

        keyboard.add(key_telec)

        key_bliznecy = types.InlineKeyboardButton(text='Близнецы', callback_data='1')

        keyboard.add(key_bliznecy)

        key_rak = types.InlineKeyboardButton(text='Рак', callback_data='1')

        keyboard.add(key_rak)

        key_lev = types.InlineKeyboardButton(text='Лев', callback_data='1')

        keyboard.add(key_lev)

        key_deva = types.InlineKeyboardButton(text='Дева', callback_data='1')

        keyboard.add(key_deva)

        key_vesy = types.InlineKeyboardButton(text='Весы', callback_data='1')

        keyboard.add(key_vesy)

        key_scorpion = types.InlineKeyboardButton(text='Скорпион', callback_data='1')

        keyboard.add(key_scorpion)

        key_strelec = types.InlineKeyboardButton(text='Стрелец', callback_data='1')

        keyboard.add(key_strelec)

        key_kozerog = types.InlineKeyboardButton(text='Козерог', callback_data='1')

        keyboard.add(key_kozerog)

        key_vodoley = types.InlineKeyboardButton(text='Водолей', callback_data='1')

        keyboard.add(key_vodoley)

        key_ryby = types.InlineKeyboardButton(text='Рыбы', callback_data='1')

        keyboard.add(key_ryby)
        msg = bot.send_message(call.message.chat.id, 'Привет, сейчас я расскажу тебе гороскоп на сегодня', reply_markup=keyboard)

    elif call.data == "holiday":
        msg = bot.send_message(call.message.chat.id, 'Тогда введи любую цифру:')
        bot.register_next_step_handler(msg, holiday)

    elif call.data == "joke":
        msg = bot.send_message(call.message.chat.id, 'Тогда введи любую цифру:')
        bot.register_next_step_handler(msg, jokes)

    else:
        # Формируем гороскоп
        msg = random.choice(first) + ' ' + random.choice(second) + ' ' + random.choice(
            second_add) + ' ' + random.choice(third)

        # Отправляем текст в Телеграм

        bot.send_message(call.message.chat.id, msg)

# Запускаем постоянный опрос бота в Телеграме

bot.polling(none_stop=True, interval=0)
bot.polling()


