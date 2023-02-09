## Author: Shivaz Sharma
## Date: 07/02/2023
## InvertedIndex: class contains the information about the index.txt

## Import desired modules for efficient and robust code implementation
from bs4 import BeautifulSoup 
import re
#from stemming.porter2 import stem
import time
import os
import sys
import math
import csv
from os.path import exists, join
from pathlib import Path

start = time.time()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
app_path = Path(__file__).resolve().parent.parent
print(" app_path name : ", app_path)
index_file_path = os.path.join(app_path, 'index.txt')
print(" index file path: ", index_file_path)
trec_file_path = os.path.join(app_path, 'trec.5000.xml')
stop_words_file = os.path.join(app_path, 'englishST.txt')
recipe_file_path = os.path.join(app_path, 'full_dataset.csv') #This file should be there in the folder before running the code

## Porter stemmer module for efficient stemming while pre-processing
#from stemming.porter2 import stem
from porter2stemmer import Porter2Stemmer
stemmer = Porter2Stemmer()

stop_word_list = []
## Module for populating list of stop words from file englishST.txt
def populateStopWords():
    word_list = open(stop_words_file).readlines()
    for w in word_list:
        stop_word_list.append(w.replace('\n',''))

## Module definition for pre-processing raw text and queries
## Steps: Tokenization, Stop-words removal and Stemming
## Input: raw data <Type:String>
## Output: terms list <Type:List>
def preProcessing(data):
    terms_list = []
    tmp_data = re.split('\W', data)
    #print ("stage 1 :", tmp_data)
    for word in tmp_data:
        #if word == ""  or re.match('\d+', word):
        if word == "":
            continue
        word = word.lower()
        if word in stop_word_list:
            continue
        terms_list.append(stemmer.stem(word))
    #print ("stage 2 :", terms_list)
    return terms_list

#Function to create the inverted index
def build_index_internal(ids, info):
    d = {}
    populateStopWords()
    #Making Inverted Index
    print('before preprocessing')
    for i in range(len(ids)):
        #Preprocessing the data of the document
        porter = preProcessing(info[i])
        #tokens = tokenization(info[i])
        #lower = case_folding(tokens)
        #stop = remove_stop_words(lower)
        #porter = porter_stemming(stop)
        document_id = ids[i]
        #Traversing the preprocessed data
        for j in range(len(porter)):
            word = porter[j]
            #If the word is new adding it to dictionary with the docID and it's position
            if(word not in d):
                d[word] = Pair()
                position = [j+1]
                d[word].details[document_id] = position
            #Word is already present in the dictionary
            else:
                #If it is a new docID for the word add the docID and it's postition for that word
                if(document_id not in d[word].details):
                    d[word].doc_freq += 1
                    position = [j+1]
                    d[word].details[document_id] = position
                #Else if docID is already stored for the word then just append the position for that docID
                #It means it's not the first time the word is seen in that docID
                else:
                    d[word].details[document_id].append(j+1)
    print('Dictionary populated')

    #Sorting the inverted index on basis of lexicographical orders of terms
    sorted_dict = dict(sorted(d.items(),key = lambda item: item[0]))
   
    print('Before writing in a file')
    #Storing the inverted index in memory
    with open(index_file_path, 'w') as file_obj:
        #Iterating word by word in the dictionary
        for word in sorted_dict:
            file_obj.write(word+":"+str(sorted_dict[word].doc_freq)+'\n') #Writing the word in the file
            information = sorted_dict[word].details #Getting details of docID and positions for the word
            #Sorting the data on basis of DocID
            inner_sort = dict(sorted(information.items(),key = lambda item: item[0]))
            sorted_dict[word].details = inner_sort
            #Iterating all the docIDs for the word and storing the data in the file
            for num in inner_sort:
                file_obj.write("\t" + str(num) + ": ") #Writing the docID
                length = len(inner_sort[num])
                #Storing the positions for that docID of the word
                for position in range(length):
                    if(position != length -1):
                        file_obj.write(str(inner_sort[num][position]) + ',')
                    else:
                        file_obj.write(str(inner_sort[num][position])) #Last position so won't have comma at the end
                file_obj.write('\n')

    print('After Writing in a File')
    return sorted_dict

def getInvertedIndexObj():
  return InvertedIndex.getInstance()
 
class Pair:
  def __init__(self):
    self.doc_freq = 1
    self.details = {}

class InvertedIndex:
  __instance = None
  @staticmethod
  def getInstance():
    """ Static access method. """
    if InvertedIndex.__instance == None:
      InvertedIndex()
    return InvertedIndex.__instance
  def __init__(self):
    """ Virtually private constructor. """
    if InvertedIndex.__instance != None:
      raise Exception("This class is a singleton!")
    else:
      InvertedIndex.__instance = self
      self.dictdata = {}

  def getIndexSize(self):
    print("Dictionary size: ", len(self.dictdata))
    return len(self.dictdata)

  def buildIndex(self):
    #Shivaz: Need to modify the parsing based on new recipe dataset 
    #Radhikesh: Commented the trec data and reading the data from recipe dataset

    # #Reading the xml file
    # with open(trec_file_path) as file_obj:
    #   data = file_obj.read()

    # #Parsing the xml file
    # soup = BeautifulSoup(data,'lxml')
    # doc_id = soup.find_all('docno') #Getting the document ids
    # headline = soup.find_all('headline') #Getting the headline tags
    # text = soup.find_all('text') #Getting the text tags
    # #Storing all the document ids and the data (Headline + Text)

    ids = []
    info = []

    # for i in range(len(doc_id)):
    #   ids.append(int(doc_id[i].string))
    #   info.append(str(headline[i].string + text[i].string))

    doc_id = 1
    with open(recipe_file_path, 'r', encoding="utf-8") as csv_file:
      next(csv_file)
      csv_reader = csv.reader(csv_file, delimiter=',')
      for row in csv_reader:
          doc_data = row[1] + " " + row[2] + " " + row[3] + " " + row[6]
          ids.append(doc_id)
          info.append(doc_data)
          doc_id += 1

          #Can put the number of documents to be populated in the idex.txt file
          if(doc_id == 501): #Populating first 500 documents
            break
    print('Before Build')
    self.dictdata = build_index_internal(ids, info)
    print('After Build')

  def loadIndexInMemory(self):
    print ("Getting a call here ")
    data = []
    #Fetch data from index file 
    with open(index_file_path, 'r') as f:
      data = f.readlines()
    d = {}
    curr_word = ''
    #Parsing the index file by iterating line by line
    for line in data:
      line = line.replace('\n','')
      line = line.replace(' ','')
      #Splitting data of line on basis of ':' or 'tab' 
      info = re.split(':|\t',line)
      #If splitted data has only 2 elements it will be first line of new word
      if(len(info) == 2):
          val = Pair()
          val.doc_freq = int(info[1]) #Getting doc freq
          curr_word = info[0] #Getting word
          d[curr_word] = val #Storing in the dictionary
      #Otherwise it will be a line which has docIDs and positions of the word
      else:
          positions = info[2].split(',') #Getting poisitions by splitting on basis of comma
          positions = [int(i) for i in positions]
          d[curr_word].details[int(info[1])] = positions #Storing docID and positions for that word in the dictionary
    
    self.dictdata = d

##s = InvertedIndex()
##print(s)
#
print ("Shivaz !!!")
s = InvertedIndex.getInstance()

s.getIndexSize()
s.buildIndex()
s.loadIndexInMemory()
s.getIndexSize()

print('It took', time.time()-start, 'seconds to do all the process')
