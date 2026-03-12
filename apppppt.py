import telebot
from telebot import types
from yoomoney import *
import string
import time
from datetime import datetime, timedelta
import threading
import random
import requests
import torch
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from model_utils import (
    load_model, load_tokenizer, predict_comment,
    format_results, get_overall_verdict
)

MODEL_PATH = "russian_text_classifier.pth"

def load_toxicity_model():
    try:
        print("🔄 Загрузка модели токсичности...")

        if not os.path.exists(MODEL_PATH):
            print(f"❌ Файл модели {MODEL_PATH} не найден!")
            return None, None

        tokenizer = load_tokenizer()
        model = load_model(MODEL_PATH)

        print("✅ Модель успешно загружена!")
        return model, tokenizer

    except Exception as e:
        print(f"❌ Ошибка загрузки модели: {e}")
        return None, None

model, tokenizer = load_toxicity_model()

def check_toxicity(text):
    if model is None or tokenizer is None:
        bad_words = ['сука', 'блядь', 'хуй', 'пизда', 'ебать', 'дурак', 'идиот', 'козел', 'ублюдок']
        text_lower = text.lower()
        for word in bad_words:
            if word in text_lower:
                return True, "Токсично (заглушка)", 0.8, ["Оскорбление"]
        return False, "Норма (заглушка)", 0.5, []

    try:
        probabilities = predict_comment(text, model, tokenizer)
        results = format_results(probabilities)
        verdict = get_overall_verdict(results)

        is_toxic = "Норма" not in verdict or "обнаружена токсичность" in verdict.lower()

        toxic_categories = []
        for r in results:
            if r['is_detected'] and r['raw_label'] != "__label__NORMAL":
                toxic_categories.append(r['label'])

        main_category = toxic_categories[0] if toxic_categories else "Норма"
        max_confidence = max([r['probability'] / 100 for r in results])

        return is_toxic, main_category, max_confidence, toxic_categories

    except Exception as e:
        print(f"Ошибка при проверке токсичности: {e}")
        return False, "Ошибка", 0.0, []

zakazy = {}

tovar = {
    "Ягуар": {
        "Фри(0.47л) Ягуар": [1],
        "Культ(0.45л) Ягуар": [1],
        "Вайлд(0.47л) Ягуар": [1],
        "Лайв Нью Энерджи(0.45л) Ягуар": [1]
    },
    "Торнадо": {
        "Шторм(0.45л) Торнадо": [1],
        "Баббл(0.473л) Торнадо": [1],
        "Раззберри(0.45л) Торнадо": [1],
        "Манго(0.473л) Торнадо": [1],
        "Актив/Баббл(1л) Торнадо": [1],
        "Скилл(0.473л) Торнадо": [1]
    },
    "Адреналин": {
        "Раш(0.449л) Адреналин": [1],
        "Гуанабана Лайм(0.449л) Адреналин": [1]
    },
    "Берн": {
        "Классический(0.449л) Берн": [1],
        "Манго(0.449л) Берн": [1]
    },
    "Flash Up": {
        "Энерджи(0.5л) Flash Up": [1]
    }
}

API_TOKEN = '7341970699:AAHZHuBu53xukqUwqmld6lxGY8rt-T81C4M'
OPENROUTER_API_KEY = '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'
OPENROUTER_URL = 'https://openrouter.ai/api/v1/chat/completions'

korzina = {}
bot = telebot.TeleBot(API_TOKEN)

def ask_ai(prompt):
    headers = {
        'Authorization': f'Bearer {OPENROUTER_API_KEY}',
        'Content-Type': 'application/json'
    }

    data = {
        'model': 'openrouter/free',
        'messages': [
            {'role': 'user', 'content': f"Ты консультант по энергетикам. Коротко ответь на вопрос: {prompt}"}
        ],
        'max_tokens': 100,
        'temperature': 0.7
    }

    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json=data, timeout=10)

        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                if 'message' in result['choices'][0]:
                    return result['choices'][0]['message']['content']
                elif 'text' in result['choices'][0]:
                    return result['choices'][0]['text']
            return "🤔 Не могу сформулировать ответ. Попробуйте спросить конкретнее."
        else:
            return f"Ошибка API: {response.status_code}"
    except Exception as e:
        return f"😔 Ошибка: {str(e)}"

def proverka():
    token = "4100117911082711.0D52CBFCB2FDD1A08159D7981E09BEC1850A2476873721A7CFA81472BB99A7658A3ADD97040A183ED9C0E8A65352E0558B55BF0B13EAB264FDC39D13EEC73D54A19C7221B867B21BBD726503F1E5F97433ACECECD4C640D185D0042C82C8801A49C90C0D234DE449CEDC207F6FB14A89BBD5E8ADEE995CE1013629DFBF370E56"
    client = Client(token)
    expiration_time = timedelta(minutes=20)

    while True:
        try:
            to_remove = []

            for chat_id, data in list(zakazy.items()):
                if len(data) < 3:
                    data.append(datetime.now())
                if len(data) < 4:
                    data.append("pending")
                if len(data) < 5:
                    data.append("")
                if len(data) < 6:
                    data.append("")

                order_creation_time = data[2]

                if datetime.now() - order_creation_time > expiration_time:
                    bot.send_message(chat_id, "Срок годности заказа истек. Заказ был отменен.")
                    to_remove.append(chat_id)
                    continue

                if data[3] == "pending":
                    history = client.operation_history(label=data[0])

                    for operation in history.operations:
                        if operation.status == "success":
                            bot.send_message(chat_id, "✅ Оплата прошла успешно!")
                            bot.send_message(chat_id, "📍 Введите адрес доставки:")

                            data[3] = "waiting_address"

            for key in to_remove:
                zakazy.pop(key, None)

        except Exception as e:
            print("Ошибка в proverka:", e)

        time.sleep(10)

@bot.message_handler(func=lambda message: message.chat.id in zakazy and zakazy[message.chat.id][3] == "waiting_address")
def receive_address(message):
    chat_id = message.chat.id
    address = message.text

    zakazy[chat_id][4] = address
    zakazy[chat_id][3] = "waiting_comment"

    bot.send_message(chat_id, "📝 Теперь напишите комментарий для курьера (например, подъезд, этаж, код домофона):")
    bot.send_message(chat_id, "⚠️ Пожалуйста, избегайте нецензурных выражений - комментарий проверяется автоматически!")

@bot.message_handler(func=lambda message: message.chat.id in zakazy and zakazy[message.chat.id][3] == "waiting_comment")
def receive_comment(message):
    chat_id = message.chat.id
    comment = message.text

    is_toxic, category, confidence, toxic_categories = check_toxicity(comment)

    if is_toxic and confidence > 0.5:
        warning = f"⚠️ Ваш комментарий содержит *{category.lower()}* (уверенность: {confidence:.0%}).\n"
        if toxic_categories:
            warning += f"Обнаружено: {', '.join(toxic_categories)}\n"
        warning += "Пожалуйста, напишите комментарий заново, используя вежливые формулировки."
        bot.send_message(chat_id, warning, parse_mode='Markdown')
        return

    zakazy[chat_id][5] = comment
    zakazy[chat_id][3] = "completed"

    admin_msg = (
        f"🆕 *НОВЫЙ ЗАКАЗ*\n\n"
        f"{zakazy[chat_id][1]}\n\n"
        f"👤 Юзернейм: @{message.from_user.username}\n"
        f"📍 Адрес: {zakazy[chat_id][4]}\n"
        f"📝 Комментарий: {comment}\n"
    )

    try:
        total = zakazy[chat_id][1].split('Итого:')[1].split('руб')[0].strip()
        admin_msg += f"💰 Сумма: {total} руб\n"
    except:
        pass

    bot.send_message(-1003799725115, admin_msg, parse_mode='Markdown')

    bot.send_message(chat_id, "✅ Заказ оформлен! Спасибо за покупку!\nКурьер скоро свяжется с вами.")

    if chat_id in korzina:
        del korzina[chat_id]

threading.Thread(target=proverka, daemon=True).start()

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id != 1820789113 and message.chat.id != -1003799725115:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        Coffee_btn = types.KeyboardButton('Энергос')
        Trashbutton = types.KeyboardButton('Корзина')
        Consultant_btn = types.KeyboardButton('👨‍💼 Консультант')
        markup.add(Coffee_btn, Trashbutton, Consultant_btn)
        bot.send_message(message.chat.id, "🥤 Добро пожаловать!\nВыберите действие:", reply_markup=markup)
    elif message.chat.id == 1820789113:
        bot.send_message(message.chat.id, "Для крыс не доставляем")

@bot.message_handler(func=lambda message: message.text == "👨‍💼 Консультант")
def consultant_handler(message):
    if message.chat.id != 1820789113:
        bot.send_message(message.chat.id, "👋 Привет! Я консультант. Что хотите узнать об энергетиках?")
        bot.send_message(message.chat.id,
                         "Например, спросите:\n- Какой самый бодрящий?\n- Что со вкусом манго?\n- Какой лучше для учебы?")
        bot.register_next_step_handler(message, process_consultant_question)
    else:
        bot.send_message(message.chat.id, "Для крыс не консультируем")

def process_consultant_question(message):
    if message.chat.id != 1820789113:
        thinking = bot.send_message(message.chat.id, "🤔 Думаю...")
        response = ask_ai(message.text)
        bot.delete_message(message.chat.id, thinking.message_id)
        bot.send_message(message.chat.id, f"👨‍💼 *Консультант:*\n{response}", parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, "Для крыс не консультируем")

@bot.message_handler(func=lambda message: message.text == "Энергос")
def coffee_action(message):
    if message.chat.id != 1820789113:
        keyboard = telebot.types.InlineKeyboardMarkup()
        for brand in tovar.keys():
            keyboard.row(telebot.types.InlineKeyboardButton(text=brand.split(' ')[0], callback_data=brand))
        bot.send_message(message.chat.id, "Выберите бренд:", reply_markup=keyboard)
    elif message.chat.id == 1820789113:
        bot.send_message(message.chat.id, "Для крыс не доставляем")

@bot.callback_query_handler(func=lambda call: call.data in tovar.keys())
def brand_callback(call):
    keyboard = telebot.types.InlineKeyboardMarkup()
    for product in tovar[call.data].keys():
        keyboard.row(telebot.types.InlineKeyboardButton(text=product.split('(')[0], callback_data=product))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                          text=f"Выберите напиток {call.data}:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda
        call: call.data not in tovar.keys() and '123' not in call.data and call.data != "oplata" and not call.data.startswith(
    'delete_'))
def product_callback(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)

    product_name = call.data
    for brand, products in tovar.items():
        if product_name in products:
            price = products[product_name][0]

            if call.message.chat.id not in korzina:
                korzina[call.message.chat.id] = [[price, product_name]]
            else:
                korzina[call.message.chat.id].append([price, product_name])

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(
                types.KeyboardButton('Энергос'),
                types.KeyboardButton('Корзина'),
                types.KeyboardButton('👨‍💼 Консультант')
            )

            bot.send_message(call.message.chat.id,
                             f"✅ {product_name} добавлен в корзину!\n💰 Цена: {price} руб",
                             reply_markup=markup)
            break

@bot.message_handler(func=lambda message: message.text.lower() == "корзина" or message.text == "Корзина")
def show_cart(message):
    if message.chat.id == 1820789113:
        bot.send_message(message.chat.id, "Для крыс не продаем")
        return

    if message.chat.id not in korzina or not korzina[message.chat.id]:
        bot.send_message(message.chat.id, "🛒 Корзина пуста!")
        return

    cart = korzina[message.chat.id]
    total = 0
    text = "🛒 *Ваша корзина:*\n\n"

    keyboard = types.InlineKeyboardMarkup()

    for i, item in enumerate(cart):
        price = item[0]
        name = item[1]
        total += price
        text += f"{i + 1}. {name} — {price} руб\n"
        keyboard.row(types.InlineKeyboardButton(f"❌ Удалить", callback_data=f'delete_{i}'))

    delivery = 1
    final_total = total + delivery

    text += f"\n💰 Сумма: {total} руб\n🚚 Доставка: {delivery} руб\n💳 *ИТОГО: {final_total} руб*"

    keyboard.row(types.InlineKeyboardButton("💳 Оплатить", callback_data='oplata'))

    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_'))
def delete_from_cart(call):
    index = int(call.data.split('_')[1])
    chat_id = call.message.chat.id

    if chat_id in korzina and 0 <= index < len(korzina[chat_id]):
        del korzina[chat_id][index]
        if not korzina[chat_id]:
            del korzina[chat_id]
            bot.edit_message_text("🛒 Корзина пуста!", chat_id, call.message.message_id)
        else:
            cart = korzina[chat_id]
            total = 0
            text = "🛒 *Ваша корзина:*\n\n"

            keyboard = types.InlineKeyboardMarkup()

            for i, item in enumerate(cart):
                price = item[0]
                name = item[1]
                total += price
                text += f"{i + 1}. {name} — {price} руб\n"
                keyboard.row(types.InlineKeyboardButton(f"❌ Удалить", callback_data=f'delete_{i}'))

            delivery = 1
            final_total = total + delivery

            text += f"\n💰 Сумма: {total} руб\n🚚 Доставка: {delivery} руб\n💳 *ИТОГО: {final_total} руб*"

            keyboard.row(types.InlineKeyboardButton("💳 Оплатить", callback_data='oplata'))

            bot.edit_message_text(text, chat_id, call.message.message_id,
                                  parse_mode='Markdown', reply_markup=keyboard)
    else:
        bot.answer_callback_query(call.id, "❌ Товар не найден")

@bot.callback_query_handler(func=lambda call: call.data == "oplata")
def payment_handler(call):
    chat_id = call.message.chat.id

    if chat_id not in korzina or not korzina[chat_id]:
        bot.answer_callback_query(call.id, "🛒 Корзина пуста!")
        return

    label = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    cart = korzina[chat_id]
    total = sum(item[0] for item in cart)
    delivery = 1
    final_total = total + delivery

    order_desc = "Ваш заказ:\n"
    for item in cart:
        order_desc += f"• {item[1]} - {item[0]} руб\n"
    order_desc += f"\nДоставка: {delivery} руб\nИтого: {final_total} руб"

    try:
        quickpay = Quickpay(
            receiver="4100117911082711",
            quickpay_form="shop",
            targets="Энергетики",
            paymentType="SB",
            sum=final_total,
            label=label
        )

        zakazy[chat_id] = [label, order_desc, datetime.now(), "pending", "", ""]

        keyboard = types.InlineKeyboardMarkup()
        keyboard.row(types.InlineKeyboardButton("💳 Оплатить", url=quickpay.redirected_url))

        bot.delete_message(chat_id, call.message.message_id)
        bot.send_message(chat_id,
                         f"💳 *К оплате:* {final_total} руб\n\n"
                         f"Нажмите кнопку для оплаты через ЮMoney\n"
                         f"⏳ После оплаты введите адрес доставки",
                         parse_mode='Markdown', reply_markup=keyboard)

    except Exception as e:
        print(f"Ошибка платежа: {e}")
        bot.send_message(chat_id, "❌ Сервис оплаты временно недоступен")

if __name__ == "__main__":
    print("✅ Бот запущен!")
    if model is None:
        print("⚠️ Модель токсичности не загружена - используется базовая проверка по словам")
    else:
        print("✅ Модель токсичности успешно загружена!")
    bot.infinity_polling()