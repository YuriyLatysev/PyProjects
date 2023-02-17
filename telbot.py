import csv
import random

import telebot

bot = telebot.TeleBot('5901360246:AAE34FfQ-FaM2UCVv1t4lrlEIdAHLqssea0')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'<b>Hi</b> {message.}', parse_mode='html')


@bot.message_handler(commands=['help'])
def help_bot(message):
    bot.send_message(message.chat.id, 'Help')


def check_id(user_id):
    pass


def choose_word():
    try:
        with open('words.csv', 'r', newline='', encoding='utf-8') as csv_file:
            rand_num = random.randint(1, 5000)
            reader = csv.DictReader(csv_file)
            for row in reader:
                if row['num'] == str(rand_num):
                    return row['english_word'], row['russian_word1'], row['russian_word2'], row['russian_word3']
    except FileNotFoundError as err:
        print(f'File does not exist. error - {err}')
        return None, None, None, None


if __name__ == '__main__':
    english_word, russian_word1, russian_word2, russian_word3 = choose_word()
    bot.polling(none_stop=True)
