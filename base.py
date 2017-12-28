# DEF : Imports
import telegram, logging

# LOG : Logger declaration
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# DEF : custom switch to receive query_data and currentName from button()
def textContentDict(arg, currentName):
	textContent = {
		'1': 'Hello {}'.format(currentName),
		'2': 'Test received {}'.format(currentName),
		'3': '{} has paid respects to art thou'.format(currentName),
		'4': '¯\\\_(ツ)\_/¯'
	}
	return textContent.get(arg, 'wtf u clicking m8')

# FUN : Sends message
def sendMsg(bot, msg, text, reply = False, keyboard = False):
	reply_id = None
	reply_markup_flag = None
	if (reply is True): 
		reply_id = msg.message_id
	if (keyboard is True):
		reply_markup_flag = markup
	return bot.sendMessage(
		chat_id = msg.chat_id,
		reply_to_message_id = reply_id,
		text = text,
		parse_mode = telegram.ParseMode.MARKDOWN,
		reply_markup = reply_markup_flag
	)

# FUN : Sends a reply message to msg
def replyMsg(bot, msg, text):
	sendMsg(bot, msg, text, reply = True)	

# FUN : Pins a message
def pinMsg(bot, msg):
	bot.pinChatMessage(
		chat_id = msg.chat_id,
		message_id = msg.message_id,
		disable_notification = True
	)

# FUN : Returns true if in a group chat	
def inGroup(msg):
	return msg.chat.get_members_count() > 2

# FUN : Returns an identifiable name for chats
#       Groups use title as name
#       Private chats use their name	
def getChatName(msg):
	if inGroup(msg):
		return msg.chat.title
	else:
		return msg.chat.username

# FUN : Deletes message specified as msg		
def delete(bot, msg):
	if inGroup(msg):
		logger.info('{} from {} triggered {}'.format(msg.from_user.first_name, getChatName(msg), 'delete'))
		del_msg_id = msg.message_id
		del_chat_id = msg.chat_id
		bot.deleteMessage(
			chat_id = del_chat_id, 
			message_id = del_msg_id
		)
	else:
		logger.info('Could not {} in private chat {}'.format('delete', getChatName(msg)))
	
# LOG : Logs error
def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)