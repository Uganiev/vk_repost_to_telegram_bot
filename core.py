import logging
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.error import BadRequest, TimedOut
from time import sleep
import threading
import vk
from time import time, ctime


token = '399c6451287482a319f1733ad76df32bb0ca5365df3f4a3c65c6dca504ac101556721478938a08f403c74'
session = vk.Session(access_token = token)
vk_api = vk.API(session)

def get_news_feed():
	source = []
	data = vk_api.newsfeed.get(v = 5.52, filters = 'post', start_time = time() - 360)
	for group in data:
		for element in data[group]:
			if 'attachments' in element.keys():
				for item in element['attachments']:
					if item['type'] == 'photo':
						if 'photo_1280' in item['photo'].keys():
							source.append([item['photo']['photo_1280'], item['photo']['text']])
						elif 'photo_720' in item['photo'].keys():
							source.append([item['photo']['photo_720'], item['photo']['text']])
					elif item['type'] == 'link':
						source.append([item['link']['url'], item['link']['title']])
	return source


token = '399c6451287482a319f1733ad76df32bb0ca5365df3f4a3c65c6dca504ac101556721478938a08f403c74'

session = vk.Session(access_token = token)
vk_api = vk.API(session)

updater = Updater(token = '596835691:AAH7ptPUatH10tXSnf036S7tJ5BNslB9ipY')
dispatcher = updater.dispatcher
logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class Counter(threading.Thread):
	def __init__(self, bot, update, chat_id):
		super().__init__()
		self.bot = bot
		self.update = update
		self.chat_id = chat_id
	def run(self):
		while True:
			vkwall(self.bot, self.update, self.chat_id)
			sleep(360)

def vkwall(bot, update, chat_id):
	data = get_news_feed()
	for block in data:
		try:
			bot.send_photo(chat_id = chat_id, photo = block[0], caption = block[1], timeout = 6000)
		except BadRequest:
			continue
		except TimedOut:
			continue
		

def start(bot, update):
	chat_id = update.message.chat_id
	bot.send_message(chat_id = chat_id, text = "Hi!", timeout = 600)
	Counter(bot, update, chat_id).start()


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()

# PATH: cd desktop/python_edu/vk_wall