import csv
import random

import telebot
from telebot import types

bot = telebot.TeleBot('5901360246:AAE34FfQ-FaM2UCVv1t4lrlEIdAHLqssea0')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'<b>Привет, {message.from_user.first_name}</b>', parse_mode='html')
    bot.send_message(message.chat.id, f'<b>Бот будет присылать вам слова, вы должны написать перевод</b>', parse_mode='html')
    check_id(message.from_user.id, message.chat.id)


@bot.message_handler(commands=['help'])
def help_bot(message):
    bot.send_message(message.chat.id, 'Бот предназначен для изучения английских слов.')


def check_id(user_id, message_id):
    try:
        with open('id.csv', 'r', newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if row['user_id'] == str(user_id):
                    bot.send_message(message_id, f'Вы выбрали изучать {row["num_words"]} в день')
                    break
            else:
                choose_num_words(message_id, 'Сколько слов в день вы хотите изучать?', user_id)
    except FileNotFoundError as err:
        print(f'File does not exist. error - {err}')


def choose_num_words(message_id, mes, user_id):
    markup = types.InlineKeyboardMarkup(row_width=5)
    but1 = types.InlineKeyboardButton('1', callback_data=str(user_id) + ':1')
    but2 = types.InlineKeyboardButton('2', callback_data=str(user_id) + ':2')
    but3 = types.InlineKeyboardButton('3', callback_data=str(user_id) + ':3')
    but4 = types.InlineKeyboardButton('4', callback_data=str(user_id) + ':4')
    but5 = types.InlineKeyboardButton('5', callback_data=str(user_id) + ':5')
    but6 = types.InlineKeyboardButton('6', callback_data=str(user_id) + ':6')
    but7 = types.InlineKeyboardButton('7', callback_data=str(user_id) + ':7')
    but8 = types.InlineKeyboardButton('8', callback_data=str(user_id) + ':8')
    but9 = types.InlineKeyboardButton('9', callback_data=str(user_id) + ':9')
    but10 = types.InlineKeyboardButton('10', callback_data=str(user_id) + ':10')
    markup.add(but1, but2, but3, but4, but5, but6, but7, but8, but9, but10)
    bot.send_message(message_id, mes, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def querry_handler(call):
    temp = list()
    num_words_new = call.data.split(":")[1]
    user_id_new = call.data.split(":")[0]
    with open('id.csv', 'r', newline='', encoding='utf-8') as csv_file_r:
        reader = csv.DictReader(csv_file_r)
        for row in reader:
            temp.append(row)
    with open('id.csv', 'w', newline='', encoding='utf-8') as csv_file_wr:
        fieldnames = ['user_id', 'num_words']
        writer = csv.DictWriter(csv_file_wr, fieldnames=fieldnames)
        writer.writerow({'user_id': 'user_id', 'num_words': 'num_words'})
        new = True
        for row in temp:
            if row['user_id'] == str(user_id_new):
                writer.writerow({'user_id': row['user_id'], 'num_words': num_words_new})
                new = False
            else:
                writer.writerow({'user_id': row['user_id'], 'num_words': row['num_words']})
        if new:
            writer.writerow({'user_id': user_id_new, 'num_words': num_words_new})


def choose_word():
    try:
        with open('words.csv', 'r', newline='', encoding='utf-8') as csv_file:
            rand_num = random.randint(1, 4654)
            reader = csv.DictReader(csv_file)
            for row in reader:
                if row['num'] == str(rand_num):
                    return row['english_word'], row['russian_word1'], row['russian_word2'], row['russian_word3']
    except FileNotFoundError as err:
        print(f'File does not exist. error - {err}')
        return None, None, None, None

def main():
    english_word, russian_word1, russian_word2, russian_word3 = choose_word()
    with open()


if __name__ == '__main__':
    # english_word, russian_word1, russian_word2, russian_word3 = choose_word()
    bot.polling(none_stop=True)
