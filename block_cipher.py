"""
This block cipher:
- includes all ascii characters form number 32 to 126
- Will be using the following LFSR x^8+x^1+1
- it will encrypt 8 characters at a time totalling 64 bits encryted at a time
"""
# imports

#  ********** this package needs to be installed **********
from langdetect import detect, detect_langs
#  ********** this package needs to be installed **********

import time

# Constants
BINARY_SIXTYFOUR_ONES = 0b1111111111111111111111111111111111111111111111111111111111111111
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
    Simple function to encrypt the text 8 characers at a time by using an LFSR to based on the key value
    """
    encrypt_bit_stream = 0
    letter_count = 0

    # encrypt 8 characters at a tiem
    for i in range(len(plain_text)//8 + 1):

        eight_character_block_of_bits = 0b00000000 * 8
        eight_character_block_encrypted = 0b00000000 * 8
        letter_count = 0

        eight_character_substring = plain_text[(8*i):(8+(8*i))]

        # combine eight letters together to make a 64bit number
        for letter in eight_character_substring:
            
            # add the binary version of the number to plain text bit stream
            eight_character_block_of_bits += (ord(letter) << (8 * letter_count))

            # Debug
            # print(f"Letter: {letter} binary letter: {ord(letter):#010b} bit stream: {eight_character_block_of_bits:#066b}")

            # Increase the number of letters we have proccessed
            letter_count += 1


        # 64 bit key stream to simplifiy encryption steps later
        block_key_stream = 0b00000000 * 8
        
        block_key_stream, key = generate_keystream(key, 64)

        # XOR the character with the 8 bits of the the key stream
        eight_character_block_encrypted = eight_character_block_of_bits ^ block_key_stream

        # debug
        # print("*****")
        # print(f"bit stream: {eight_character_block_of_bits:#066b}")
        # print(f"key stream: {block_key_stream:#066b}")
        # print(f"encr block: {eight_character_block_encrypted:#066b}")
        # print("*****")


        # shift the eight character encrypted block to the left as many blocks we have proccessed
        eight_character_block_encrypted = eight_character_block_encrypted << (64 * i)
        
        # # add the next encrypted character to the beging of the bit stream
        encrypt_bit_stream += eight_character_block_encrypted

    return encrypt_bit_stream

def decrypt_LSFR(encrypted_bit_stream, key):
    """
    Simple function to decrypt the text by grabing 8 bits at a time from the encrypted bit stream
    and then generating the key needed and XORing them together
    """

    decrypt_text = ""

    # decrypt each letter
    while (encrypted_bit_stream>0):

        block_key_stream = 0b00000000 * 8

        # grab the 64 right most bits for decryption
        eight_character_block_to_decrypt = encrypted_bit_stream & BINARY_SIXTYFOUR_ONES

        # Generate the letter keystream based on the key
        block_key_stream, key = generate_keystream(key, 64)

        # XOR the character with the 8 bits of the the key stream
        decrypt_block = eight_character_block_to_decrypt ^ block_key_stream

        for i in range(8):
            decrypt_character = decrypt_block & BINARY_EIGHT_ONES

            if decrypt_character > 0:
                # change the 8 bits to a character and add to the decrypted string
                decrypt_text += chr(decrypt_character)

            decrypt_block = decrypt_block >> 8

        #  Shift the 8 right most bits to the right to remove them from bit stream
        encrypted_bit_stream = encrypted_bit_stream >> 64

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

# Demo

plain_text = "hello world, this message was encrypted at some point!"
key = 0b000000001

print(f"Length of string: {len(plain_text)} // division: {len(plain_text)//8} // * 8: {(len(plain_text)//8) * 8}")

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