# Original Author
#################################################
# Tweet Normalizer
# 1. lowercasting
# 2. URL Removal
# 3. change the slang-words into formal-words
#
# Author: Alfan Farizki Wicaksono
#
# Information Retrieval Lab.
# Faculty of Computer Science
# University of Indonesia
#################################################

# Customized by Stanley Marvin
#################################################
# Added the ability to:
# 4. enhancing the conversion from slang-words
# into formal-words
# 5. remove symbols
#
# Custom: Stanley Marvin
#
# Do note that it impacts performance by
# a large margin
#
# please email me at stanleymarvin1999@yahoo.com
# if you have a more elegant solution in 
# for the enhanceFormalize function
#################################################

import re

class Normalizer(object):

   def __init__(self, dictFile="singkatan.dic"):
      ''' default dictionary file name is singkatan.dic '''
      self.dictFile = dictFile
      self.normDict = {}
      self.loadDict()
	  
   def loadDict(self):
      ''' we use this method to load content of dictionary file
          which is conveniently stored as a python dictionary object '''
      dataFile = open(self.dictFile, "r")
      for line in dataFile:
         line = line.strip() #remove \n
	     #key: slang word, #value: norm word
         slangNorm = line.split('\t')
         if (len(slangNorm) > 1):
            self.normDict[slangNorm[0]] = slangNorm[1]
      dataFile.close()
	     
   def lowerCast(self, word):
      ''' return word in lowercase version '''
      return word.strip().lower()
	  
   def arrStrToSnt(self, arrStr):
      ''' change array of string to sentence '''
      return ' '.join(arrStr)

   def enhancedFormalize(self, word):
      # customized By Stanley Marvin
      formalize_word_1 = ["([a-z0-9]+)ny$", "([a-z0-9]+)nk$", "([a-z0-9]+)dh$"]
      result_1 = ["nya", "ng", "t"]

      formalize_word_2 = "([a-z0-9]+)x$"
      result_2 = "nya"

      formalize_word_3 = "([a-z0-9]+)2$"

      formalize_word_4 = "(?P<word1>[a-z0-9]+)2(?P<word2>[a-z0-9]*$)"

      num = ["12", "13", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
      alpha = ["r", "b", "o", "i", "r", "e", "a", "s", "g", "j", "b", "g"]

      for j in range(0, len(formalize_word_1)):
         x2 = re.search(formalize_word_1[j], word)
         if x2 != None:
               word = re.sub(formalize_word_1[j], x2.string[:(len(x2.string)-2)] + result_1[j] , word)

      x2 = re.search(formalize_word_2, word)
      if x2 != None:
         word = re.sub(formalize_word_2, x2.string[:(len(x2.string)-1)] + result_2, word)

      x2 = re.search(formalize_word_3, word)
      if x2 != None:
         word = re.sub(formalize_word_3, x2.string[:(len(x2.string)-1)]+"-"+x2.string[:(len(x2.string)-1)] , word)

      
      x2 = re.search(formalize_word_4, word)
      if x2 != None:
         word = re.sub("([a-z0-9]+)2([a-z0-9]*)$", x2.group("word1")+"-"+x2.group("word1")+x2.group("word2") , word)

      word = re.sub("oe","u",word)

      x2 = re.search(r"(?P<word1>[0-9]+)(?P<word2>[a-zA-Z]+)(?P<word3>[0-9a-zA-Z]*)", word)
      if x2 != None:
         for j in range(0, len(num)):
               if x2.group('word1') == num[j]:
                  word = re.sub("[0-9]+[a-zA-Z]+[0-9a-zA-Z]*", alpha[j] +x2.group('word2')+x2.group('word3'), word)
                  break
         
      x2 = re.search(r"(?P<word1>[a-zA-Z]+)(?P<word2>[0-9]+)(?P<word3>[0-9a-zA-Z]*)", word)
      while x2 != None:
         for j in range(0, len(num)):
               if x2.group('word2') == num[j]:
                  word = re.sub("[a-zA-Z]+[0-9]+[0-9a-zA-Z]*", x2.group('word1')+ alpha[j] +x2.group('word3'), word)
                  break
         x2 = re.search(r"(?P<word1>[a-zA-Z]+)(?P<word2>[0-9]+)(?P<word3>[0-9a-zA-Z]*)", word)

      return word
         
   def removeSymbols(self,word):
      # customized By Stanley Marvin
      word = re.sub("[.,:;!-?\"\'()0-9*]+", "", word)
      return word
   
   def normalize(self, tweet):
      ''' normalize the tweet, tweet must be words separated by white-space'''
      tweetWords = tweet.split()
      newTweet = map(lambda x:self.lowerCast(x), tweetWords)
      newTweet = map(lambda x:self.normDict[x] if x in self.normDict else x, newTweet)
      
	   # url removal
      newTweet = filter(lambda x:'https://' not in x, newTweet)
      newTweet = filter(lambda x:'@' not in x, newTweet) # I figured that a user mention isn't necassery for the data -Stanley Marvin

      newTweet = map(lambda x:self.enhancedFormalize(x), newTweet)
      newTweet = map(lambda x:self.removeSymbols(x), newTweet)
      return self.arrStrToSnt(newTweet)
