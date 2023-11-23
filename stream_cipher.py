"""
This stream cipher:
- includes all ascii characters form number 32 to 126
- Will be using the following LFSR x^8+x^1+1
"""

# imports

#  ********** this package needs to be installed **********
from langdetect import detect_langs
#  ********** this package needs to be installed **********

import time

# Constants
BINARY_EIGHT_ONES = 0b11111111

# Functions

def generate_keystream(key, length):
    """
    Genertes a keystream of length asked for and updates the key
    """

    keystream = 0

    for i in range(length):

        #  get the two values the need to XOR together based on the choosen LFSR
        x_0 = key & 0b00000001
        x_1 = key & 0b00000010

        # XOR the two inputs that go back into the LFSR
        shift_bit = x_0 ^ (x_1 >> 1)

        # Update the key by shifting to the right 1 bit and adding the shift bit to the front
        key = (key >> 1) + (shift_bit << 7)

        # make a keystream that is based on the LFSR
        keystream += (shift_bit << i)

    return keystream, key

def encrypt_LFSR(plain_text, key):
    """
    Simple function to encrypt the text one characer at a time by using an LFSR to based on the key value
    """
    encrypt_bit_stream = 0
    letter_count = 0

    # encrypt each letter
    for letter in plain_text:

        # 8 bit key stream to simplifiy encryption steps later
        letter_key_stream = 0b00000000
        
        letter_key_stream, key = generate_keystream(key, 8)

        # XOR the character with the 8 bits of the the key stream
        encrypt_character = ord(letter) ^ letter_key_stream

        # shift the encrypted character to the left as amany characters we have proccessed
        encrypt_character = encrypt_character << (8 * letter_count)
        
        # add the next encrypted character to the beging of the bit stream
        encrypt_bit_stream += encrypt_character

        # Increase the number of letters we have proccessed
        letter_count += 1

    return encrypt_bit_stream

def decrypt_LSFR(encrypted_bit_stream, key):
    """
    Simple function to decrypt the text by grabing 8 bits at a time from the encrypted bit stream
    and then generating the key needed and XORing them together
    """

    decrypt_text = ""

    # decrypt each letter
    while (encrypted_bit_stream>0):

        letter_key_stream = 0b00000000

        # grab the 8 right most bits for decryption
        eight_bits_to_decrypt = encrypted_bit_stream & BINARY_EIGHT_ONES

        # Generate the letter keystream based on the key
        letter_key_stream, key = generate_keystream(key, 8)

        # XOR the character with the 8 bits of the the key stream
        decrypt_character = eight_bits_to_decrypt ^ letter_key_stream

        # change the 8 bits to a character and add to the decrypted string
        decrypt_text += chr(decrypt_character)

        #  Shift the 8 right most bits to the right to remove them from bit stream
        encrypted_bit_stream = encrypted_bit_stream >> 8

    return decrypt_text

def brute_force_crack(encrypted_bit_stream):

    #  used to track attack time
    start_time = time.time()

    all_options_of_original_text = [""] * (BINARY_EIGHT_ONES + 1)
    potential_cracked_text = []

    # brute force create all the strings possible 
    for i in range(BINARY_EIGHT_ONES + 1):
        all_options_of_original_text[i] = decrypt_LSFR(encrypted_bit_stream, i)

    #  go through all the possible strings
    for string in all_options_of_original_text:
        
        #  detect the languages
        detected_langs = detect_langs(string)
        
        # for each language detected, only select the ones where englich is great than 0.9
        for lang in detected_langs:

            if lang.lang == "en" and lang.prob > 0.9:
                potential_cracked_text.append(string)
    
    crack_time = round(time.time() - start_time, 2)

    return potential_cracked_text, crack_time

######################### Demo #########################

plain_text = "hello world, this message was encrypted at some point!"
key = 0b000000001

encrypted_bit_stream = encrypt_LFSR(plain_text, key)
decrypted_bit_stream = decrypt_LSFR(encrypted_bit_stream, key)

print("********** Demo **********\n")
print("Plain text: " + plain_text + "\n")
print(f"Enccrypted Bit Stream: {encrypted_bit_stream:#0b} \n")
print(f"Decrypted Bit Stream Message: {decrypted_bit_stream} \n")

try:
    potential_cracked_text_array, crack_time = brute_force_crack(encrypted_bit_stream)

    print(f"Potential Cracked texts(crack time: {crack_time}s): \n")
    for i in range(len(potential_cracked_text_array)):
        print(f"[{i}]--> {potential_cracked_text_array[i]}")
except:
    print("""Hello!

You are seeing this message because something went wrong! :( 
                   
Be sure to install the langdetect package --> pip install langdetect
          
After installation, please try running again! :)
""")
