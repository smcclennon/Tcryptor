from TcCore import *


class TcProcessor():


    def commandArgs(update, context):
        whitespace=[]
        keysplit=1
        msgsplit=2
        command = update.message.text
        split = command.split(' ')  # Split the message with each space
        if len(split) < 3:
            return None
        if len(split) >= 3:
            key = split[1]
            while key == "":  # If the user used irregular spacing
                keysplit+=1
                whitespace.append(keysplit-1)
                key = split[keysplit]

            message = command
            for space in whitespace:
                message = message.replace(split[space], '', 1)
            message = message.replace(split[0]+' ', '', 1)
            message = message.replace(split[keysplit]+' ', '', 1)

            if len(message) > 5000:
                return ['too_long', len(message)-5000]
            return [key, message]


    def waitmsg(update, context):
            timeLeft_int = TcProcessor.timeLeft(update)
            if timeLeft_int == 1:
                time_msg = f'{timeLeft_int} second'
            else:
                time_msg = f'{timeLeft_int} seconds'
            logbotsend(update, context, f'Please wait {time_msg} before making another request')


    def authorised(update):
        logger.debug('authorised(0/2)')
        if TcProcessor.timeLeft(update) <= 0:
            #api_calls = getUserData(f'{update.effective_chat.id}')['api_calls']
            logger.debug('authorised(1/2)')
            #updateUserData(update)
            logger.debug('authorised(2/2)')
            return True
        else:
            logger.debug('authorised(2/2)')
            return False


    def timeLeft(update):
        logger.debug('timeLeft(0/3)')
        last_call = getUserData(update)['last_call']
        logger.debug('timeLeft(1/2)')
        dur_since_last_call = round(time.time()) - int(last_call)
        logger.debug('timeLeft(2/2)')
        return int(5 - round(dur_since_last_call))

    def find_key(d, value):  # https://stackoverflow.com/a/15210253
        for k,v in d.items():
            if isinstance(v, dict):
                p = TcProcessor.find_key(v, value)
                if p:
                    return [k] + p
            elif v == value:
                return [k]





logger.info('Loaded: TcProcessor')