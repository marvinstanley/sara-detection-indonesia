import sys
import os
sys.path.append(os.path.abspath("lib/"))
from normalizer import Normalizer
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

sentence = "RT @Gemacan70: Ayoo jaga keutuhan NKRI!!! Tangkap Penista Agama!!!  https://t.co/dxIDQ4ZQHV"

norm = Normalizer("lib/formalizationDict.txt")

# removes RT from tweets
if sentence[:3] == "RT ":
    sentence = sentence[3:]

sentence = norm.normalize(sentence)

word_tokens = word_tokenize(sentence)
indonesian_stops = stopwords.words('indonesian')
no_stops = [words for words in word_tokens if words not in indonesian_stops]

print(no_stops)

