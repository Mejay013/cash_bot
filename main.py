from datetime import datetime
from logging import raiseExceptions
import telebot
from telebot import types
import config
import db



bot = telebot.TeleBot(config.token)
keyboard = types.InlineKeyboardMarkup()
event = None

def send_message(user_id, text, check_keyboard = False):
    global bot, keyboard
    if check_keyboard != False:
        bot.send_message(user_id,text = text, reply_markup=keyboard)
    else:
        bot.send_message(user_id,text = text)


@bot.message_handler(commands=['start']) # вступителная функция
def start_message(message):
    set_keyboard()
    send_message(message.from_user.id, 'Выбираем', True) 

@bot.callback_query_handler(func=lambda call: True) #обработка кнопок
def callback_worker(call):
    global event
    if call.data == "cash_in":
        event = 'cash_in'
        send_message(call.message.chat.id, 'Введите сумму внесения')
    elif call.data == "cash_out":
        event = 'cash_out'
        send_message(call.message.chat.id, 'Введите сумму снятия')
    elif call.data == "cash_check":
        conn,cursor = db.connect()
        bank = db.get_bank(cursor)
        send_message(call.message.chat.id, f'Сумма бюджета = {bank} рублей',True)
        db.close_connect(conn,cursor)
    

def set_keyboard():
    global keyboard
    key_event = types.InlineKeyboardButton(text='Внести', callback_data='cash_in')
    key_event2 = types.InlineKeyboardButton(text='Списать', callback_data='cash_out')
    key_event3 = types.InlineKeyboardButton(text='Узнать баланс', callback_data='cash_check')
    keyboard.add(key_event,key_event2,key_event3)


@bot.message_handler(content_types=['text']) #обработка текстовых сообщений
def get_text_messages(message):
    try:  
        conn,cursor = db.connect()
        user_list = db.get_users(cursor)
        bank = db.get_bank(cursor)
        if event != None and message.from_user.id in user_list:
            if event == 'cash_in':
                sum = int(message.text.strip())
                user_name = db.get_user_name(cursor,message.from_user.id)
                if not sum > 0:
                    raise ValueError
                bank += sum
                if not (db.save_history(cursor,event,message.from_user.id,sum, bank)):
                    raise Exception
                send_message(user_list[0], f'Внесение денег {user_name}: {sum} рублей \nСумма бюджета составляет: {bank} рублей', True) #(!) 
                # for user in user_list:
                #     send_message(user, f'Внесение учтено \nСумма бюджета составляет: {bank} рублей', True)
            elif event == 'cash_out':
                sum = int(message.text.strip())
                user_name = db.get_user_name(cursor,message.from_user.id)
                if not sum > 0:
                    raise ValueError
                bank -= sum
                if not (db.save_history(cursor,event,message.from_user.id,sum,bank)):
                    raise Exception
                send_message(user_list[0], f'Снятие денег {user_name}: {sum} рублей \nСумма бюджета составляет: {bank} рублей', True) #(!)
                
                # for user in user_list:
                #     send_message(user, f'Внесение учтено \nСумма бюджета составляет: {bank} рублей', True)
            print('kek')
            if not (db.update_bank(cursor,bank)):
                raise Exception
            conn.commit()
            db.close_connect(conn,cursor)
    except ValueError:
        send_message(message.from_user.id, 'Введен неверный формат', False)
    except Exception as e:
        print(e)
        send_message(message.from_user.id, 'Я сломался', False)



bot.polling()