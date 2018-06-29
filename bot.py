# from telegram.ext import Updater
# updater = Updater(token='528744932:AAEPt-yfHBZbNQ9aMIlAUyuMSTz-QilXM6M')
# url = 'http://api.rasp.nsuem.ru/?controller=Times&action=GetTime&key=80a07cadffa1169625e3d4849bd31e793e05e81a'

# dispatcher = updater.dispatcher

# import logging
# import requests
# import json
# import telegram
# from telegram import InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# def start(bot, update):
	# keyboard = [[InlineKeyboardButton("Option 1", callback_data="1"),
	# InlineKeyboardButton("Option 2", callback_data="2")],
	# [InlineKeyboardButton("Option 3", callback_data="3")]]
	# reply_markup = InlineKeyboardMarkup(keyboard)
	# update.message.reply_text('Please choose:', reply_markup=reply_markup)


# def r4751(bot, update):
	 # response = requests.get(url)
	 # bot.send_message(chat_id=update.message.chat_id, text=json.dumps(response.json()))

# def parsed(bot, update):
	# data = requests.get(url).json()
	# json_data = json.dumps(data)
	# parsed_json = json.loads(json_data)
	# s = json.dumps(parsed_json["data"][0]["TimeName"]).replace('"', '')
	# bot.send_message(chat_id=update.message.chat_id, text=s)
	
# def build_menu(buttons,n_cols,header_buttons=None,footer_buttons=None):
	# menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
	# if header_buttons: menu.insert(0, header_buttons)
	# if footer_buttons: menu.append(footer_buttons)
	# return menu

# def start_menu(bot, update):
	# button_list = [InlineKeyboardButton("col1", callback_data='1'),
	# InlineKeyboardButton("col2", callback_data='2'),
	# InlineKeyboardButton("row 2", callback_data='3')]
	# reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
	# bot.send_message(update.message.chat_id, "A two-column menu", reply_markup=reply_markup)
	
# def button(bot, update):
	# query = update.callback_query
	# bot.edit_message_text(text="Selected option: {}".format(query.data),
	# chat_id=query.message.chat_id,
	# message_id=query.message.message_id)
	
# from telegram.ext import CommandHandler
# start_handler = CommandHandler('start', start)
# dispatcher.add_handler(start_handler)

# r4751_handler = CommandHandler('r4751', r4751)
# dispatcher.add_handler(r4751_handler)

# parsed_handler = CommandHandler('parsed', parsed)
# dispatcher.add_handler(parsed_handler)

# start_menu_handler = CommandHandler('start_menu', start_menu)
# dispatcher.add_handler(start_menu_handler)

# button_handler = CallbackQueryHandler('button', button)
# dispatcher.add_handler(button_handler)

# updater.start_polling()
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import requests
import json

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)

def parsed():
	url = 'http://api.rasp.nsuem.ru/?controller=Times&action=GetTime&key=80a07cadffa1169625e3d4849bd31e793e05e81a'
	data = requests.get(url).json()
	json_data = json.dumps(data)
	parsed_json = json.loads(json_data)
	s = json.dumps(parsed_json["data"][0]["TimeName"]).replace('"', '')
	return s
	
def menu(bot, update):
	keyboard = [[InlineKeyboardButton("На сегодня", callback_data='1'),
	InlineKeyboardButton("На завтра", callback_data='2')],
	[InlineKeyboardButton("На неделю", callback_data='3'),
	InlineKeyboardButton("Полное", callback_data='4')],
	[InlineKeyboardButton("Преподаватели", callback_data='5'),
	InlineKeyboardButton("Новости", callback_data='6')],
	[InlineKeyboardButton("Настройки", callback_data='Настройки')]]
	reply_markup = InlineKeyboardMarkup(keyboard)
	update.message.reply_text('Выберите функцию:', reply_markup=reply_markup)

def settings():
	keyboard = [[InlineKeyboardButton("Изменить факультет", callback_data='1')],
	[InlineKeyboardButton("Изменить группу", callback_data='2')]]

def button(bot, update):
	query = update.callback_query
	chat_id=query.message.chat_id,
	message_id=query.message.message_id
	if format(query.data) == '1': 
	  s = parsed()
	  bot.send_message(chat_id=query.message.chat_id, text=s)
	if format(query.data) == '7':
	  settings()

def help(bot, update):
    update.message.reply_text("Use /start to test this bot.")


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the Updater and pass it your bot's token.
	updater = Updater("528744932:AAEPt-yfHBZbNQ9aMIlAUyuMSTz-QilXM6M")

	updater.dispatcher.add_handler(CommandHandler('menu', menu))
	updater.dispatcher.add_handler(CallbackQueryHandler(button))
	updater.dispatcher.add_handler(CommandHandler('help', help))
	updater.dispatcher.add_error_handler(error)
	updater.dispatcher.add_handler(CommandHandler('settings', settings))

    # Start the Bot
	updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
	updater.idle()


if __name__ == '__main__':
    main()