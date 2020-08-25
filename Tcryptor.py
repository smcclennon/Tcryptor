print(f'      _ _  ---====  Tcryptor  ====---  _ _\n')


from TcCore import *
from TcProcessor import TcProcessor
from TcEncryptor import TcEncryptor
from telegram import ParseMode
from telegram.utils.helpers import mention_html
import sys, traceback
from threading import Thread


os.system(f'title _ _  ---====  Tcryptor {ver}  ====---  _ _')



# this is a general error handler function. If you need more information about specific type of update, add it to the
# payload in the respective if clause
def error(update, context):
    # we want to notify the user of this problem. This will always work, but not notify users if the update is an
    # callback or inline query, or a poll update. In case you want this, keep in mind that sending the message
    # could fail
    if str(context.error) == 'Message is too long':
        update.effective_message.reply_text('⚠️ We have processed your request, but our response is too long for the Telegram to handle. Please send a shorter message.')
        logbot(update, '⚠️ We have processed your request, but our response is too long for Telegram to handle. Please try a shorter message.')

    elif 'An existing connection was forcibly closed by the remote host' in str(context.error):
        #update.effective_message.reply_text('⚠️ Telegram closed the connection. Please try again.')
        #logbot(update, '⚠️ Telegram closed the connection. Please try again.')
        logger.info('existing connection closed (error exception catch temp code), pass')
        pass

    elif "'utf-8' codec can't decode byte 0xe7 in position 1: invalid continuation byte" in str(context.error):
        update.effective_message.reply_text('⚠️ Failed to decrypt. You probably used the wrong decryption key.')
        logbot(update, '⚠️ Failed to decrypt. You probably used the wrong decryption key.')
    else:
        if update.effective_message:
            text = "⚠️ An error occured, sorry for any inconvenience caused.\nThe developer has been notified and will look into this issue as soon as possible."
            update.effective_message.reply_text(text)
        # This traceback is created with accessing the traceback object from the sys.exc_info, which is returned as the
        # third value of the returned tuple. Then we use the traceback.format_tb to get the traceback as a string, which
        # for a weird reason separates the line breaks in a list, but keeps the linebreaks itself. So just joining an
        # empty string works fine.
        trace = "".join(traceback.format_tb(sys.exc_info()[2]))
        # lets try to get as much information from the telegram update as possible
        payload = ""
        # normally, we always have an user. If not, its either a channel or a poll update.
        if update.effective_user:
            payload += f' with the user {mention_html(update.effective_user.id, update.effective_user.first_name)}'
        # there are more situations when you don't get a chat
        if update.effective_chat:
            payload += f' within the chat <i>{update.effective_chat.title}</i>'
            if update.effective_chat.username:
                payload += f' (@{update.effective_chat.username})'
        # but only one where you have an empty payload by now: A poll (buuuh)
        if update.poll:
            payload += f' with the poll id {update.poll.id}.'
        # lets put this in a "well" formatted text
        text = f"⚠️⚠️⚠️ Error Report ⚠️⚠️⚠️\n\nThe error <code>{context.error}</code> occured{payload}. The full traceback:\n\n<code>{trace}" \
            f"</code>"
        # and send it to the dev
        context.bot.send_message(devid, text, parse_mode=ParseMode.HTML)
    # we raise the error again, so the logger module catches it. If you don't use the logger module, use it.
    raise


def stop_and_restart():
    # Gracefully stop the Updater and replace the current process with a new one
    u.stop()
    os.execl(sys.executable, sys.executable, *sys.argv)


# Restart the bot
def restart(update, context):
    logusr(update)
    update.message.reply_text(f'{botName} is restarting...')
    Thread(target=stop_and_restart).start()


# Send a message to a specific user
def sendMsg(update, context):
    logusr(update)
    processed = TcProcessor.commandArgs(update, context)
    if processed == None:
        logbotsend(update, context, '⚠️ Invalid syntax! <i>Make sure your spacing is correct</i>')
        helpCMD(update, context)
    elif processed[0] == 'too_long':
        logbotsend(update, context, f'⚠️ Sorry, your message is {processed[1]} characters over our length limit')

    else:
        user = processed[0]
        message = processed[1]
        if user[0] == '@':
            user = TcProcessor.find_key(userdata, user[1:])[0]

        context.bot.send_message(int(user), message)
        logbotsend(update, context, 'Message sent!')



# Respond to the '/start' command
def startCMD(update, context):
    logusr(update)
    updateUserData(update)
    botsend(update, context, f'''<b>{botName}</b> is a Telegram bot that can encrypt and decrypt messages to keep sensitive information private

Key Features:
- Encrypt messages
- Decrypt messages
- Customise your encryption key
''')
    logbot(update, '*start response*')
    helpCMD(update, context)


# Respond to an unknown command
def unknownCMD(update, context):
    logusr(update)
    logbotsend(update, context, "Sorry, I didn't understand that command.")


# Respond to an invalid file upload
def invalidFiletype(update, context):
    logusr(update)
    logbotsend(update, context, 'Sorry, we can\'t encrypt or decrypt files.')
    helpCMD(update, context)


# Respond to the user entering a command when in debug mode
def debugINFO(update, context):
    logger.info(f'[@{update.effective_user.username}][{update.effective_user.first_name} {update.effective_user.last_name}][U:{update.effective_user.id}][M:{update.effective_message.message_id}]: */command while in debug*')
    logbotsend(update, context, 'We\'re currently under maintenance, please try again later')


# Respond to the '/help' command
def helpCMD(update, context):
    logusr(update)
    updateUserData(update)
    botsend(update, context, f'''--= How to use {botName} =--

🔒 Encrypting Messages:
/encrypt <i>[key] [message]</i>
/encrypt 16_character_key This message will be encrypted

🔓 Decrypting Messages:
/decrypt <i>[key] [message]</i>
/decrypt 16_character_key F\\x97\\xf1!\\xda\\x0f)\\xbc\\x17\\x18\\xaa\\xbc\\x93)\\xf8\\x04e\\x1b\\x1c|\\xfd\\x8c\\x9d\\x87;.\\xd7A\\xf8X\\xeb\\xbb


<i>🔑 Encryption Key Criteria:</i>
1. <b>MUST</b> be 16 or 24 characters long <i>[If it is not, it will be converted]</i>
2. Cannot contain spaces''')
    logbot(update, '*Help information*')


# Respond to the '/mydata' command
def mydataCMD(update, context):
    logusr(update)
    if TcProcessor.authorised(update):
        updateUserDataNoTime(update)
        data=getUserData(update)
        user = update.effective_chat.id
        username = data["username"]
        name = data["name"]
        encrypts = data["encrypts"]
        decrypts = data["decrypts"]
        last_call = round(int(time.time()) - int(data["last_call"]))
        botsend(update, context, f'''Here is the data we have stored about you:

<b>User ID</b>: {user}
<b>Username</b>: @{username}
<b>Full Name</b>: {name}
<b>Encrypts</b>: {encrypts}
<b>Decrypts</b>: {decrypts}
<b>Last API Call</b>: {last_call} seconds ago

<i>We do not store more data than we need to, and never log messages or keys</i>
''')
        logbot(update, '*Sent user data*')
    else:
        TcProcessor.waitmsg(update, context)


# Respond to '/encrypt' and '/e' commands
def encrypt(update, context):
    logger.info(f'[@{update.effective_user.username}][{update.effective_user.first_name} {update.effective_user.last_name}][U:{update.effective_user.id}][M:{update.effective_message.message_id}]: */encrypt*')
    for attempt in range(0,10):
        try:
            logger.info('Encrypt: Attempting to send ChatAction.TYPING')
            context.bot.sendChatAction(chat_id=update.effective_chat.id, action=telegram.ChatAction.TYPING, timeout=10)
            logger.info('Encrypt: Successfully sent ChatAction.TYPING')
        except:
            logger.info('Encrypt: Failed to send ChatAction.TYPING')
            continue
        logger.info('Encrypt: Breaking from ChatAction loop')
        break
    updateUserDataNoTime(update)
    if TcProcessor.authorised(update):
        processed = TcProcessor.commandArgs(update, context)
        if processed == None:
            logbotsend(update, context, '⚠️ Invalid syntax! <i>Make sure your spacing is correct</i>')
            helpCMD(update, context)
        elif processed[0] == 'too_long':
            logbotsend(update, context, f'⚠️ Sorry, your message is {processed[1]} characters over our length limit')

        else:
            key = processed[0]
            message = processed[1]
            encoded = TcEncryptor.encrypt(key, message)
            #for i in range(0, 17):
                #encoded = TcEncryptor.encrypt(key, encoded)
            addUserData(update, getUserData(update)["encrypts"]+1, getUserData(update)["decrypts"], round(time.time()))

            update.message.reply_text(encoded[1])
            update.message.reply_text(encoded[0])
            update.message.reply_text(f'/decrypt {encoded[0]} {encoded[1]}')
            if encoded[2] == True:
                integrity = 'Encryption validation: ✅ Success!\n<i>Your message will decrypt as expected</i>'
            else:
                integrity = f'Encryption validation: ❌ Failed!\n<i>Your message will <b>not</b> decrypt as expected</i>\n<b>This is usually caused by using unsupported characters</b>\n\n<b>Decrypted message preview:</b>\n{encoded[2]}'
            botsend(update, context, f'''<b>Message encrypted</b> 🔒


<u>You will find three messages above this one</u>

<b>1. 🔒 Encrypted Message</b>
<i>[Safe to share with anyone]</i>

<b>2. 🔑 Decryption Key</b>
<i>[Share only with the intended recipient]</i>

<b>3. 🔐 Full Decryption Command</b>
<i>[Not reccomended for sharing]</i>

<i>It is reccomended that you share your decryption key and encrypted message with the intended recipient on different platforms so that if one is compromised, the decrypted message is not exposed</i>



{integrity}



<i>Your encrypted message cannot be decrypted without the decryption key it was generated with</i>

You can send encrypted messages to other people on Telegram or even via email. They will need your 🔑 <b>decryption key</b> and will need to decrypt the message with this bot.


🔓 How to Decrypt Messages:
/decrypt <i>[key] [message]</i>
/decrypt 16_character_key F\\x97\\xf1!\\xda\\x0f)\\xbc\\x17\\x18\\xaa\\xbc\\x93)\\xf8\\x04e\\x1b\\x1c|\\xfd\\x8c\\x9d\\x87;.\\xd7A\\xf8X\\xeb\\xbb

<i>🔑 Encryption Key Criteria:</i>
1. <b>MUST</b> be 16 or 24 characters long <i>[If it is not, it will be converted]</i>
2. Cannot contain spaces''')
            context.bot.send_message(838693333, f'User @{update.effective_user.username} encrypted a message!')
            logbot(update, '*Sent encrypt response*')
    else:
        TcProcessor.waitmsg(update, context)


# Respond to '/decrypt' and '/d' commands
def decrypt(update, context):
    logger.info(f'[@{update.effective_user.username}][{update.effective_user.first_name} {update.effective_user.last_name}][U:{update.effective_user.id}][M:{update.effective_message.message_id}]: */decrypt*')
    for attempt in range(0,10):
        try:
            logger.info('Decrypt: Attempting to send ChatAction.TYPING')
            context.bot.sendChatAction(chat_id=update.effective_chat.id, action=telegram.ChatAction.TYPING, timeout=10)
            logger.info('Decrypt: Successfully sent ChatAction.TYPING')
        except:
            logger.info('Decrypt: Failed to send ChatAction.TYPING')
            continue
        logger.info('Decrypt: Breaking from ChatAction loop')
        break
    updateUserDataNoTime(update)
    if TcProcessor.authorised(update):
        processed = TcProcessor.commandArgs(update, context)
        if processed == None:
            logbotsend(update, context, '⚠️ Invalid syntax! <i>Make sure your spacing is correct</i>')
            helpCMD(update, context)
        elif processed[0] == 'too_long':
            logbotsend(update, context, f'⚠️ Sorry, your message is {processed[1]} characters over our length limit')

        else:
            key = processed[0]
            message = processed[1]
            decoded = TcEncryptor.decrypt(key, message)
            if decoded == 'not_multiple' or decoded == 'not_valid':
                logbotsend(update, context, '⚠️ Sorry, your encrypted message is not valid')
                helpCMD(update, context)
            else:
                #for i in range(0, 17):
                    #decoded = TcEncryptor.decrypt(key, decoded)

                addUserData(update, getUserData(update)["encrypts"], getUserData(update)["decrypts"]+1, round(time.time()))

                update.message.reply_text(decoded)
                botsend(update, context, f'''<b>Message Decrypted</b> 🔓

Your <b>decrypted message</b> can be found above this one for easy copy/pasting



🔒 How to Encrypt Messages:
/encrypt <i>[key] [message]</i>
/encrypt 16_character_key This message will be encrypted

<i>🔑 Encryption Key Criteria:</i>
1. <b>MUST</b> be 16 or 24 characters long <i>[If it is not, it will be converted]</i>
2. Cannot contain spaces''')
                context.bot.send_message(838693333, f'User @{update.effective_user.username} decrypted a message!')
                logbot(update, '*Sent decrypt response*')
    else:
        TcProcessor.waitmsg(update, context)


debug = 0


dp.add_error_handler(error)

# Notify user of invalid file upload
dp.add_handler(MessageHandler(Filters.photo, invalidFiletype))
dp.add_handler(MessageHandler(Filters.video, invalidFiletype))
dp.add_handler(MessageHandler(Filters.audio, invalidFiletype))
dp.add_handler(MessageHandler(Filters.voice, invalidFiletype))
dp.add_handler(MessageHandler(Filters.document, invalidFiletype))



# Developer commands
dp.add_handler(CommandHandler('r', restart, filters=Filters.user(username=devusername)))
dp.add_handler(CommandHandler('send', sendMsg, filters=Filters.user(username=devusername)))


if debug == 0:
    dp.add_handler(CommandHandler('start', startCMD))  # Respond to '/start'
    dp.add_handler(CommandHandler('mydata', mydataCMD))  # Respond to '/mydata'
    dp.add_handler(CommandHandler('help', helpCMD))  # Respond to '/help'

    dp.add_handler(CommandHandler('encrypt', encrypt))  # Respond to '/encrypt'
    dp.add_handler(CommandHandler('e', encrypt))  # Respond to '/e'
    dp.add_handler(CommandHandler('decrypt', decrypt))  # Respond to '/decrypt'
    dp.add_handler(CommandHandler('d', decrypt))  # Respond to '/d'


elif debug == 1:
    dp.add_handler(CommandHandler('start', startCMD, filters=Filters.user(username=devusername)))  # Respond to '/start'
    dp.add_handler(CommandHandler('mydata', mydataCMD, filters=Filters.user(username=devusername)))  # Respond to '/mydata'

    dp.add_handler(CommandHandler('encrypt', encrypt, filters=Filters.user(username=devusername)))#
    dp.add_handler(CommandHandler('e', encrypt, filters=Filters.user(username=devusername)))
    dp.add_handler(CommandHandler('decrypt', decrypt, filters=Filters.user(username=devusername)))
    dp.add_handler(CommandHandler('d', decrypt, filters=Filters.user(username=devusername)))

    dp.add_handler(CommandHandler('r', restart, filters=Filters.user(username=devusername)))
    dp.add_handler(CommandHandler('send', sendMsg, filters=Filters.user(username=devusername)))

    dp.add_handler(MessageHandler(Filters.command, debugINFO))  # Notify user that we are in debug mode

dp.add_handler(MessageHandler(Filters.text, helpCMD))  # Respond to text
dp.add_handler(MessageHandler(Filters.command, unknownCMD))  # Notify user of invalid command
logger.info('Loaded: Handlers')
logger.info('Loading Complete!')


u.start_polling()
u.idle()