from TcCore import *
import pyDes, codecs


#https://stackoverflow.com/questions/3815656 DES
#https://stackoverflow.com/questions/339007 PADDING

#minimum = float("inf")
#myArr = [16, 24]
def toKey (string):
    b = string
    a = 0
    print(f'initial {string.encode()}')
    if len(b.encode()) < 16:
        while len (b.encode()) < 16:
            print(f'less than 16 initial: {b.encode()}')
            b += b [a]
            a += 1
        while len(b.encode()) > 16:
            b = b [:-1]
        
        while len(b.encode()) < 16:
            b = (b.encode()+'x'.encode()).decode()
        print(len(b.encode()))
    elif len(b.encode()) > 24:
        while len(b.encode()) > 24:
            print(f'more than 24 initial: {b.encode()}')
            b = b [:-1]
    print(f'absolute: {b}')
    return b.encode()

class TcEncryptor():
    def encrypt(original_key, text):
        logger.info('TcEncryptor: Encrypting message...')
        key = toKey(original_key)
        data = pyDes.triple_des(key, pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
        encrypted = str(data.encrypt(text.encode()))[2:-1]
        key = key.decode()
        logger.info('TcEncryptor: Message encrypted!')
        decrypted = TcEncryptor.decrypt(key, encrypted)
        logger.info('TcEncryptor: Comparing decrypted message to the original...')
        if decrypted == str(text):
            success = True
        else:
            success = decrypted
        return [key, encrypted, success]

    def decrypt(original_key, original_text):
        logger.debug('TcEncryptor: Decrypting message...')
        key = toKey(original_key)
        text = bytes(map(ord, original_text)).decode('unicode-escape').encode('ISO-8859-1')
        if len(text) % 8 != 0:
            return 'not_multiple'
        data = pyDes.triple_des(key, pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
        decrypted = str(data.decrypt(text).decode())
        if decrypted == '':
            return 'not_valid'
        logger.info('TcEncryptor: Message decrypted!')
        return decrypted









class TcEncryptor_old():
    def encrypt(key, string):
        logger.info('TcEncryptor: Encrypting message...')
        #string = re.sub('[^a-zA-Z0-9 \n\.]', '', message)
        #string = string.replace('  ', ' ')
        #string = string.replace('  ', ' ')
        encoded_chars = []
        for i in range(len(string)):
            key_c = key[i % len(key)]
            encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
            encoded_chars.append(encoded_c)
        encoded_string = ''.join(encoded_chars)
        logger.info('TcEncryptor: Message encrypted!')
        return encoded_string

    def decrypt(key, string):
        logger.debug('TcEncryptor: Decrypting message...')
        encoded_chars = []
        for i in range(len(string)):
            key_c = key[i % len(key)]
            encoded_c = chr((ord(string[i]) - ord(key_c) + 256) % 256)
            encoded_chars.append(encoded_c)
        encoded_string = ''.join(encoded_chars)
        logger.info('TcEncryptor: Message decrypted!')
        return encoded_string


logger.info('Loaded: TcEncryptor')