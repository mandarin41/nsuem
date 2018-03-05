from telegram.ext import Updater
updater = Updater(token='528744932:AAEPt-yfHBZbNQ9aMIlAUyuMSTz-QilXM6M')
url = 'http://api.rasp.nsuem.ru/?controller=Times&action=GetTime&key=80a07cadffa1169625e3d4849bd31e793e05e81a'

dispatcher = updater.dispatcher

import logging
import requests
import json

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(bot, update):
     bot.send_message(chat_id=update.message.chat_id, text="Hello, world!")

def r4751(bot, update):
	 response = requests.get(url)
	 bot.send_message(chat_id=update.message.chat_id, text=json.dumps(response.json()))

from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()