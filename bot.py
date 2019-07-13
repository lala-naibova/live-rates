from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from sources import CentralBankSource
from datetime import datetime
import os

central = CentralBankSource()
def say_hi(bot, update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id, 'Salam!')
    bot.send_photo()

def parse_msg(msg):
    msg: str = msg[10:]
    money_index = msg.index(" ")
    money = msg[:money_index]
    from_index = msg.index(" ", money_index + 1)
    curr_from = msg[money_index + 1: from_index]
    curr_to = msg[from_index + 1:]
    return float(money), curr_from, curr_to


def try_parse_message(msg):
    # /exchange 58.82 asd azn
    parts = msg.split()

    if len(parts) != 4:
        return False, "Format düzgün deyil. Nümunə format: /exchange 100 usd azn"

    _, money, curr_from, curr_to = parts

    try:
        money = float(money)
    except ValueError:
        return False, f"{money} - rəqəm deyil"

    return True, money, curr_from, curr_to


def exchange_money(bot, update):
    chat_id = update.message.chat_id
    msg = update.message.text
    money, from_curr, to_curr = parse_msg(msg)
    from_rate = central.get_rate(from_curr)
    to_rate = central.get_rate(to_curr)
    result = round(money*from_rate/to_rate, 2)
    response_msg = f"{money} {from_curr} = {result} {to_curr}"
    bot.send_message(chat_id, response_msg)


def exchange_money2(bot, update):
    chat_id = update.message.chat_id
    msg = update.message.text
    success, *args = try_parse_message(msg)

    if not success:
        error_msg = args[0]
        bot.send_message(chat_id, error_msg)
    else:
        money, from_curr, to_curr = args

        is_valid = central.validate_currency(from_curr)[0]

        if not is_valid:
            bot.send_message(chat_id, f"'{from_curr}' dəstəklənmir")
            return

        is_valid = central.validate_currency(to_curr)[0]

        if not is_valid:
            bot.send_message(chat_id, f"'{to_curr}' dəstəklənmir")
            return

        if from_curr.lower() == to_curr.lower():
            bot.send_message(chat_id, f"{money} {from_curr}")
            return

        from_rate = central.get_rate(from_curr)
        to_rate = central.get_rate(to_curr)

        result = round(money*from_rate/to_rate, 2)
        response_msg = f"{money} {from_curr} = {result} {to_curr}"
        bot.send_message(chat_id, response_msg)


def message_format(rates):
    now = datetime.now()
    date = now.strftime('%d.%m.%Y')
    msg = f"💰💰💰 {date} - tarixinə olan AZN məzənnələri: \n 💰💰💰"
    for rate in rates:
        code = rate['code']
        name = rate['name']
        rate = rate['rate']
        msg += '\n {} ({}): {}'.format(name, code, rate)
    return msg


def send_all_rates(bot, update):
    all_rates = central.get_all_rates()
    chat_id = update.message.chat_id
    bot.send_message(chat_id,message_format(all_rates))


def start(bot, update):
    keyboard = [[InlineKeyboardButton("Məzənnələr", callback_data='rates'),
                 InlineKeyboardButton("Valyuta kalkulyatoru", callback_data='exchange')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.send_message(update.message.chat_id, "Əməliyyatlar:", reply_markup=reply_markup)


def button(bot, update):
    query = update.callback_query
    chat_id = update.effective_user.id
    if query.data == 'rates':
        all_rates = central.get_all_rates()
        msg = message_format(all_rates)
        #query.edit_message_text(msg)
        bot.send_message(chat_id, msg)
        start(bot, query)
    else:
        #query.edit_message_text(text="Selected option: {}".format(query.data))
        bot.send_message(chat_id, "Hal-hazırda işlək deyil 😢")
        start(bot, query)


token = os.environ['curr_token']
updater = Updater(token)

rates_handler = CommandHandler('rates', send_all_rates)
exchange_handler = CommandHandler('exchange', exchange_money2)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_handler(rates_handler)
updater.dispatcher.add_handler(exchange_handler)
updater.start_polling()

updater.idle()
