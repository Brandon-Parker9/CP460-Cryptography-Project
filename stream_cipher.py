"""
This stream cipher:
- includes all ascii characters form number 32 to 126
- Will be using the following LFSR x^8+x^1+1
"""
# imports

#  ********** this package needs to be installed **********
from langdetect import detect, detect_langs
#  ********** this package needs to be installed **********

import time

# Constants
MOD = 126-32 + 1
NORMALIZATION = 32
BINARY_EIGHT_ONES = 0b11111111

# Functions

def generate_eight_bit_keystream(key):

    eight_bit_keystream = 0

    for i in range(8):

        #  get the two values the need to XOR together based on the choosen LFSR
        x_0 = key & 0b00000001
        x_1 = key & 0b00000010

        # XOR the two inputs that go back into the LFSR
        shift_bit = x_0 ^ (x_1 >> 1)

        # ***** Debug *****
        # print(f"x^1 Number: {x_1} x^1 Binary: {bin(x_1)}  x^0 Number: {x_0} x^0 Binary: {bin(x_0)} shift_bit Number: {shift_bit} shift_bit Binary: {bin(shift_bit)}")

        # Update the key by shifting to the right 1 bit and adding the shift bit to the front
        key = (key >> 1) + (shift_bit << 7)

        # make a keystream that is 8 bits long based on the LFSR
        eight_bit_keystream += (shift_bit << i)

        # ***** Debug *****
            # print(f"Key: {key:#010b} Shifted out bit: {shift_bit}")f

    return eight_bit_keystream, key

def encrypt_LFSR(plain_text, key):
    """
    Simple function to encrypt the text by using an LFSR to based on the key value
    """
    encrypt_bit_stream = 0
    letter_count = 0

    # encrypt each letter
    for letter in plain_text:

        # 8 bit key stream to simplifiy encryption steps later
        letter_key_stream = 0b00000000
        
        letter_key_stream, key = generate_eight_bit_keystream(key)

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
        letter_key_stream, key = generate_eight_bit_keystream(key)

        # XOR the character with the 8 bits of the the key stream
        decrypt_character = eight_bits_to_decrypt ^ letter_key_stream

        # change the 8 bits to a character and add to the decrypted string
        decrypt_text += chr(decrypt_character)

        #  Shift the 8 right most bits to the right to remove them from bit stream
        encrypted_bit_stream = encrypted_bit_stream >> 8

    return decrypt_text

def brute_force_decrypt(encrypted_bit_stream):

    potential_cracked_text = []

    for i in range(BINARY_EIGHT_ONES + 1):
        print(i)

    return potential_cracked_text

plain_text = "hello world, this message was encrypted at some point!"
key = 0b000000001

print("Plain text: " + plain_text + "\n")

encrypted_bit_stream = encrypt_LFSR(plain_text, key)
print(f"Enccrypted Bit Stream: {encrypted_bit_stream:#0b} \n")


decrypted_bit_stream = decrypt_LSFR(encrypted_bit_stream, key)
print(f"Decrypted Bit Stream Message: {decrypted_bit_stream} \n")

brute_force_decrypt(encrypted_bit_stream)

print()

print(BINARY_EIGHT_ONES)
