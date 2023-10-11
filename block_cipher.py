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
