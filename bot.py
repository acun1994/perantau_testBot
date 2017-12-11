# -*- coding: utf-8 -*-
import os, telegram, re
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
Event = namedtuple('Event', 'username date name')

from telegram.ext import Updater,CommandHandler, MessageHandler, Filters
import logging

#def echo(bot, update):
#    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)
#echo_handler = MessageHandler(Filters.text, echo)
#dispatcher.add_handler(echo_handler)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

#Private chat tracker
private_chats = []
events= []
lastEventCaller = ''

datePattern = re.compile("(0[1-9]|[1-2][0-9]|31(?!(?:0[2469]|11))|30(?!02))(0[1-9]|1[0-2])(\d{2})")

#Helper functions
def sendMsg(bot, msg, text, reply = False):
	if (reply == True): reply_id = msg.message_id
	else: reply_id = None
	bot.sendMessage(
	chat_id = msg.chat_id,
	reply_to_message = reply_id,
	text = text,
	parse_mode=telegram.ParseMode.MARKDOWN)
	
def replyMsg(bot, msg, text):
	sendMsg(bot, msg, text, True)
	
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
	sendMsg(bot, update.message, 'Hello World!')
	privateChatTuple = PersonChat(update.message.from_user, update.message.chat_id)
	if (privateChatTuple not in private_chats):
		private_chats.append(privateChatTuple)
		print (private_chats)

def hello(bot, update):
	sendMsg(bot, update.message, 'Hello {}'.format(update.message.from_user.first_name))
	
def test(bot, update):
	logger.info('{} from {} triggered {}'.format(update.message.from_user.first_name, getChatName(update.message), 'test'))
	sendMsg(bot, update.message, 'Test received {}'.format(update.message.from_user.first_name))
	
def shrug(bot, update):
	sendMsg(bot, update.message, '{} : ¯\_(ツ)_/¯'.format(update.message.from_user.first_name))
	delete(bot, update.message)
	
#def event(bot, update):
#	if inGroup(update.message):
#		update.message.reply_text("Remember to start a private chat with me")
#		global lastEventCaller
#		lastEventCaller = PersonChat(update.message.from_user, update.message.chat_id, getChatName(update.message))
		
#		print("Tracking event from {} in {}".format(lastEventCaller.user.first_name, lastEventCaller.chat_name))
#	else:
#		if (lastEventCaller == ''):
#			update.message.reply_text("Please create an event from a group chat first")
#		else:
#			print("Attempting event from {} in {}".format(lastEventCaller.user.first_name, lastEventCaller.chat_name))
#			sendMsg(bot, lastEventCaller.chat_id, "{} created a test event".format(lastEventCaller.user.first_name))
#			lastEventCaller = ''

def event(bot, update, args):
	if (len(args) == 0):
		replyMsg(bot, update.message, 
			"\n\
			To create an event, use the following command \n\
			`/event add [DDMMYY] [event name]` \nFor multi-word names, just type as usual \n\
			\nTo view events , use the command \n\
			`/event list`")
	
	elif (args[0] == 'list'):
		if (len(events) == 0):
			text = 'No events currently'
		else:
			text = '';
			for event in events:
				text = text + event.date + ' : ' + event.name + '\n'
				
		replyMsg(bot, update.message, text)
			
	elif (args[0] == 'add'):
		if (len(args) < 3):
			replyMsg(bot, update.message, 
				"\n\
				To create an event, use the following command \n\
				`/event add [DDMMYY] [event name]` \nFor multi-word names, just type as usual")
		elif (bool(datePattern.match(args[1])) == False):
			replyMsg(bot, update.message, "Please use `DDMMYY` format for date")
		
		else:
			addedEvent = Event(update.message.from_user.username, args[1], ' '.join(args[2:]))
			events.append(addedEvent)
			replyMsg(bot, update.message, "Event added")
			
	
	else:
		replyMsg(bot, update.message, 
			"\n\
			To create an event, use the following command \n\
			`/event add [DDMMYY] [event name]` \nFor multi-word names, just type as usual \n\
			\nTo view events , use the command \n\
			`/event list`")
	
#Register handlers
updater = Updater(token)

dp = updater.dispatcher

#Command Handlers
dp.add_handler(CommandHandler('start', start))
dp.add_handler(CommandHandler('hello', hello))
dp.add_handler(CommandHandler('test', test))
dp.add_handler(CommandHandler('shrug', shrug))
dp.add_handler(CommandHandler('event', event, pass_args = True))

#Error Handlers
dp.add_error_handler(error)

updater.start_polling()
updater.idle()