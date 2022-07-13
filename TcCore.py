import requests, json, time, os
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, MessageQueue
import telegram
ver='0.3.7.2.6'
botName = 'Tcryptor'
botVer=f'{botName} {ver}'
botAt = '@TcryptorBot'
botUsername='TcryptorBot'
userdataDIR='data/userdata.json'


# Initialise the logger and format it's output
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
)
logger = logging.getLogger(__name__)


#  Load private information regarding the telegram bot
with open('data/token.json', 'r') as f:
    all_tokens = json.load(f)
    telegramConfig = all_tokens["telegram"]
    token = telegramConfig["token"]
    devid = telegramConfig["devid"]
    devusername = telegramConfig["devusername"]


with open('data/userdata.json') as f:
    userdata = json.load(f)


#  Initialise the required telegram bot data
u=Updater(token=token, use_context=True, request_kwargs={'read_timeout': 20, 'connect_timeout': 30})
dp = u.dispatcher



# Log the users previous message (debugging)
def logusr(update):
    logger.info(f'[@{update.effective_user.username}][{update.effective_user.first_name} {update.effective_user.last_name}][U:{update.effective_user.id}][M:{update.effective_message.message_id}]: {update.message.text}')


# Send a message to the user
def botsend(update, context, msg):
    update.message.reply_text(
        f'{str(msg)}\n\n<i>{botAt} <code>{ver}</code></i>',
        parse_mode=telegram.ParseMode.HTML,
    )


# Send a message to the user and log the message sent
def logbotsend(update, context, msg):
    update.message.reply_text(
        f'{str(msg)}\n\n<i>{botAt} <code>{ver}</code></i>',
        parse_mode=telegram.ParseMode.HTML,
    )

    logger.info(f'[@{botUsername}][{botName}][M:{update.effective_message.message_id}]: {msg}')


# Log a message the bot has sent anonymously
def logbot(update, msg):
    logger.info(f'[@{botUsername}][{botName}][M:{update.effective_message.message_id}]: {msg}')


# Update the users userdata automatically
def updateUserData(update):
    userID=str(update.effective_user.id)
    if userID not in userdata:
        addUserData(update, 0, 0, 0)
    else:
        addUserData(update, getUserData(update)["encrypts"], getUserData(update)["decrypts"], round(time.time()))


# Update the users userdata automatically but don't alter the "last_call"
def updateUserDataNoTime(update):
    userID=str(update.effective_user.id)
    if userID not in userdata:
        addUserData(update, 0, 0, 0)
    else:
        addUserData(update, getUserData(update)["encrypts"], getUserData(update)["decrypts"], getUserData(update)["last_call"])


# Add/update/overwrite the users userdata
def addUserData(update, encrypts, decrypts, lastCall):
    userdata[f'{update.effective_user.id}'] = {'username': f'{update.effective_chat.username}', 'name': f'{update.effective_user.first_name} {update.effective_user.last_name}', 'encrypts': encrypts, 'decrypts': decrypts, 'last_call': round(lastCall)}
    #logger.info(f'User data added/updated: [{update.effective_user.id}: {update.effective_user.username}, {update.effective_user.first_name} {update.effective_user.last_name}, {encrypts}, {decrypts}, {lastCall}]')
    saveUserData()


# Get the users userdata
def getUserData(update):
    #update = json.loads(update)
    logger.debug('getUserData(0/1)')
    data = userdata[f'{update.effective_user.id}']
    logger.debug('getUserData(1/1)')
    return data


# Save the 'userdata' variable content to data/userdata.json
def saveUserData():
    with open('data/userdata.json', 'w') as f:
        json.dump(userdata, f)
    #logger.info('User data has been saved')







logger.info('Loaded: TcCore')