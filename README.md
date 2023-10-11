# Shift, Stream, and Block Cipher in Action
Welcome! 

Here you will find some basic examples of the shift, stream, and block cipher written in python. As a part of these example, we include a brute force attack to try and crack the encryption for each of them. 

These were developed to demonstrate how they work and complement our report about the 3 ciphers. 

For details on what is needed to make them work or a more detailed description of each ciphers implementation, please read more below! 😊

# How To Use
1. git clone https://github.com/Brandon-Parker9/CP460-Project.git
2. install the langdetect package --> pip install langdetect

## Shift Cipher

The shift cipher is about as simple as it gets. First off it includes all the ASCII characters from 32 to 126 that way capitals and punctuation are included. From there on its pretty straight forward. There is an encrypt function that takes the plain text and the key value to shift call the characters to the right staying within the character ring using modulus operations. That function returns the encrypted message. There is a decryption function that takes the encrypted text and the key. This function returns the decrypted text by shifting the characters back to the left. 

Finally, we implemented a brute force attack which goes through all the possible key values. This function then uses the Lang detect package to sort through all the messages and return a list of ones that are believed to be english. After the function has completed it returns the list of potential messages and the amount of time it too to run through all the keys to show just how fast it can be broken. 

All the functions described above are demonstrated at the bottom of the file so all you have to do is run the file to see it in action!

## Stream Cipher

The stream cipher we implemented works on one character at a time and used the LFSR x^8+x^1+1. The encrypt function takes the plain text and the seed value for the LFSR and encrypts the message. This is done by converting all the characters into numbers then using python’s bitwise operators to XOR the keystream and bit stream together and then put them all together to make one long encrypted bitstream. This is then returned and encrypted. The decryption functions works in a very similar way by take the encrypted bitstream and the key. I then works on 8 bits at a time and XORing it with the keystream. The 8 bits are then converted back to a character and at the end the full decrypted string is returned. 

Once again, we implement a brute force attack, but we have many more keys to go through. This function also uses the langdetect package to sort through all the messages and return a list of ones that are believed to be English. After the function has completed it returns the list of potential messages and the amount of time it too to run through all the keys to show just how fast it can be broken.

All the functions described above are demonstrated at the bottom of the file so all you have to do is run the file to see it in action!

## Block Cipher

The block cipher is very similar to the stream cipher where the only difference is it works on 8 characters at a time instead of 1. This means the key and plain text are both 64 bits when they are XORed together. The encrypt and decrypt functions both work the same way.

For the last time we implement a brute force attack, but we have many more keys to go through. This function also uses the langdetect package to sort through all the messages and return a list of ones that are believed to be English. After the function has completed it returns the list of potential messages and the amount of time it too to run through all the keys to show just how fast it can be broken.

All the functions described above are demonstrated at the bottom of the file so all you have to do is run the file to see it in action!

## Contributers

- Brandon Parker 
- Nahor Yirgaalem