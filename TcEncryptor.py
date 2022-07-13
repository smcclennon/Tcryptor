from TcCore import *
import pyDes, codecs


#https://stackoverflow.com/questions/3815656 DES
#https://stackoverflow.com/questions/339007 PADDING

#minimum = float("inf")
#myArr = [16, 24]
def toKey(string):
    b = string
    # debug print(f'initial {string.encode()}')
    if len(b.encode()) < 16:
        a = 0
        while len (b.encode()) < 16:
            # debug print(f'less than 16 initial: {b.encode()}')
            b += b [a]
            a += 1
        while len(b.encode()) > 16:
            b = b [:-1]

        while len(b.encode()) < 16:
            b = (b.encode()+'x'.encode()).decode()
            # debug print(len(b.encode()))
    elif len(b.encode()) > 24:
        while len(b.encode()) > 24:
            # debug print(f'more than 24 initial: {b.encode()}')
            b = b [:-1]
    # debug print(f'absolute: {b}')
    return b.encode()

class TcEncryptor():
    def encrypt(self, text):
        logger.info('TcEncryptor: Encrypting message...')
        key = toKey(self)
        data = pyDes.triple_des(key, pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
        encrypted = str(data.encrypt(text.encode()))[2:-1]
        key = key.decode()
        logger.info('TcEncryptor: Message encrypted!')
        decrypted = TcEncryptor.decrypt(key, encrypted)
        logger.info('TcEncryptor: Comparing decrypted message to the original...')
        success = True if decrypted == str(text) else decrypted
        return [key, encrypted, success]

    def decrypt(self, original_text):
        logger.debug('TcEncryptor: Decrypting message...')
        key = toKey(self)
        text = bytes(map(ord, original_text)).decode('unicode-escape').encode('ISO-8859-1')
        if len(text) % 8 != 0:
            return 'not_multiple'
        data = pyDes.triple_des(key, pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
        decrypted = str(data.decrypt(text).decode())
        if not decrypted:
            return 'not_valid'
        logger.info('TcEncryptor: Message decrypted!')
        return decrypted









class TcEncryptor_old():
    def encrypt(self, string):
        logger.info('TcEncryptor: Encrypting message...')
        #string = re.sub('[^a-zA-Z0-9 \n\.]', '', message)
        #string = string.replace('  ', ' ')
        #string = string.replace('  ', ' ')
        encoded_chars = []
        for i in range(len(string)):
            key_c = self[i % len(self)]
            encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
            encoded_chars.append(encoded_c)
        logger.info('TcEncryptor: Message encrypted!')
        return ''.join(encoded_chars)

    def decrypt(self, string):
        logger.debug('TcEncryptor: Decrypting message...')
        encoded_chars = []
        for i in range(len(string)):
            key_c = self[i % len(self)]
            encoded_c = chr((ord(string[i]) - ord(key_c) + 256) % 256)
            encoded_chars.append(encoded_c)
        logger.info('TcEncryptor: Message decrypted!')
        return ''.join(encoded_chars)


logger.info('Loaded: TcEncryptor')