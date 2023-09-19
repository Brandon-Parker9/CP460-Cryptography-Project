# this shift cipher includes all ascii characters form number 32 to 126

# imports

from langdetect import detect, detect_langs
import time

# Constants
MOD = 126-32 + 1

# Functions

def encrypt(plain_text, key):
    """
    Simple function to encrypt the text by shifting to the right based on the key value
    while keeping within the MOD value
    """
    encrypt_text = ""

    for letter in plain_text:
        encrypt_text += chr(((ord(letter) - 32 + key) % MOD) + 32)

    return encrypt_text

def decrypt(encrypted_text, key):
    """
    Simple function to decrypt the text by shifting to the left based on the key value
    while keeping within the MOD value
    """

    decrypt_text = ""

    for letter in encrypted_text:
        decrypt_text += chr(((ord(letter) - 32 - key) % MOD) + 32)

    return decrypt_text

def brute_force_crack(encrypted_text):
    """
    Try cracking the message by going through all poosible options. Then detect 
    the language and return the english languages that have a probability greater than .90
    """
    #  used to track attack time
    start_time = time.time()

    all_options_of_original_text = [""] * (MOD-1)
    potential_cracked_text = []

    # brute force create all the strings possible 
    for letter in encrypted_text:
        for i in range(MOD - 1):
            all_options_of_original_text[i] += chr(((ord(letter) - 32 - i) % MOD) + 32)

    #  go through all the possible strings
    for string in all_options_of_original_text:
        
        #  detect the languages
        detected_langs = detect_langs(string)
        
        # for each language detected, only select the ones where englich is great than 0.9
        for lang in detected_langs:

            if lang.lang == "en" and lang.prob > 0.9:
                potential_cracked_text.append(string)
    
    crack_time = round(time.time() - start_time, 2)

    # return the list of all potential english messages and time it took to determine the messages
    return potential_cracked_text, crack_time


# Demo

plain_text = "hello world, this message was encrypted at some point!"
key = 3

encrypted_text = encrypt(plain_text, key)
decrypted_text = decrypt(encrypted_text, key)
potential_cracked_text_array, crack_time = brute_force_crack(encrypted_text)

print("Plain text: " + plain_text + "\n")
print("Encrypted text: " + encrypted_text + "\n")
print("Decrypted text: "+ decrypted_text + "\n")
print(f"Potential Cracked texts(crack time: {crack_time}s): \n")
for i in range(len(potential_cracked_text_array)):
    print(f"[{i}]--> {potential_cracked_text_array[i]}")


    
