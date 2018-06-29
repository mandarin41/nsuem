from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater
from telegram.ext import CallbackQueryHandler
import os
import logging
import requests
import json
import sqlite3

user_faculty=0
user_group=''

conn = sqlite3.connect('botDB.db')

cursor = conn.cursor()

cursor.execute("SELECT group_name FROM groups WHERE faculty_id = 1")

results = cursor.fetchall()

from tgmagic.buttons import PrevButton
from tgmagic.bot import MagicFunction
from tgmagic.helper import menu

my_custom_menu = {
	'menu': {
		'rasp': 'Расписание',
		'rasp_nested': {
			'stud': 'Студенты',
			'prep': 'Преподаватели',
			'prev': PrevButton('◀️Назад'),
			'stud_nested': {
				'today': 'На сегодня',
				'tommorow': 'На завтра',
				'week': 'На неделю',
				'full': 'Полное',
				'prev': PrevButton('◀️Назад')
				},
		},
		'news': 'Новости',
		'news_nested': {
			'last1': 'Последняя новость',
			'last3': 'Последние три',
			'last10': 'Последние 10',
			'prev': PrevButton('◀️Назад')
					},
		'settings': 'Настройки',
		'settings_nested': {
			'change': 'Сменить группу',
			'notifications': 'Уведомления',
			'prev': PrevButton('◀️Назад'),
			'change_nested': {
				'itf': 'ИТФ',
				'fbp': 'ФБП',
				'fkep': 'ФКЭП',
				'uf': 'ЮФ',
				'fgs': 'ФГС',
				'prev': PrevButton('◀️Назад'),
				# 'itf_nested': {
					# 'prev': PrevButton('◀️Назад'),
					# 'itf1': '11-ПИ501',
					# 'itf2': '11-ПИ601',
					# 'itf3': '3ЭБ61',
					# 'itf4': '4711',
					# 'itf5': '4721',
					# 'itf6': '4722',
					# 'itf7': '4731',
					# 'itf8': '4741',
					# 'itf9': '4751',
					# 'itf10': '4761',
					# 'itf11': '9-ПИ401',
					# 'itf12': '9-ПИ501',
					# 'itf13': 'аИС401',
					# 'itf14': 'аИС41',
					# 'itf15': 'аИС501',
					# 'itf16': 'аИС601',
					# 'itf17': 'аИС701',
					# 'itf18': 'аИС71',
					# 'itf19': 'АП501',
					# 'itf20': 'ИБ501',
					# 'itf21': 'ИН501',
					# 'itf22': 'ИС501',
					# 'itf23': 'мБИ601',
					# 'itf24': 'мБИ61',
					# 'itf25': 'мБИ71',
					# 'itf26': 'мБИ71в',
					# 'itf27': 'мИН61',
					# 'itf28': 'мИН71',
					# 'itf29': 'мИН71в',
					# 'itf30': 'мПИ601',
					# 'itf31': 'мПИ71',
					# 'itf32': 'мПИ71в',
					# 'itf33': 'мУБИ61',
					# 'itf34': 'мУБИ71',
					# 'itf35': 'мЭЛБ51',
					# 'itf36': 'мЭЛБ601',
					# 'itf37': 'мЭЛБ61',
					# 'itf38': 'мЭЛБ71',
					# 'itf39': 'мЭЛБ71в',
					# 'itf40': 'ПИ501',
					# 'itf41': 'ФИ501',
					# 'itf42': 'ЭБ501',
					# 'itf43': 'ЭБ51'
				# },
				# 'fbp_nested': {
						# 'fbp1': '',
						# 'fbp2': '',
						# 'fbp3': '',
						# 'fbp4': '',
						# 'fbp5': '',
						# 'fbp6': '',
						# 'fbp7': '',
						# 'fbp8': '',
						# 'fbp9': '',
						# 'fbp10': '',
						# 'fbp11': '',
						# 'fbp12': '',
						# 'fbp13': '',
						# 'fbp14': '',
						# 'fbp15': '',
						# 'fbp16': '',
						# 'fbp17': '',
						# 'fbp18': '',
						# 'fbp19': '',
						# 'fbp20': '',
						# 'fbp21': '',
						# 'fbp22': '',
						# 'fbp23': '',
						# 'fbp24': '',
						# 'fbp25': '',
						# 'fbp26': '',
						# 'fbp27': '',
						# 'fbp28': '',
						# 'fbp29': '',
						# 'fbp30': '',
						# 'fbp31': '',
						# 'fbp32': '',
						# 'fbp33': '',
						# 'fbp34': '',
						# 'fbp35': '',
						# 'fbp36': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
						# 'fbp': '',
				# }
			},
			'notifications_nested': {
				'daily': 'Ежедневно',
				'weekly': 'Еженедельно',
				'disable': 'Отключить уведомления',
				'prev': PrevButton('◀️Назад')},
			}
		},
	}

class TestBot(MagicFunction):

	def start(self, bot, update):
		bot.sendMessage(
		text='Выберите функцию:',
		chat_id=update.message.chat_id,
		reply_markup=self.gen_keyboard(update)
		)
		
	def rasp(self, bot, update):
		bot.sendMessage(
		text='Выбери расписание',
		chat_id=update.message.chat_id,
		reply_markup=self.gen_keyboard(update)
		)

	def stud(self, bot, update):
		text = 'Выбери период' + os.linesep
		bot.sendMessage(
		text=text,
		chat_id=update.message.chat_id,
		reply_markup=self.gen_keyboard(update)
		)

	def news(self, bot, update): 
		text = 'Выбери количество новостей' + os.linesep
		bot.sendMessage(
		text=text,
		chat_id=update.message.chat_id,
		reply_markup=self.gen_keyboard(update))

	def settings(self, bot, update): bot.sendMessage(
			text='Изменить настройки',
			chat_id=update.message.chat_id,
			reply_markup=self.gen_keyboard(update))

	def change(self, bot, update):
		bot.sendMessage(
		text='Выберите факультет',
		chat_id=update.message.chat_id,
		reply_markup=self.gen_keyboard(update)
		)
	
	def itf(self, bot, update):
		bot.sendMessage(
		text='Вы выбрали ИТФ! Введите номер группы: ',
		chat_id=update.message.chat_id,
		reply_markup=self.gen_keyboard(update))
		user_faculty=1
		response = bot.getUpdates()
		user_group=response.message.text
	
	def fbp(self, bot, update):
		bot.sendMessage(
		text=user_group,
		chat_id=update.message.chat_id,
		reply_markup=self.gen_keyboard(update))
		user_faculty=2
	
	def fkep(self, bot, update):
		bot.sendMessage(
		text='Вы выбрали ФКЭП!',
		chat_id=update.message.chat_id,
		reply_markup=self.gen_keyboard(update))
		user_faculty=3
		
	def uf(self, bot, update):
		bot.sendMessage(
		text='Вы выбрали ЮФ!',
		chat_id=update.message.chat_id,
		reply_markup=self.gen_keyboard(update))
		user_faculty=4
		
	def fgs(self, bot, update):
		bot.sendMessage(
		text=update.message.text,
		chat_id=update.message.chat_id,
		reply_markup=self.gen_keyboard(update))
		user_faculty=5
		
	def itf_group(self, bot, update):
		bot.send_message(message.chat.id, message.text)
		
	# def group(self, bot, update):
	
	# def notifications(self, bot, update):
	
	
	def prev(self, bot, update): bot.sendMessage(
			text='Возращаемся назад...',
			chat_id=update.message.chat_id,
			reply_markup=self.gen_keyboard(update))

	@menu
	def text(self, bot, update):
		pass

	def main(self):
		self.set_custom_menu(my_custom_menu)
		updater = Updater('528744932:AAEPt-yfHBZbNQ9aMIlAUyuMSTz-QilXM6M')
		dp = updater.dispatcher
		dp.add_handler(CommandHandler('start', self.start))
		dp.add_handler(MessageHandler(Filters.text, self.text))
		updater.start_polling()
		updater.idle()

TestBot().main()
conn.close()