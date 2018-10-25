import Cipher as Cipher
import Person as Pe
import Hacker as Ha

receiver = Pe.Receiver()
sender = Pe.Sender()
hacker = Ha.Hacker()
hackMessage = False

def select_hacker(num):
    if(num == 0):
        return Ha.HackCaesar()
    elif(num == 1):
        return Ha.HackMultiplicative()
    elif(num == 2):
        return Ha.HackAffine()
    elif(num == 3):
        return Ha.HackUnbreakable()
    else:
        raise Exception("No hacker for %d" % num)

def select_cipher(num):
    if(num == 0):
        return Cipher.Caesar()
    elif(num == 1):
        return Cipher.Multiplication()
    elif(num == 2):
        return Cipher.Affine()
    elif(num == 3):
        return Cipher.Unbreakable()
    elif(num == 4):
        return Cipher.RSA()
    else:
        raise Exception("Illegal argument, the argument must be an int between 0 and 4, but it was %d" % num)

def setup_persons(cipher, num):
    global receiver, sender, hacker, hackMessage
    receiver = Pe.Receiver()
    receiver.set_cipher(cipher)
    receiver.set_key(cipher.get_key())
    sender = Pe.Sender()
    sender.set_cipher(select_cipher(num))
    if(isinstance(cipher, Cipher.RSA)):
        sender.set_key(receiver.get_public_key())
    else:
        sender.set_key(receiver.get_key())
        if(hackMessage):
            hacker = select_hacker(num)

def send_single_message(message):
    global receiver, sender
    encode = sender.operate_cipher(message)

    print("Sender encoded the message to: %s" % encode)
    decode = receiver.operate_cipher(encode)
    print("Reciver decoded the message to: %s" % decode)
    if(hackMessage):
        result = hacker.hack(encode)
        print("The hacker found a best match of %d with key %s.\nThis gives the message: %s" % (result[1], str(result[0]), result[2]))

def main():
    alp = r""" !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"""
    option = None
    while (True):
        print("Select the cipher that will be used to encode/decode the message.")
        print("Caesar (0)", "Multiplicative(1)", "Affine(2)", "Unbreakable (3)", "RSA (4)", sep="\n")
        try:
            option = int(input())
            break
        except:
            print("Invalid input, please enter a number between 0 and 4.")
            continue
    rec_cipher = select_cipher(option)
    if(isinstance(rec_cipher, Cipher.RSA)):
        genRandom = True
    else:
        #Ask the user if he/she want to hack the message
        global hackMessage
        while(True):
            print("Do you want to hack the message? y/n")
            user_input = input()
            if(user_input == "y"):
                hackMessage = True
                break
            elif(user_input == "n"):
                hackMessage = False
                break
            else:
                print("Invalid input.")
        genRandom = None

    # Ask the user if they want to generate a random key or not
    # Not supported for RSA
    while (genRandom == None):
        print("Do you want to generate a random key? (recommended) y/n")
        user_input = input()
        if(user_input == "y"):
            genRandom = True
            break
        elif(user_input == "n"):
            genRandom = False
            break
        else:
            print("Invalid input, please enter y or n.")
            continue
    if(not genRandom):
        while(True):
            print("Enter a key in the format %s." % rec_cipher.get_keyformat())
            user_input = input()
            if(rec_cipher.isValidKey(user_input)):
                key = rec_cipher.string_to_key(user_input)
                rec_cipher.set_key(key)
                break
            else:
                print("Invalid input.")
                continue
    else:
        key = rec_cipher.generate_keys()
        rec_cipher.set_key(key)

    setup_persons(rec_cipher, option)

    #Loop for sending messages
    while(True):
        print("Please enter the message:")
        user_input = input()
        send_single_message(user_input)

main()