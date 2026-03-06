import telebot
from telebot import *
from yoomoney import *
import string
import time
from datetime import datetime, timedelta
import threading
import random

zakazy = {}

tovar = {
    "Ягуар": {
        "Фри(0.47л) Ягуар": [99],
        "Культ(0.45л) Ягуар": [89],
        "Вайлд(0.47л) Ягуар": [95],
        "Лайв Нью Энерджи(0.45л) Ягуар": [90]
    },
    "Торнадо": {
        "Шторм(0.45л) Торнадо": [89],
        "Баббл(0.473л) Торнадо": [92],
        "Раззберри(0.45л) Торнадо": [85],
        "Манго(0.473л) Торнадо": [90],
        "Актив/Баббл(1л) Торнадо": [120],
        "Скилл(0.473л) Торнадо": [93]
    },
    "Адреналин": {
        "Раш(0.449л) Адреналин": [95],
        "Гуанабана Лайм(0.449л) Адреналин": [100]
    },
    "Берн": {
        "Классический(0.449л) Берн": [105],
        "Манго(0.449л) Берн": [110]
    },
    "Flash Up": {
        "Энерджи(0.5л) Flash Up": [87]
    }
}
API_TOKEN = '7341970699:AAHZHuBu53xukqUwqmld6lxGY8rt-T81C4M'

korzina = {}
bot = telebot.TeleBot(API_TOKEN)


def proverka():
    token = "4100117911082711.0D52CBFCB2FDD1A08159D7981E09BEC1850A2476873721A7CFA81472BB99A7658A3ADD97040A183ED9C0E8A65352E0558B55BF0B13EAB264FDC39D13EEC73D54A19C7221B867B21BBD726503F1E5F97433ACECECD4C640D185D0042C82C8801A49C90C0D234DE449CEDC207F6FB14A89BBD5E8ADEE995CE1013629DFBF370E56"
    client = Client(token)
    expiration_time = timedelta(minutes=20)

    while True:
        try:
            to_remove = []

            for chat_id, data in list(zakazy.items()):
                if len(data) < 3:
                    zakazy[chat_id].append(datetime.now())
                    zakazy[chat_id].append("pending")

                order_creation_time = zakazy[chat_id][2]

                if datetime.now() - order_creation_time > expiration_time:
                    bot.send_message(chat_id, "Срок годности заказа истек. Заказ был отменен.")
                    to_remove.append(chat_id)
                    continue

                if zakazy[chat_id][3] == "pending":
                    history = client.operation_history(label=zakazy[chat_id][0])

                    for operation in history.operations:
                        if operation.status == "success":
                            bot.send_message(chat_id, "Оплата прошла успешно, ваш заказ в обработке.")
                            bot.send_message(chat_id, "Введите, куда доставить напиток, одним сообщением.")


                            zakazy[chat_id][3] = "paid"

            for key in to_remove:
                zakazy.pop(key, None)

        except Exception as e:
            print("Ошибка:", e)

        time.sleep(10)
        print("Текущие заказы:", zakazy)



@bot.message_handler(func=lambda message: message.chat.id in zakazy and zakazy[message.chat.id][3] == "paid")
def receive_address(message):
    chat_id = message.chat.id
    bot.send_message(-1002274574983, text=zakazy[chat_id][1] + "\n" + "Юзернейм:@" + message.from_user.username + "\n" + "Доставить в:\n" + message.text)

    zakazy.pop(chat_id, None)

    bot.send_message(chat_id, "Ваш заказ передан на доставку. Спасибо за покупку!")

threading.Thread(target=proverka).start()
@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id != 1820789113 and message.chat.id != -1002274574983:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        Coffee_btn = types.KeyboardButton('Энергос')
        Trashbutton = types.KeyboardButton('Корзина')
        markup.add(Coffee_btn, Trashbutton)
        bot.send_message(message.chat.id, "Добро Пожаловать!\nВыберите действие:", reply_markup=markup)
    elif message.chat.id == 1820789113:
        bot.send_message(message.chat.id, "Для крыс не доставляем")



@bot.message_handler(func=lambda message: message.text == "Энергос")
def coffee_action(message):
    if message.chat.id != 1820789113:
        keyboard = telebot.types.InlineKeyboardMarkup()
        for i in range(len(tovar.keys())):
            keyboard.row(telebot.types.InlineKeyboardButton(text=f"{list(tovar.keys())[i].split(' ')[0]}", callback_data=f"{list(tovar.keys())[i]}"))
        bot.send_message(message.chat.id, "Выберите напиток из меню", reply_markup=keyboard)
    elif message.chat.id == 1820789113:
        bot.send_message(message.chat.id, "Для крыс, не доставляем")


@bot.callback_query_handler(func=lambda call: call.data in list(tovar.keys()))
def cof_btn(call):
    keyboard = telebot.types.InlineKeyboardMarkup()
    for i in range(len(tovar[call.data].keys())):
        keyboard.row(telebot.types.InlineKeyboardButton(text=f"{list(tovar[call.data].keys())[i].split(' ')[0]}",
                                                        callback_data=f'{list(tovar[call.data].keys())[i]}'))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="Выберите напиток из меню", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data not in list(tovar.keys()) and '123' not in call.data and call.data != "oplata" and call.data != "pay" and "delete_" not in call.data)
def ctfh_btn(call):
    markup = telebot.types.InlineKeyboardMarkup()
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
    opt = len(tovar[call.data.split(' ')[-1]][call.data])
    match opt:
        case 2:
            markup.add(telebot.types.InlineKeyboardButton(text=f"0.3 | {tovar[call.data.split(' ')[-1]][call.data][0]}руб\n",
                                                            callback_data=f'{call.data} 0.3 {tovar[call.data.split(' ')[-1]][call.data][0]} 123'))
            markup.add(telebot.types.InlineKeyboardButton(text=f"0.4 | {tovar[call.data.split(' ')[-1]][call.data][1]}руб\n",
                                                          callback_data=f'{call.data} 0.4 {tovar[call.data.split(' ')[-1]][call.data][1]} 123'))
        case 3:
            markup.add(telebot.types.InlineKeyboardButton(text=f"0.2 | {tovar[call.data.split(' ')[-1]][call.data][0]}руб\n",
                                                          callback_data=f'{call.data} 0.2 {tovar[call.data.split(' ')[-1]][call.data][0]} 123'))
            markup.add(telebot.types.InlineKeyboardButton(text=f"0.3 | {tovar[call.data.split(' ')[-1]][call.data][1]}руб\n",
                                                          callback_data=f'{call.data} 0.3 {tovar[call.data.split(' ')[-1]][call.data][1]} 123'))
            markup.add(telebot.types.InlineKeyboardButton(text=f"0.4 | {tovar[call.data.split(' ')[-1]][call.data][2]}руб\n",
                                                          callback_data=f'{call.data} 0.4 {tovar[call.data.split(' ')[-1]][call.data][2]} 123'))
    if opt != 1:
        bot.send_message(call.message.chat.id, "Выберите объем: ", reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        Coffee_btn = types.KeyboardButton('Энергос')
        Trashbutton = types.KeyboardButton('Корзина')
        markup.add(Coffee_btn, Trashbutton)
        bot.send_message(chat_id=call.message.chat.id, text="Товар добавлен в корзину!\nОтправьте слово *КОРЗИНА* для отображения вашей корзины", reply_markup=markup, parse_mode='Markdown')
        if call.message.chat.id not in korzina:
            korzina.update({call.message.chat.id: [[tovar[call.data.split(' ')[-1]][call.data][0], call.data.split(' ')[1] + " " + call.data.split(' ')[0]]]})
        else:
            korzina[call.message.chat.id].append([tovar[call.data.split(' ')[-1]][call.data][0], call.data.split(' ')[1] + " " + call.data.split(' ')[0]])


@bot.callback_query_handler(func=lambda call: '123' in call.data)
def printerok(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    Coffee_btn = types.KeyboardButton('Энергос')
    Trashbutton = types.KeyboardButton('Корзина')
    markup.add(Coffee_btn, Trashbutton)
    bot.send_message(chat_id=call.message.chat.id,
                     text="Товар добавлен в корзину!\nОтправьте слово *КОРЗИНА* для отображения вашей корзины",
                     reply_markup=markup, parse_mode='Markdown')
    bufferik = call.data.split(" ")
    print(bufferik)
    if call.message.chat.id not in korzina:
        korzina.update(
            {call.message.chat.id: [[bufferik[3], bufferik[0], bufferik[2]]]})
    else:
        korzina[call.message.chat.id].append([bufferik[3], bufferik[0], bufferik[2]])


@bot.message_handler(func=lambda message: True)
def coffee_cart(message):
    if message.content_type == "text" and message.text.lower() == "корзина" and message.chat.id != 1820789113:
        if message.chat.id not in korzina:
            bot.send_message(message.chat.id, "Ваша корзина пуста!")
        else:
            buffer = korzina[message.chat.id]
            vivod = ""
            price = 0
            keyboard = telebot.types.InlineKeyboardMarkup()

            for i in range(len(buffer)):
                if len(buffer[i]) == 2:
                    vivod += f"Цена: {buffer[i][0]}руб\nНапиток: {buffer[i][1]}\n\n"
                    keyboard.add(telebot.types.InlineKeyboardButton(
                        text=f"Удалить {buffer[i][1].split(" ")[1]}",
                        callback_data=f'delete_{i}'
                    ))
                elif len(buffer[i]) == 3:
                    vivod += f"Цена: {buffer[i][0]}руб\nНапиток: {buffer[i][1]}\nОбъем: {buffer[i][2]}\n\n"
                    keyboard.add(telebot.types.InlineKeyboardButton(
                        text=f"Удалить {buffer[i][1]} {buffer[i][2]}",
                        callback_data=f'delete_{i}'
                    ))
                price += int(buffer[i][0])
            navar = price * 0.1
            price += navar
            vivod += f"\nИтого: *{price + 20}руб*\n(в стоимость включена доставка)"
            keyboard.row(telebot.types.InlineKeyboardButton(text=f"Перейти к оплате", callback_data=f'oplata'))
            bot.send_message(message.chat.id, vivod, parse_mode="Markdown", reply_markup=keyboard)
    elif message.chat.id == 1820789113:
        bot.send_message(message.chat.id, "Для крыс, не доставляем")


@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_'))
def delete_from_cart(call):
    index = int(call.data.split('_')[1])
    chat_id = call.message.chat.id
    if chat_id in korzina and 0 <= index < len(korzina[chat_id]):
        del korzina[chat_id][index]
        if not korzina[chat_id]:
            del korzina[chat_id]
            updatecart(call.message)
        else:
            updatecart(call.message)
    else:
        bot.answer_callback_query(call.id, "Ошибка: товар не найден.")


@bot.callback_query_handler(func=lambda call: call.data == "oplata")
def printe34(call):
    a = string.digits + string.ascii_lowercase + string.ascii_uppercase
    b = ''
    for i in range(10):
        b += a[random.randint(0, len(a) - 1)]
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
    buffer = korzina[call.message.chat.id]
    vivod = ""
    price = 0
    colvo = 0
    print(buffer)
    for i in range(len(buffer)):
        if len(buffer[i]) == 2:
            vivod += f"Цена: {buffer[i][0]}руб\nНапиток: {buffer[i][1]}\n\n"
        elif len(buffer[i]) == 3:
            vivod += f"Цена: {buffer[i][0]}руб\nНапиток: {buffer[i][1]}\nОбъем: {buffer[i][2]}\n\n"
        price += int(buffer[i][0])
        colvo += 1
    navar = price * 0.1
    price += navar

    try:
        quickpay = Quickpay(
            receiver="4100117911082711",
            quickpay_form="shop",
            targets="Sponsor this project",
            paymentType="SB",
            sum=price + 20,
            label=b
        )
        vivod = vivod.rstrip("\n")
        zakazy.update({call.message.chat.id: [b, vivod + f"\nПрибыль с заказа: {navar}"]})
        testirovaniy = quickpay.redirected_url
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(telebot.types.InlineKeyboardButton(text=f"Оплатить", url=testirovaniy))
        bot.send_message(call.message.chat.id, text=f"К оплате: {price + 20}руб\nКол-во товаров: {colvo}",
                         reply_markup=keyboard)
    except Exception as e:
        print(f"Ошибка создания платежа: {e}")
        bot.send_message(call.message.chat.id, "Извините, сервис оплаты временно недоступен. Попробуйте позже.")


def updatecart(message):
    if message.chat.id not in korzina:
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.id, text="Ваша корзина пуста!")
    else:
        buffer = korzina[message.chat.id]
        vivod = ""
        price = 0
        keyboard = telebot.types.InlineKeyboardMarkup()

        for i in range(len(buffer)):
            if len(buffer[i]) == 2:
                vivod += f"Цена: {buffer[i][0]}руб\nНапиток: {buffer[i][1]}\n\n"
                keyboard.add(telebot.types.InlineKeyboardButton(
                    text=f"Удалить {buffer[i][1]}",
                    callback_data=f'delete_{i}'
                ))
            elif len(buffer[i]) == 3:
                vivod += f"Цена: {buffer[i][0]}руб\nНапиток: {buffer[i][1]}\nОбъем: {buffer[i][2]}\n\n"
                keyboard.add(telebot.types.InlineKeyboardButton(
                    text=f"Удалить {buffer[i][1]} {buffer[i][2]}",
                    callback_data=f'delete_{i}'
                ))
            price += int(buffer[i][0])
        navar = price * 0.1
        price += navar
        vivod += f"\nИтого: *{str(price + 20)}руб*\n(в стоимость включена доставка)"
        keyboard.row(telebot.types.InlineKeyboardButton(text=f"Перейти к оплате", callback_data=f'oplata'))
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=vivod, parse_mode="Markdown", reply_markup=keyboard)

bot.polling()


