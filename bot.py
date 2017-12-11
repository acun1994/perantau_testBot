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
from collections import namedtuple

PersonChat = namedtuple('PersonChat', 'user chat_id chat_name')

from telegram.ext import Updater,CommandHandler
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

#Private chat tracker
private_chats = []
events= []
lastEventCaller = ''

#Helper functions
def sendMsg(bot, chat_id, text):
	bot.sendMessage(
	chat_id = chat_id,
	text = text)
	
def inGroup(msg):
	return msg.chat.get_members_count() > 2
	
def getChatName(msg):
	if inGroup(msg):
		return msg.chat.title
	else:
		return msg.chat.username
		
def delete(bot, msg):
	if inGroup(msg):
		logger.info('{} from {} triggered {}'.format(msg.from_user.first_name, getChatName(msg), 'delete'))
		del_msg_id = msg.message_id
		del_chat_id = msg.chat_id
		bot.deleteMessage(chat_id = del_chat_id, message_id = del_msg_id)
	else:
		logger.info('Could not {} in private chat {}'.format('delete', getChatName(msg)))
	
#Error logging	
def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

#Command Handler Recipients
def start(bot, update):
	sendMsg(bot, update.message.chat_id, 'Hello World!')
	privateChatTuple = PersonChat(update.message.from_user, update.message.chat_id)
	if (privateChatTuple not in private_chats):
		private_chats.append(privateChatTuple)
		print (private_chats)

def hello(bot, update):
	sendMsg(bot, update.message.chat_id, 'Hello {}'.format(update.message.from_user.first_name))
	
def test(bot, update):
	logger.info('{} from {} triggered {}'.format(update.message.from_user.first_name, getChatName(update.message), 'test'))
	sendMsg(bot, update.message.chat_id, 'Test received {}'.format(update.message.from_user.first_name))
	
def shrug(bot, update):
	sendMsg(bot, update.message.chat_id, '{} : ¯\_(ツ)_/¯'.format(update.message.from_user.first_name))
	delete(bot, update.message)
	
def event(bot, update):
	if inGroup(update.message):
		update.message.reply_text("Remember to start a private chat with me first")
		global lastEventCaller
		lastEventCaller = PersonChat(update.message.from_user, update.message.chat_id, getChatName(update.message))
		
		print("Tracking event from {} in {}".format(lastEventCaller.user.first_name, lastEventCaller.chat_name))
	else:
		print("Attempting event from {} in {}".format(lastEventCaller.user.first_name, lastEventCaller.chat_name))
		if (lastEventCaller != ''):
			sendMsg(bot, lastEventCaller.chat_id, "{} created a test event".format(lastEventCaller.user.first_name))
			lastEventCaller = ''
	
#Register handlers
updater = Updater(token)

dp = updater.dispatcher

#Command Handlers
dp.add_handler(CommandHandler('start', start))
dp.add_handler(CommandHandler('hello', hello))
dp.add_handler(CommandHandler('test', test))
dp.add_handler(CommandHandler('shrug', shrug))
dp.add_handler(CommandHandler('event', event))

#Error Handlers
dp.add_error_handler(error)

updater.start_polling()
updater.idle()