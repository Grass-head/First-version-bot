import datetime
import ephem 
from glob import glob
import logging
from random import choice

from utils import get_keyboard, get_user_emo

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

def get_contact(bot, update, user_data):
    print(update.message.contact)
    update.message.reply_text('Готово: {}'.format(get_user_emo(user_data)), reply_markup=get_keyboard())

def get_location(bot, update, user_data):
    print(update.message.location)
    update.message.reply_text('Готово: {}'.format(get_user_emo(user_data)), reply_markup=get_keyboard())
