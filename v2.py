import pyowm  # package for forecast of weather
import telebot
from config import TOKEN, OWM_TOKEN
from random import randint
from telebot import types  # import buttons
import datetime
import os
import requests
from bs4 import BeautifulSoup
from random import randint

# Ubud
bot = telebot.TeleBot(TOKEN)
owm = pyowm.OWM(OWM_TOKEN, language="ru")
os.chdir('telegram')


@bot.message_handler(commands=['start'])  # it is welcome part
def welcome(message):
    sti = open('hello.jpeg', 'rb')
    bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.chat.id, "Because Dreams Come True, if You Really Want =)")

@bot.message_handler(commands=['about_love'])
def about_love(message):
    n = randint(13564,13687)
    r = requests.get(f'http://ruspoeti.ru/aut/tushnova/{n}/')
    soup = BeautifulSoup(r.text, 'lxml')
    soup = str(soup)
    start = soup.find('class="pcont"')
    finish = soup.find('class="pfoot"')
    soup = soup[start:finish]
    st = 'Тушнова</em><br/><br/>'
    start = soup.find('Тушнова</em><br/><br/>')
    finish = soup.find('</p><div') 
    soup = soup[start+len(st):finish]
    soup = soup.replace('<br/>', '')
    bot.send_message(message.chat.id, soup)

@bot.message_handler(content_types=['text'])
def send_echo(message):
    # another city
    if message.chat.type == 'private':
        user_text = message.text
        if message.text[0:5] == 'City ' or message.text[0:5] == 'city ':
            try:
                nc = user_text[5:]    # new_city
                Nc = owm.weather_at_place(nc)
                w_Nc = Nc.get_weather()
                temp_Nc = w_Nc.get_temperature('celsius')["temp"]
                answer3 = "В " + nc + ' ' + w_Nc.get_detailed_status()+'\n'
                answer3 += "Температура в среднем " + str(temp_Nc) + '\n\n'
                bot.send_message(message.chat.id, answer3)
            except:
                answer4 = 'Я не знаю такого города, наверное там хорошо :-)'
                bot.send_message(message.chat.id, answer4)
        # My first easter egg for culture people))
        elif user_text[1:5] == 'hank' or user_text[1:7] == 'пасибо':
            if 22 > datetime.datetime.now().hour > 6:
                sti4 = open('nice_day.jpg', 'rb')
                bot.send_sticker(message.chat.id, sti4)
            else:
                sti5 = open('good_night.png', 'rb')
                bot.send_sticker(message.chat.id, sti5)
        # mainpart: Forecast for Saint-Petersburg
        else:
            Ubud = owm.weather_at_place('Ubud')

            w_Ubud = Ubud.get_weather()

            temp_Ubud = w_Ubud.get_temperature('celsius')["temp"]

            answer = "В Убуде сейчас " + w_Ubud.get_detailed_status()+'\n'
            answer += "Температура в среднем " + str(temp_Ubud) + '\n'

            answer += 'В целом на Бали плюс-минус такая же херня со стандартным отклонением погоды в раю =) \n'

            # add stickers =))
            x_r = randint(1, 3)
            if 'дождь' in answer or 'ливень' in answer:
                name = f'rain{x_r}.png'
                stik = open(name, 'rb')
                bot.send_sticker(message.chat.id, stik)
            if 'солнечно' in answer or 'солнце' in answer:
                name = f'sun{x_r}.png'
                sti2 = open(name, 'rb')
                bot.send_sticker(message.chat.id, sti2)
            bot.send_message(message.chat.id, answer)

            # buttons and instructions about other cities
            markup = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton("Да!", callback_data='good')

            markup.add(item1)
            bot.send_message(message.chat.id, 'Хочешь узнать погоду в другом городе?', reply_markup=markup)


# function proccesing answer
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                help_message = ("Напиши слово 'City', пробел и затем название "
                                'по английски, убедись что оно '
                                'совпадает с названием латиницей на гугл-картах, '
                                'совсем маленькие города могут не '
                                'отображаться, я еще маленький =)')
                bot.send_message(call.message.chat.id, help_message)

    except Exception as e:
        print(repr(e))

bot.polling(none_stop=True)  # bot work non-stop

