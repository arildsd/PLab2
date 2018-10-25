import Cipher as ci

class Person(object):
    def __int__(self):
        self.key = None
        self.cipher = None

    def set_key(self, key):
        self.key = key

    def get_key(self):
        return self.key

    def set_cipher(self, cipher):
        self.cipher = cipher

    def get_cipher(self):
        return self.cipher

    def operate_cipher(self, message):
        if (self.cipher == None):
            raise Exception("Cipher is not set.")
        if (self.key == None):
            raise Exception("Key is not set.")

class Receiver(Person):
    def __init__(self):
        super().__init__()
        self.public_key = None

    #Decodes the given message with the current cipher and key
    #Cipher and key must be set before calling this function
    def operate_cipher(self, message):
        super().operate_cipher(message)
        self.cipher.set_key(self.key)
        decoded_message = self.cipher.decode(message)
        return decoded_message

    def get_public_key(self):
        return self.key[0]

class Sender(Person):
    #If this class uses the RSA cipher self.key
    #is the public key of the reciver
    def __init__(self):
        super().__init__()

    #Encodes the given message with the current cipher and key
    #Cipher and key must be set before calling this function
    def operate_cipher(self, message):
        super().operate_cipher(message)
        self.cipher.set_key(self.key)
        if(isinstance(self.cipher, ci.RSA)):
            encoded_message = self.cipher.encode(message, self.key)
        else:
            self.cipher.set_key(self.key)
            encoded_message = self.cipher.encode(message)
        return encoded_message
