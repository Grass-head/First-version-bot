import datetime
import ephem 
from glob import glob
import logging
from random import choice

from emoji import emojize
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, RegexHandler, Filters

import settings


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

def greet_user(bot, update, user_data):
    emo = get_user_emo(user_data)
    user_data['emo'] = emo
    text = 'Привет {}'.format(emo)
    update.message.reply_text(text, reply_markup=get_keyboard())

def talk_to_me(bot, update, user_data):
    emo = get_user_emo(user_data)
    user_text = "Привет, {} {}! Ты написал: {}".format(update.message.chat.first_name, emo, 
                update.message.text) 
    logging.info('User: %s, Chat id: %s, Message: %s', update.message.chat.username,
                update.message.chat.id, update.message.text)
    update.message.reply_text(user_text, reply_markup=get_keyboard())

def send_cat_picture(bot, update, user_data):
    cat_list = glob('images/cat*.jp*g')
    cat_pic = choice(cat_list)
    bot.send_photo(chat_id=update.message.chat.id, photo=open(cat_pic, 'rb'), reply_markup=get_keyboard())

def reply_planet(bot, update):
    s_planet = update.message.text.split()
    planet = s_planet[1]
    now = update.message.date.strftime("%Y/%m/%d")
    update.message.reply_text('Ты написал(а) планету {}, эта планета сегодня находится в созвездии {}'.format(planet, check_planet(planet, now)))

def check_planet(planet, date):
    planets = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupyter', 
    'Saturn', 'Uranus', 'Neptune', 'Pluto']        
    if planet in planets:
        if planet == 'Sun':
            p = ephem.Sun(date)
            return ephem.constellation(p)[1] 
        elif planet == 'Moon':
            p = ephem.Moon(date)
            return ephem.constellation(p)[1]
        elif planet == 'Mercury':
            p = ephem.Mercury(date)
            return ephem.constellation(p)[1]
        elif planet == 'Venus':
            p = ephem.Venus(date)
            return ephem.constellation(p)[1]
        elif  planet == 'Mars':
            p = ephem.Mars(date)
            return ephem.constellation(p)[1]
        elif planet == 'Jupyter':
            p = ephem.Jupiter(date)
            return ephem.constellation(p)[1]
        elif planet == 'Saturn':
            p = ephem.Saturn(date)
            return ephem.constellation(p)[1]
        elif planet == 'Uranus':
            p = ephem.Uranus(date)
            return ephem.constellation(p)[1]
        elif planet == 'Neptune':
            p = ephem.Neptune(date)
            return ephem.constellation(p)[1]
        else:
            p = ephem.Pluto(date)
            return ephem.constellation(p)[1]
    else: 
        raise ValueError("Вы ввели название планеты Earth или иного тела солнечной системы. Для данных позиций произвести расчеты нельзя")

def change_avatar(bot, update, user_data):
    if 'emo' in user_data:
        del user_data['emo']
    emo = get_user_emo(user_data)
    update.message.reply_text('Готово: {}'.format(emo), reply_markup=get_keyboard())

def get_user_emo(user_data):
    if 'emo' in user_data:
        return user_data['emo']
    else: 
        user_data['emo'] = emojize(choice(settings.USER_EMOJI), use_aliases=True)
        return user_data['emo']

def get_keyboard():
    contact_button = KeyboardButton('Прислать контакты', request_contact=True)
    location_button = KeyboardButton('Геолокация', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([
                                        ['Прислать котика', 'Поменять аватар'],
                                        [contact_button, location_button]
                                      ], resize_keyboard=True)
    return my_keyboard

def get_contact(bot, update, user_data):
    print(update.message.contact)
    update.message.reply_text('Готово: {}'.format(get_user_emo(user_data)), reply_markup=get_keyboard())

def get_location(bot, update, user_data):
    print(update.message.location)
    update.message.reply_text('Готово: {}'.format(get_user_emo(user_data)), reply_markup=get_keyboard())

def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)

    logging.info('Бот запускается')

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", reply_planet,))
    dp.add_handler(CommandHandler('cat', send_cat_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Прислать котика)$', send_cat_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Поменять аватар)$', change_avatar, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))

    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))
    

    mybot.start_polling()
    mybot.idle()

main()