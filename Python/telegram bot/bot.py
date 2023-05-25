import telebot
from telebot import types
import spotify

bot_token = '6151101399:AAGSS34zCD11g3QZUaB1ZBL7K9Eob0ksEMk'
bot = telebot.TeleBot(bot_token)
my_search = spotify.SpotifyApi()

def start_message(message):
  markup = types.InlineKeyboardMarkup(row_width=1)
  botton_artist = types.InlineKeyboardButton('Найти исполнителя', callback_data='find artist')
  botton_track = types.InlineKeyboardButton('Найти песню', callback_data='find track')
  markup.add(botton_artist, botton_track)

  bot.send_animation(message.chat.id, reply_markup=markup, animation='https://media.tenor.com/CBY7kbGrdaAAAAAC/music-ally-brooke.gif')

@bot.message_handler(commands=['start'])
def start(message):
    start_message(message)

def again(message):
    return types.InlineKeyboardButton(text=f'Найти что-то другое', callback_data='again')

@bot.callback_query_handler(func=lambda call:  call.data in ['find artist', 'find track', 'again'])
def callback(call):

    if call.data == 'find artist':
        bot.send_message(call.message.chat.id, 'Введите исполнителя')
        bot.register_next_step_handler(call.message, find_artist)

    if call.data == 'find track':
        bot.send_message(call.message.chat.id, 'Введите название песни')
        bot.register_next_step_handler(call.message, find_track)

    if call.data == 'again':
        start(call.message)

@bot.callback_query_handler(func=lambda call: call.data in ['right track', 'wrong track'])
def callback(call):

    if call.data == 'right track':
        link_track(call.message)

    if call.data == 'wrong track':
        nex_track(call.message)



def find_artist(message):
    my_search.search_artist(message.text)

    markup = types.InlineKeyboardMarkup(row_width=1)
    item = types.InlineKeyboardButton(text=f'{my_search.artist_name} в Spotify', url=my_search.artist_data['link'])
    markup.add(item, again(message))

    bot.send_photo(message.chat.id, photo=my_search.artist_data['images'], reply_markup=markup)


def find_track(message):
    my_search.search_track(message.text)
    about_find_track(message)


def about_find_track(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    botton_yes = types.InlineKeyboardButton('Да', callback_data='right track')
    botton_no = types.InlineKeyboardButton('Нет', callback_data='wrong track')
    markup.add(botton_yes, botton_no)

    bot.send_audio(message.chat.id, \
                   parse_mode="html",
                   caption=f'Найдена песня <b>{my_search.track_name}</b>, исполнителя  <b>{my_search.track_data["artist"]}</b>. Вы можете послушать отрывок. Это та песня, которую вы искали?', \
                   audio=my_search.track_data['preview_url'], reply_markup=markup)


def link_track(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    botton_link = types.InlineKeyboardButton(text=f'Слушать в Spotify', url=my_search.track_data['link'])
    markup.add(botton_link, again(message))

    bot.send_message(message.chat.id, text='Отлично! Рад был помочь! Вот ссылка!')
    bot.send_photo(message.chat.id, photo=my_search.track_data['images'], reply_markup=markup)


def nex_track(message):
    if 'None' in str(my_search.url_next_track):
        bot.send_message(message.chat.id, text='Извините, я не могу найти больше песен с таким названием')
        start(message)
    else:
        my_search.next_track()
        about_find_track(message)



bot.polling()
