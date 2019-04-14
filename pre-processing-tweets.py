import sys
import os
sys.path.append(os.path.abspath("lib/"))
from normalizer-customized import Normalizer
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

#VARIABLES
inputPath = "data/labeled/2019-04-15.txt"
outputPath = "data/preprocessed/2019-04-15.txt"

#ALGORITHM
if os.path.isfile(inputPath):
    norm = Normalizer("lib/formalizationDict.txt")
    txtFile = open(inputPath,"r")
    output = open(outputPath,"w")
    for i,j in enumerate(txtFile):
        label = j[:1]
        sentence = (j[2:len(j)-1])
        if sentence[:3] == "RT ": # removes RT from tweets
            sentence = sentence[3:]
        sentence = norm.normalize(sentence)
        word_tokens = word_tokenize(sentence)
        indonesian_stops = stopwords.words('indonesian')
        no_stops = [words for words in word_tokens if words not in indonesian_stops]
        toWrite = label+'\t'+str(no_stops)+'\n'
        output.write(toWrite)
        print(no_stops)
    txtFile.close()
else:
    print('FILE NOT FOUND')

