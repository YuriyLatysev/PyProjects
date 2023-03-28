import csv
import random
import telebot
import threading
import schedule
import time
from telebot import types

bot = telebot.TeleBot('')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'<b>Привет, {message.from_user.first_name}</b>', parse_mode='html')
    bot.send_message(message.chat.id, f'<b>Бот будет присылать вам слова, вы должны написать перевод</b>',
                     parse_mode='html')
    check_id(message.from_user.id, message.chat.id)


@bot.message_handler(commands=['help'])
def help_bot(message):
    bot.send_message(message.chat.id, 'Бот предназначен для изучения английских слов.')


def check_id(user_id, message_id):
    new = True
    try:
        with open('id.csv', 'r', newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if row['user_id'] == str(user_id):
                    bot.send_message(message_id, f'Вы выбрали изучать {row["num_words"]} в день')
                    markup = types.InlineKeyboardMarkup(row_width=2)
                    but1 = types.InlineKeyboardButton('Да', callback_data='ans_1:' + str(user_id) + ':Yes')
                    but2 = types.InlineKeyboardButton('Нет', callback_data='ans_1:' + str(user_id) + ':No')
                    markup.add(but1, but2)
                    bot.send_message(message_id, 'Хотите изменить количество слов?', reply_markup=markup)
                    new = False
            else:
                if new:
                    choose_num_words(message_id, 'Сколько слов в день вы хотите изучать?', user_id)
    except FileNotFoundError as err:
        print(f'File does not exist. error - {err}')


@bot.callback_query_handler(func=lambda call: call.data.split(":")[0] == "ans_1")
def querry_handler_1(call):
    answer = call.data.split(':')[2]
    user_id_new = call.data.split(":")[1]
    bot.edit_message_reply_markup(user_id_new, call.message.message_id, reply_markup=None)
    if answer == 'Yes':
        choose_num_words(user_id_new, 'Сколько слов в день вы хотите изучать?', user_id_new)


def choose_num_words(message_id, mes, user_id):
    markup = types.InlineKeyboardMarkup(row_width=5)
    but1 = types.InlineKeyboardButton('1', callback_data='ans:' + str(user_id) + ':1')
    but2 = types.InlineKeyboardButton('2', callback_data='ans:' + str(user_id) + ':2')
    but3 = types.InlineKeyboardButton('3', callback_data='ans:' + str(user_id) + ':3')
    but4 = types.InlineKeyboardButton('4', callback_data='ans:' + str(user_id) + ':4')
    but5 = types.InlineKeyboardButton('5', callback_data='ans:' + str(user_id) + ':5')
    but6 = types.InlineKeyboardButton('6', callback_data='ans:' + str(user_id) + ':6')
    but7 = types.InlineKeyboardButton('7', callback_data='ans:' + str(user_id) + ':7')
    but8 = types.InlineKeyboardButton('8', callback_data='ans:' + str(user_id) + ':8')
    but9 = types.InlineKeyboardButton('9', callback_data='ans:' + str(user_id) + ':9')
    but10 = types.InlineKeyboardButton('10', callback_data='ans:' + str(user_id) + ':10')
    markup.add(but1, but2, but3, but4, but5, but6, but7, but8, but9, but10)
    bot.send_message(message_id, mes, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.split(":")[0] == "ans")
def querry_handler(call):
    num_words_new = call.data.split(":")[2]
    user_id_new = call.data.split(":")[1]
    change_id_csv(num_words_new=num_words_new, user_id_new=user_id_new)
    bot.edit_message_reply_markup(user_id_new, call.message.message_id, reply_markup=None)
    bot.send_message(user_id_new, f'Вы выбрали {num_words_new} слов')


def change_id_csv(num_words_new, user_id_new):
    temp = list()
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


def send_words(num_words_now):
    english_word, russian_word1, russian_word2, russian_word3 = choose_word()
    with open('id.csv', 'r', newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if int(row['num_words']) in num_words_now:
                mess = bot.send_message(row['user_id'], f'Напишите перевод слова <b>{english_word}</b>',
                                        parse_mode='html')
                bot.register_next_step_handler(mess, check_translation, russian_word1=russian_word1,
                                               russian_word2=russian_word2, russian_word3=russian_word3)


def main():
    schedule.every().day.at("09:00").do(send_words, num_words_now=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    schedule.every().day.at("10:00").do(send_words, num_words_now=[6, 7, 8, 9, 10])
    schedule.every().day.at("11:00").do(send_words, num_words_now=[4, 5, 6, 7, 8, 9, 10])
    schedule.every().day.at("12:00").do(send_words, num_words_now=[8, 9, 10])
    schedule.every().day.at("13:00").do(send_words, num_words_now=[3, 4, 5, 6, 7, 9, 10])
    schedule.every().day.at("14:00").do(send_words, num_words_now=[2, 7, 8, 10])
    schedule.every().day.at("15:00").do(send_words, num_words_now=[4, 5, 6, 7, 8, 9, 10])
    schedule.every().day.at("16:00").do(send_words, num_words_now=[8, 9, 10])
    schedule.every().day.at("17:00").do(send_words, num_words_now=[3, 5, 6, 7, 8, 9, 10])
    schedule.every().day.at("18:00").do(send_words, num_words_now=[9, 10])

    while True:
        schedule.run_pending()
        time.sleep(1)


def check_translation(message, russian_word1, russian_word2, russian_word3):
    if (message.text.lower() == russian_word1.lower()) or (message.text.lower() == russian_word2.lower()) or \
            (message.text.lower() == russian_word3.lower()):
        bot.send_message(message.chat.id, '<b>Правильно!</b>', parse_mode='html')
    else:
        bot.send_message(message.chat.id, f'<b>Не верно.</b> Правильный перевод - {russian_word1} '
                                          f'{russian_word2} {russian_word3}', parse_mode='html')


def bot_polling():
    bot.polling(none_stop=True)


if __name__ == '__main__':
    thread_1 = threading.Thread(target=main)
    thread_2 = threading.Thread(target=bot_polling)
    thread_1.start()
    thread_2.start()
    thread_1.join()
    thread_2.join()
