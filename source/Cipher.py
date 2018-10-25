import crypto_utils as cry
import random
import math

class Cipher(object):
    def __init__(self):
        self.alphabetDict = {" ": 0, "!": 1, "\"": 2, "#": 3, "$": 4, "%": 5, "&": 6, r"'": 7, "(": 8, ")": 9, "*": 10,
                             "+": 11, ",": 12, "-": 13, ".": 14, "/": 15, "0": 16, "1": 17, "2": 18, "3": 19, "4": 20,
                             "5": 21, "6": 22, "7": 23, "8": 24, "9": 25, ":": 26, ";": 27, "<": 28, "=": 29, ">": 30,
                             "?": 31, "@": 32, "A": 33, "B": 34, "C": 35, "D": 36, "E": 37, "F": 38, "G": 39, "H": 40,
                             "I": 41, "J": 42, "K": 43, "L": 44, "M": 45, "N": 46, "O": 47, "P": 48, "Q": 49, "R": 50,
                             "S": 51, "T": 52, "U": 53, "V": 54, "W": 55, "X": 56, "Y": 57, "Z": 58, "[": 59, "ø" : 60,
                             "]": 61, "^": 62, "_": 63, "`": 64, "a": 65, "b": 66, "c": 67, "d": 68, "e": 69, "f": 70,
                             "g": 71, "h": 72, "i": 73, "j": 74, "k": 75, "l": 76, "m": 77, "n": 78, "o": 79, "p": 80,
                             "q": 81, "r": 82, "s": 83, "t": 84, "u": 85, "v": 86, "w": 87, "x": 88, "y": 89, "z": 90,
                             "{": 91, "|": 92, "}": 93, "~": 94}
        alphabet_chars = [str(key) for key in self.alphabetDict.keys()]
        self.alphabet = "".join(alphabet_chars)
        self.alphabetLength = len(self.alphabet)
        self.key = None

    def encode(self, string):
        if(self.key == None):
            raise Exception("No key is set.")

    def decode(self, string):
        if (self.key == None):
            raise Exception("No key is set.")

    def verify(self, string):
        return string == self.decode(self.encode(string))

    def generate_keys(self):
        pass

    def set_key(self, key):
        self.key = key

    def get_key(self):
        return self.key

    def get_keyformat(self):
        pass

    def isValidKey(self, key):
        pass

    def string_to_key(self, key):
        if(not self.isValidKey(key)):
            raise Exception("The key is not valid.")

    def get_key_as_string(self):
        if(self.key == None):
            raise Exception("The key was None.")

class Caesar(Cipher):
    def __init__(self):
        super().__init__()

    def encode(self, string):
        super().encode(string)
        result = ""
        for letter in string:
            result += self.alphabet[(self.alphabetDict[letter] + self.key) % self.alphabetLength]
        return result

    def decode(self, string):
        super().decode(string)
        result = ""
        for letter in string:
            result += self.alphabet[(self.alphabetDict[letter]-self.key) % self.alphabetLength]
        return result

    def generate_keys(self):
        return random.randint(1, self.alphabetLength-1)

    def get_keyformat(self):
        return "Integer"

    def isValidKey(self, key):
        try:
            key = int(key)
        #The key string could not convert to an int
        except:
            return False
        return True

    def string_to_key(self, key):
        super().string_to_key(key)
        return int(key)

class Multiplication(Cipher):
    def __init__(self):
        super().__init__()

    def encode(self, string):
        super().encode(string)
        result = ""
        for letter in string:
            result += self.alphabet[(self.alphabetDict[letter] * self.key) % self.alphabetLength]
        return result

    def decode(self, string):
        super().decode(string)
        decode_key = cry.modular_inverse(self.key, self.alphabetLength)
        result = ""
        for letter in string:
            result += self.alphabet[(self.alphabetDict[letter] * decode_key) % self.alphabetLength]
        return result

    def generate_keys(self):
        for i in range(random.randint(2, 95), 96):
            #The key is not a valid option
            if(math.gcd(i, self.alphabetLength) != 1):
                continue
            #The key is correct and is returned
            else:
                return i

    def get_keyformat(self):
        return "Integer"

    def isValidKey(self, key):
        try:
            key = int(key)
        #The key string could not convert to an int
        except:
            return False
        return (math.gcd(key, self.alphabetLength) == 1)

    def string_to_key(self, key):
        super().string_to_key(key)
        return int(key)

class Affine(Cipher):
    #The key is in the format (* , +)
    def __init__(self):
        super().__init__()

    def encode(self, string):
        super().encode(string)
        temp_result = ""
        result = ""
        for letter in string:
            temp_result += self.alphabet[(self.alphabetDict[letter] * self.key[0]) % self.alphabetLength]
        for letter in temp_result:
            result += self.alphabet[(self.alphabetDict[letter] + self.key[1]) % self.alphabetLength]
        return result

    def decode(self, string):
        super().encode(string)
        temp_result =""
        result = ""
        #Caesar decode
        for letter in string:
            temp_result += self.alphabet[(self.alphabetDict[letter]-self.key[1]) % self.alphabetLength]
        #Multipication decode
        decode_key = cry.modular_inverse(self.key[0], self.alphabetLength)
        for letter in temp_result:
            result += self.alphabet[(self.alphabetDict[letter] * decode_key) % self.alphabetLength]
        return result

    def generate_keys(self):
        for i in range(random.randint(2, 95), 97):
            #The key is correct and is returned
            if(math.gcd(i, self.alphabetLength) == 1):
                return (i, random.randint(1, self.alphabetLength - 1))

    def get_keyformat(self):
        return "Integer;Integer"

    def isValidKey(self, key):
        strings = key.split(";")
        if(len(strings) != 2):
            return False
        try:
            strings[0] = int(strings[0])
            strings[1] = int(strings[1])
        except:
            return False
        return (math.gcd(strings[0], self.alphabetLength) == 1)

    def string_to_key(self, key):
        super().string_to_key(key)
        strings = key.split(";")
        return (int(strings[0]), int(strings[1]))

class Unbreakable(Cipher):
    def __init__(self):
        super().__init__()
        self.counter = 0

    def increment(self):
        self.counter = (self.counter+1)%len(self.key)

    def encode(self, string):
        super().encode(string)
        self.counter = 0
        result = ""
        for letter in string:
            result += self.alphabet[(self.alphabetDict[self.key[self.counter]]+self.alphabetDict[letter]) % self.alphabetLength]
            self.increment()
        return result

    def decode(self, string):
        super().decode(string)
        self.counter = 0
        result = ""
        for letter in string:
            result += self.alphabet[(self.alphabetDict[letter] - self.alphabetDict[self.key[self.counter]]) % self.alphabetLength]
            self.increment()
        return result

    def generate_keys(self):
        result = ""
        for i in range(0, 12):
            result += self.alphabet[random.randint(0, self.alphabetLength-1)]
        print(result)
        return result

    def get_keyformat(self):
        return "String"

    def isValidKey(self, key):
        if(key == ""):
            return False
        for c in key:
            if c not in self.alphabet:
                return False
        return True

    def string_to_key(self, key):
        super().string_to_key(key)
        return key

class RSA(Cipher):
    #self.key is the tuple ((n,e), (n, d)) where (n, e) is the public key
    #And (n, d) is the private key
    #The public key must be provided in encode
    def __init__(self):
        super().__init__()
        self.bit_size = 24

    def get_public_key(self):
        return self.key[0]

    def get_private_key(self):
        return self.key[1]

    def encode(self, string, key):
        result = []
        message = cry.blocks_from_text(string, self.bit_size//4)
        for t in message:
            result.append(pow(t, key[1], key[0]))
        return result

    def decode(self, message):
        temp_result = []
        for c in message:
            temp_result.append(pow(c, self.key[1][1], self.key[1][0]))
        return cry.text_from_blocks(temp_result, self.bit_size//4)

    def generate_keys(self):
        p = cry.generate_random_prime(self.bit_size)
        q = cry.generate_random_prime(self.bit_size)
        n = p*q
        phi = (p-1)*(q-1)
        e = random.randint(3, phi-1)
        while(math.gcd(e, phi) != 1):
            e = random.randint(3, phi - 1)
        d = cry.modular_inverse(e, phi)
        # (n, e) is the public key and (n, d) is the private key
        return ((n,e), (n, d))

    #Key is the public key to encode
    def verify(self, string, key):
        return string == self.decode(self.encode(string, key))

    def get_keyformat(self):
        raise Exception("Operation not supported for RSA.")

    def isValidKey(self, key):
        raise Exception("Operation not supported for RSA.")

    def string_to_key(self, key):
        raise Exception("Operation not supported for RSA.")