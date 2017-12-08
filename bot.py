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
from telegram.ext import Updater, CommandHandler

def start(bot, update):
	update.message.reply_text('Hello World!')

def hello(bot, update):
	update.message.reply_text(
	'Hello {}'.format(update.message.from_user.first_name))
	
def test(bot, update):
	update.message.reply_text(
	'Test received {}'.format(update.message.from_user.first_name))

updater = Updater(token)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('test', test))

updater.start_polling()
updater.idle()