import Cipher as Cipher
import math

class Hacker(object):
    def __init__(self):
        self.bestMatch = -1
        self.bestMatchKey = None
        self.bestDecode = ""
        self.words = []
        file = open(r".\words", "r")
        for line in file:
            self.words.append(line[:len(line)-1])
        file.close()

    def hack(self, encodedMessage):
        pass

class HackCaesar(Hacker):
    def __init__(self):
        super().__init__()
        self.cipher = Cipher.Caesar()

    def hack(self, encodedMessage):
        self.bestMatch = -1
        self.bestMatchKey = None
        self.bestDecode = ""
        for key in range(0, 95):
            self.cipher.set_key(key)
            decode = self.cipher.decode(encodedMessage)
            strings = decode.split(" ")
            counter = 0
            for word in strings:
                if(word.lower() in self.words):
                    counter +=1
            if(counter > self.bestMatch):
                self.bestMatch = counter
                self.bestMatchKey = key
                self.bestDecode = decode
        return (self.bestMatchKey, self.bestMatch, self.bestDecode)

class HackMultiplicative(Hacker):
    def __init__(self):
        super().__init__()
        self.cipher = Cipher.Multiplication()

    def hack(self, encodedMessage):
        self.bestMatch = -1
        self.bestMatchKey = None
        self.bestDecode = ""
        for key in range(0, 97):
            if (math.gcd(key, 95) != 1):
                continue
            self.cipher.set_key(key)
            decode = self.cipher.decode(encodedMessage)
            strings = decode.split(" ")
            counter = 0
            for word in strings:
                if(word.lower() in self.words):
                    counter +=1
            if(counter > self.bestMatch):
                self.bestMatch = counter
                self.bestMatchKey = key
                self.bestDecode = decode
        return (self.bestMatchKey, self.bestMatch, self.bestDecode)

class HackAffine(Hacker):
    def __init__(self):
        super().__init__()
        self.cipher = Cipher.Affine()

    def hack(self, encodedMessage):
        self.bestMatch = -1
        self.bestMatchKey = None
        self.bestDecode = ""
        for mult in range(0, 97):
            if (math.gcd(mult, 95) != 1):
                continue
            for add in range(0, 95):
                self.cipher.set_key((mult, add))
                decode = self.cipher.decode(encodedMessage)
                strings = decode.split(" ")
                counter = 0
                for word in strings:
                    if(word.lower() in self.words):
                        counter +=1
                if(counter > self.bestMatch):
                    self.bestMatch = counter
                    self.bestMatchKey = "(%d, %d)" % (mult, add)
                    self.bestDecode = decode
        return (self.bestMatchKey, self.bestMatch, self.bestDecode)

class HackUnbreakable(Hacker):
    def __init__(self):
        super().__init__()
        self.cipher = Cipher.Unbreakable()
        self.counterList = [None]*95
        self.alp = r""" !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"""

    def _increment(self):
        #Traverse the list backwards
        for i in range(len(self.counterList)-1, -1, -1):
            if(self.counterList[i] == 94):
                self.counterList[i] = 0
            elif(self.counterList[i] == None):
                self.counterList[i] = 0
                break
            else:
                self.counterList[i] += 1
                break

    def _list_to_string(self):
        result = ""
        for num in self.counterList:
            if(num == None):
                continue
            else:
                result += self.alp[num]
        return result


    def hack(self, message):
        self.bestMatch = -1
        self.bestMatchKey = None
        self.bestDecode = ""
        ratio = 0
        while(ratio < 0.6):
            self._increment()
            key = self._list_to_string()
            self.cipher.set_key(key)
            decode = self.cipher.decode(message)
            strings = decode.split(" ")
            counter = 0
            for word in strings:
                if (word in self.words and word != ""):
                    counter += 1
            if (counter > self.bestMatch):
                self.bestMatch = counter
                self.bestMatchKey = key
                self.bestDecode = decode
                ratio = counter/len(strings)
        return (self.bestMatchKey, self.bestMatch, self.bestDecode)
