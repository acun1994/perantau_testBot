# -*- coding: utf-8 -*-
import os
# import some_api_lib
# import ...

# Example of your code beginning
#           Config vars
token = os.environ['TELEGRAM_TOKEN']
#some_api_token = os.environ['SOME_API_TOKEN']
#             ...

# If you use redis, install this add-on https://elements.heroku.com/addons/heroku-redis
#r = redis.from_url(os.environ.get("REDIS_URL"))
import telegram
from telegram.ext import Updater, CommandHandler
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def sendMsg(bot, update, text):
	bot.sendMessage(
	chat_id = update.message.chat_id,
	text = text)
	
def log(username, chat_id, fucntionName):
	print('{} from {} triggered {}'.format(username, chat_id, functionName))

def start(bot, update):
	sendMsg(bot, update, 'Hello World!')

def hello(bot, update):
	sendMsg(bot, update, 'Hello {}'.format(update.message.from_user.first_name))
	
def test(bot, update):
	sendMsg(bot, update, 'Test received {}'.format(update.message.from_user.first_name))
	
def shrug(bot, update):
	sendMsg(bot, update, '{} : ¯\_(ツ)_/¯'.format(update.message.from_user.first_name))
	delete(bot, update.message)
	
def delete(bot, msg):
	if inGroup(bot, msg):
		logger.info('{} from {} triggered {}'.format(msg.from_user.first_name, msg.chat.title, 'delete'))
		del_msg_id = msg.message_id
		del_chat_id = msg.chat_id
		bot.deleteMessage(chat_id = del_chat_id, message_id = del_msg_id)
	else:
		logger.info('Could not {} in private chat {}'.format('delete', msg.chat.username ))
	
def inGroup(bot, msg):
	return msg.chat.get_members_count() > 2

updater = Updater(token)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('test', test))
updater.dispatcher.add_handler(CommandHandler('shrug', shrug))

updater.start_polling()
updater.idle()