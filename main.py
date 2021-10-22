from datetime import datetime
import telebot
from telebot import types
import config



bot = telebot.TeleBot(config.token)
keyboard = types.InlineKeyboardMarkup()
event = None
bank = 0

def send_message(user_id, text, check_keyboard = False):
    global bot, keyboard
    if check_keyboard != False:
        bot.send_message(user_id,text = text, reply_markup=keyboard)
    else:
        bot.send_message(user_id,text = text)


@bot.message_handler(commands=['start']) # вступителная функция
def start_message(message):
    set_keyboard()
    send_message(message.from_user.id, 'Напиши сюда чото', True) 

@bot.callback_query_handler(func=lambda call: True) #обработка кнопок
def callback_worker(call):
    global event
    global bank
    if call.data == "cash_in":
        event = 'cash_in'
        send_message(call.message.chat.id, 'Введите сумму внесения')
    elif call.data == "cash_out":
        event = 'cash_out'
        send_message(call.message.chat.id, 'Введите сумму снятия')
    elif call.data == "cash_check":
        send_message(call.message.chat.id, f'Сумма бюджета = {bank} рублей',True)
    

def set_keyboard():
    global keyboard
    key_event = types.InlineKeyboardButton(text='Внести', callback_data='cash_in')
    key_event2 = types.InlineKeyboardButton(text='Списать', callback_data='cash_out')
    key_event3 = types.InlineKeyboardButton(text='Узнать баланс', callback_data='cash_check')
    keyboard.add(key_event,key_event2,key_event3)


@bot.message_handler(content_types=['text']) #обработка текстовых сообщений
def get_text_messages(message):
    global bank
    try:    
        if event != None and message.from_user.id in config.access_id:
            print(message.from_user.id, event)
            if event == 'cash_in':
                sum = int(message.text.strip())
                if not sum > 0:
                    raise ValueError
                bank += sum
                for user in config.access_id:
                    send_message(user, f'Внесение учтено \nСумма бюджета составляет: {bank} рублей', True)
            elif event == 'cash_out':
                sum = int(message.text.strip())
                if not sum > 0:
                    raise ValueError
                bank -= sum
                for user in config.access_id:
                    send_message(user, f'Внесение учтено \nСумма бюджета составляет: {bank} рублей', True)
    except ValueError:
        send_message(message.from_user.id, 'Введен неверный формат', False)



bot.polling()