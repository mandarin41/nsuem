import telebot
from telebot import types
from telebot import logging
import sqlite3
import datetime
import requests
import json
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen

TOKEN = '528744932:AAEPt-yfHBZbNQ9aMIlAUyuMSTz-QilXM6M'
bot = telebot.TeleBot(TOKEN)

dict={
	"facnum":"",
	"gronum":"",
	"grolist":[[0 for x in range(100)] for y in range(100)]
	}
	
@bot.message_handler(commands=['start'])
def start(m):
	key = types.InlineKeyboardMarkup()
	key.add(types.InlineKeyboardButton(text='Расписание', callback_data="rasp"))
	key.add(types.InlineKeyboardButton(text='Новости', callback_data="news"))  
	key.add(types.InlineKeyboardButton(text='Настройки', callback_data="settings")) 
	msg=bot.send_message(m.chat.id, 'Выберите действие: ', reply_markup=key)
	logging.info(m.chat.id)
	
@bot.callback_query_handler(func=lambda c:True)
def inline(c):
	if c.data=='rasp':
		bot.edit_message_text(
		chat_id=c.message.chat.id,
		message_id=c.message.message_id,
		text="*Расписание*",
		parse_mode="markdown",
		reply_markup=rasp(c))
	elif c.data=='news':
		bot.edit_message_text(
		chat_id=c.message.chat.id,
		message_id=c.message.message_id,
		text="*Новости*",
		parse_mode="markdown",
		reply_markup=news())
	elif c.data=='settings':
		bot.edit_message_text(
		chat_id=c.message.chat.id,
		message_id=c.message.message_id,
		text="*Настройки*",
		parse_mode="markdown",
		reply_markup=settings())
	elif c.data=='back':
		bot.edit_message_text(
		chat_id=c.message.chat.id,
		message_id=c.message.message_id,
		text="*Возвращаемся назад...*",
		parse_mode="markdown",
		reply_markup=start(c.message))
	elif c.data=='back1':
		bot.edit_message_text(
		chat_id=c.message.chat.id,
		message_id=c.message.message_id,
		text="*Возвращаемся назад...*",
		parse_mode="markdown",
		reply_markup=settings())
	elif c.data=='back2':
		bot.edit_message_text(
		chat_id=c.message.chat.id,
		message_id=c.message.message_id,
		text="*Возвращаемся назад...*",
		parse_mode="markdown",
		reply_markup=rasp(c))
	elif c.data=='back3':
		bot.edit_message_text(
		chat_id=c.message.chat.id,
		message_id=c.message.message_id,
		text="*Возвращаемся назад...*",
		parse_mode="markdown",
		reply_markup=faculty_list())
	elif c.data=='back4':
		bot.edit_message_text(
		chat_id=c.message.chat.id,
		message_id=c.message.message_id,
		text="*Возвращаемся назад...*",
		parse_mode="markdown",
		reply_markup=change())
	elif c.data=='change':
		bot.edit_message_text(
		chat_id=c.message.chat.id,
		message_id=c.message.message_id,
		text="*Укажите ваш факультет*",
		parse_mode="markdown",
		reply_markup=faculty_list())
	elif re.match(r'fac', c.data):
		res = re.split(r'c', c.data,maxsplit=1)
		dict["facnum"]=res[1]
		bot.edit_message_text(
		chat_id=c.message.chat.id,
		message_id=c.message.message_id,
		text="*Укажите вашу группу*",
		parse_mode="markdown",
		reply_markup=group_list(dict["facnum"]))
	elif re.match(r'gro', c.data):
		res = re.split(r'o', c.data,maxsplit=1)
		dict["gronum"]=res[1]
		bot.edit_message_text(
		chat_id=c.message.chat.id,
		message_id=c.message.message_id,
		text="*Вы выбрали группу*",
		parse_mode="markdown",
		reply_markup=group_choose(dict["gronum"],c.message))
	elif c.data=='today':
		bot.edit_message_text(
		chat_id=c.message.chat.id,
		message_id=c.message.message_id,
		text=makecontent(c,0),
		parse_mode="markdown",
		reply_markup=today())
	elif c.data=='tomorrow':
		bot.edit_message_text(
		chat_id=c.message.chat.id,
		message_id=c.message.message_id,
		text=makecontent(c,1),
		parse_mode="markdown",
		reply_markup=tomorrow())
	elif c.data=='last':
		bot.edit_message_text(
		chat_id=c.message.chat.id,
		message_id=c.message.message_id,
		text="*Последняя новость*",
		parse_mode="markdown",
		reply_markup=last(c, 1))
	elif c.data=='last3':
		bot.edit_message_text(
		chat_id=c.message.chat.id,
		message_id=c.message.message_id,
		text="*Последние новости*",
		parse_mode="markdown",
		reply_markup=last(c, 3))
	elif c.data=='last10':
		bot.edit_message_text(
		chat_id=c.message.chat.id,
		message_id=c.message.message_id,
		text="*Последние новости*",
		parse_mode="markdown",
		reply_markup=last(c, 10))
		
def rasp(m):
	if(check_user(m)):
		key = types.InlineKeyboardMarkup()
		key.add(types.InlineKeyboardButton(text='На сегодня', callback_data="today"))
		key.add(types.InlineKeyboardButton(text='На завтра', callback_data="tomorrow")) 
		key.add(types.InlineKeyboardButton(text='На неделю', callback_data="week")) 
		key.add(types.InlineKeyboardButton(text='Полное', callback_data="full")) 
		key.add(types.InlineKeyboardButton(text='Назад', callback_data="back"))  
		return key
	else: bot.send_message(m.message.chat.id, "Укажите номер группы в настройках!")

def news():
	key = types.InlineKeyboardMarkup()
	key.add(types.InlineKeyboardButton(text='Последняя новость', callback_data="last"))
	key.add(types.InlineKeyboardButton(text='Последние 3 новости', callback_data="last3")) 
	key.add(types.InlineKeyboardButton(text='Последние 10 новостей', callback_data="last10")) 
	key.add(types.InlineKeyboardButton(text='Назад', callback_data="back"))  
	return key
	
def settings():
	key = types.InlineKeyboardMarkup()
	key.add(types.InlineKeyboardButton(text='Изменить группу', callback_data="change"))
	key.add(types.InlineKeyboardButton(text='Уведомления', callback_data="push")) 
	key.add(types.InlineKeyboardButton(text='Назад', callback_data="back"))  
	return key
	
def faculty_list():
	key = types.InlineKeyboardMarkup()
	conn = sqlite3.connect('botDB.db')
	cursor = conn.cursor()
	cursor.execute("SELECT faculty_name FROM faculties")
	results = cursor.fetchall()
	calc=1
	for row in results:
		key.add(types.InlineKeyboardButton(text=row[0], callback_data="fac"+str(calc)))
		calc=calc+1
	cursor.close()    
	conn.commit()
	key.add(types.InlineKeyboardButton(text='Назад', callback_data="back1"))  
	return key
	
def group_list(facnum):
	key = types.InlineKeyboardMarkup()
	conn = sqlite3.connect('botDB.db')
	cursor = conn.cursor()
	cursor.execute("SELECT group_name FROM groups WHERE faculty_id ="+ facnum)
	dict["grolist"] = cursor.fetchall()
	cursor.close()    
	conn.commit()
	calc=1
	for row in dict["grolist"]:
		key.add(types.InlineKeyboardButton(text=row[0], callback_data="gro"+str(calc)))
		calc=calc+1
	key.add(types.InlineKeyboardButton(text='Назад', callback_data="back3"))  
	return key
	
def group_choose(gronum,message):
	list=dict["grolist"]
	groupname=list[int(gronum)-1][0]          
	bot.send_message(message.chat.id, "Вы выбрали "+groupname)
	insertion=(message.chat.id, int(gronum)-1)
	conn = sqlite3.connect('botDB.db')
	cursor = conn.cursor()
	cursor.execute("INSERT OR REPLACE INTO bot_users VALUES (?,?)",insertion)
	cursor.close()    
	conn.commit()

def check_user(m):
	conn = sqlite3.connect('botDB.db')
	cursor = conn.cursor()
	cursor.execute("SELECT id FROM bot_users")
	userlist = cursor.fetchall()
	for userid in userlist:
		if userid[0] == m.message.chat.id:
			return True
		else: return False
	cursor.close()    
	conn.commit()

def today():
	key = types.InlineKeyboardMarkup()
	key.add(types.InlineKeyboardButton(text='Назад', callback_data="back2"))  
	return key

def tomorrow():
	key = types.InlineKeyboardMarkup()
	key.add(types.InlineKeyboardButton(text='Назад', callback_data="back2"))  
	return key

def makecontent(m,day):
	now = datetime.datetime.now()
	wk = now.isocalendar()[1]
	if wk % 2 == 0:
		owk = "0"
	else:
		owk = "-1"
	day += now.isocalendar()[2] - 1
	conn = sqlite3.connect('botDB.db')
	cursor = conn.cursor()
	cursor.execute("SELECT group_id FROM bot_users WHERE id =" + str(m.message.chat.id))
	id = cursor.fetchone()
	cursor1 = conn.cursor()
	cursor1.execute("SELECT group_name FROM groups WHERE id =" + str(id[0]))
	groupname=int(cursor1.fetchone()[0])
	url = 'http://api.rasp.nsuem.ru/?controller=Group&action=GetScheduleForGroup&groupname='+str(groupname)+'&subgroup=1&key=80a07cadffa1169625e3d4849bd31e793e05e81a'
	data = requests.get(url).json()
	dayno=str(day)
	subject=[]
	time=[]
	prep=[]
	room=[]
	content=""
	weekday = {
		"0": "Понедельник",
		"1": "Вторник",
		"2": "Среда",
		"3": "Четверг",
		"4": "Пятница",
		"5": "Суббота"
	}
	content = weekday[dayno]+'\n'+'🕓'+'       📗'+'             🚪'+'        👨🏻‍🏫'+'\n'
	for x in range(0,len(data["data"])-1):
		if data["data"][x]["dayno"] == dayno and data["data"][x]["oddweek"] == owk:
			subject.append(data["data"][x]["subjectshortname"])
			time.append(data["data"][x]["timename"])
			prep.append(data["data"][x]["teacher_shortname"])
			room.append(data["data"][x]["roomname"])
	for x in range(0,len(subject)):
		content += time[x]+' \t'+subject[x]+' \t'+room[x]+' \t'+prep[x]+'\n'
	return content

def last(m, num):
	for x in range (0, num):
		html_doc = urlopen('https://nsuem.ru/university/news-and-announces/').read()
		soup = BeautifulSoup(html_doc, 'html.parser')
		link_list=soup.find_all(href=re.compile("detail.php"))
		link1=link_list[x].get('href')
		next_page=urlopen('https://nsuem.ru'+link1).read()
		soup1=BeautifulSoup(next_page, 'html.parser')
		bot.send_message(m.message.chat.id, soup1.title)
		img_list=soup1.find_all(src=re.compile("upload"))
		img=img_list[0].get('src')
		bot.send_photo(m.message.chat.id, 'https://nsuem.ru' + img)
		txt_list=soup1.find_all(style="text-align: justify;")
		newstext=''
		for txt in txt_list:
			if len(txt.contents)>0:
				newstext = newstext + str(txt.get_text())
		bot.send_message(m.message.chat.id, newstext)

bot.polling()