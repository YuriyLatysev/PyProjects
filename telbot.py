import telebot

bot = telebot.TeleBot('5901360246:AAE34FfQ-FaM2UCVv1t4lrlEIdAHLqssea0')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, '<b>Hi</b>', parse_mode='html')
