import telebot
import sqlite3

token = "6115247479:AAHIowrL7QTuVvUr8GZyKp0xDnVcTXSydvo"
bot = telebot.TeleBot(token)
name = None

@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('telegrambot.sql')
    curs = conn.cursor()
    curs.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))')
    conn.commit()
    curs.close()
    conn.close()
    bot.send_message(message.chat.id, 'Привет! Сейчас я тебя зарегистрирую! Введите имя!')
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(message, user_pass)

def user_pass(message):
    password = message.text.strip()
    conn = sqlite3.connect('telegrambot.sql')
    curs = conn.cursor()
    curs.execute("INSERT INTO users (name, pass) VALUES ('%s', '%s')" % (name, password))
    conn.commit()
    curs.close()
    conn.close()
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Список пользователей', callback_data='users'))
    bot.send_message(message.chat.id, 'Пользователь зарегистрирован', reply_markup=markup)

#Выводим список пользователей
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    conn = sqlite3.connect('telegrambot.sql')
    curs = conn.cursor()
    curs.execute("SELECT * FROM users")

    users = curs.fetchall()
    info = ''
    for i in users:
        info = info + f' Имя: {i[1]}, пароль: {i[2]}\n'

    bot.send_message(call.message.chat.id, info)
    curs.close()
    conn.close()


bot.polling(none_stop=True)

