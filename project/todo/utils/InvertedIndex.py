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
import json
from os.path import exists, join
from pathlib import Path
import shutil

start = time.time()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
app_path = Path(__file__).resolve().parent.parent
print(" app_path name : ", app_path)
index_file_path = os.path.join(app_path, 'index.json')
print(" index file path: ", index_file_path)
trec_file_path = os.path.join(app_path, 'trec.5000.xml')
stop_words_file = os.path.join(app_path, 'englishST.txt')
recipe_file_path = os.path.join(app_path, 'full_dataset.csv') #This file should be there in the folder before running the code
#recipe_file_path = os.path.join(app_path, 'sample_data.csv') #This file should be there in the folder before running the code
doc_len_file = os.path.join(app_path, 'docLenFile.json')

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
        if word == ""  or re.match('\d+', word):
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
      self.docLenDict = {}

  def getIndexSize(self):
    return len(self.dictdata)

  def getIndexDict(self):
    return self.dictdata

  def getDocLenSize(self):
    return len(self.docLenDict)
  
  def getDocLenDict(self):
    return self.docLenDict

  def buildDocLenDict(self):
    doc_len_dict = {}
    doc_id = 1
    with open(recipe_file_path, 'r', encoding="utf-8") as csv_file:
      next(csv_file)
      csv_reader = csv.reader(csv_file, delimiter=',')
      for row in csv_reader:
        doc_data = preProcessing(row[1] + " " + row[2])
        doc_len = len(doc_data)
        doc_len_dict[int(doc_id)] = int(doc_len)
        #if ((doc_id % 100000) == 0):
          #print("Doc_id cnt : ", doc_id)
        doc_id += 1
   
    json_data = json.dumps(doc_len_dict);
    with open(doc_len_file,'w') as f:
      f.write(json_data)
    self.docLenDict = doc_len_dict
 
  def updateIndex(self, ids, info):
    print("Getting a call inside updateIndex ....")
    populateStopWords()
    #Making Inverted Index
    print('before preprocessing')
    for i in range(len(ids)):
      porter = preProcessing(info[i])
      document_id = ids[i]
      #Traversing the preprocessed data
      for j in range(len(porter)):
          word = porter[j]
          #If the word is new adding it to dictionary with the docID and it's position
          if(word not in self.dictdata):
              self.dictdata[word] = Pair()
              position = [j+1]
              self.dictdata[word].details[document_id] = position
          #Word is already present in the dictionary
          else:
              #If it is a new docID for the word add the docID and it's postition for that word
              if(document_id not in self.dictdata[word].details):
                  self.dictdata[word].doc_freq += 1
                  position = [j+1]
                  self.dictdata[word].details[document_id] = position
              #Else if docID is already stored for the word then just append the position for that docID
              #It means it's not the first time the word is seen in that docID
              else:
                  if (j+1) not in self.dictdata[word].details[document_id]:
                    self.dictdata[word].details[document_id].append(j+1)
       
    ### Need to update the existing index_file
    filename = "sample_index.json.bk"
    index_backup = os.path.abspath(os.path.join(app_path, filename))
    if index_backup.startswith(str(app_path)) and os.path.exists(index_backup):
      os.remove(index_backup)
    source = index_file_path
    target = os.path.abspath(os.path.join(app_path, filename))
    copy_success = True
    ## adding exception handling
    try:
      shutil.copy(source, target)
      print ("Index copy successful")
    except IOError as e:
      copy_success = False
      print("Unable to copy file. %s" % e)
    except:
      copy_success = False
      print("Unexpected error:", sys.exc_info())
  
    if copy_success == True:
     loaded_dict = {}
     print("loaded-dict length : ", len(loaded_dict))
     #sorted_dict = dict(sorted(self.dictdata.items(),key = lambda item: item[0]))
     #print("sorted-dict length : ", len(sorted_dict))
     print("Check before index_file deletion")
     ## Delete current index file
     os.remove(index_file_path)
     print("Problem arise after index_file deletion")
     print("Can we still access index_file ", index_file_path)
     print("loaded-dict length : ", len(loaded_dict))
     for word in self.dictdata.keys():
       loaded_dict[word] = self.dictdata[word].details
     
     print("loaded-dict length : ", len(loaded_dict))
     #print("sorted-dict length : ", len(sorted_dict))

     ## Write new index in dictionary
     with open(index_file_path,'w') as f1:
       f1.write(json.dumps(loaded_dict))
     print("sample_index.json written successfully")
    else:
      ## index.json.bk should be set to current index in-case of failure 
      shutil.copy(source, target)
     

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
 
  def loadDocLenDictInMemory(self):
    with open(doc_len_file, 'rb') as f:
      # self.docLenDict = json.loads(f.read())
      d = json.loads(f.read())
      for k in d.keys():
        self.docLenDict[int(k)] = d[k]
      assert(len(self.docLenDict) > 0)
 
  def loadIndexInMemory(self):
    print('Getting a call here inside loadIndexInMemory')
    populateStopWords()
    #Using json file now
    with open(index_file_path, 'r') as f:
      d = json.loads(f.read())
    for key in d.keys():
      val = Pair()
      val.doc_freq = len(d[key])
      # val.details = d[key]
      temp_d = {}
      for k in d[key].keys():
        temp_d[int(k)] = d[key][k]
      val.details = temp_d
      d[key] = val
      
    self.dictdata = d
   
    
  def computeAvgDocLen(self):
    avg_dl = 0
    sum = 0
    total_docs = self.getDocLenSize()
    if (len(self.docLenDict) > 0):
      for cnt in self.docLenDict.values():
        sum += cnt
    return int(sum/total_docs)


#s.getIndexSize()
#s.buildIndex()
#s.loadIndexInMemory()
#s.getIndexSize()
#s = InvertedIndex.getInstance()
#s.buildDocLenDict()
#s.loadDocLenDictInMemory()
#print (s.computeAvgDocLen())

#sample_dict = s.getDocLenDict()

print ('It took', time.time()-start, 'seconds to do all the process')
