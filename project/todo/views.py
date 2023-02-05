from django.shortcuts import render
from .serializers import TodoSerializer 
from rest_framework import viewsets      
from .models import Todo           

from bs4 import BeautifulSoup
import re
from stemming.porter2 import stem
import time
import os
import math
from os.path import exists

class Pair:
    def __init__(self):
        self.doc_freq = 1
        self.details = {}

#Function to get tokens
def tokenization(data):
    tokens = re.split(r"[\b\W\b]+",data)
    return tokens

#Function to make the tokens lower case
def case_folding(tokens):
    return [i.lower() for i in tokens if i!= '']

#Function to get the stop words
def stop_words():
    with open('englishST.txt','r') as file_obj:
        stop_words = file_obj.read().splitlines()
    return stop_words

#Function to remove the stop words
def remove_stop_words(lower_case_words):
    stop = stop_words()
    return [i for i in lower_case_words if (i not in stop)]

#Function to do Proter's stemming
def porter_stemming(words_after_removing_stop):
    return [stem(i) for i in words_after_removing_stop]

#Reading the xml file
with open('trec.5000.xml') as file_obj:
    data = file_obj.read()

#Parsing the xml file
soup = BeautifulSoup(data,'lxml')
doc_id = soup.find_all('docno') #Getting the document ids
headline = soup.find_all('headline') #Getting the headline tags
text = soup.find_all('text') #Getting the text tags
#Storing all the document ids and the data (Headline + Text)
ids = []
info = []
for i in range(len(doc_id)):
    ids.append(int(doc_id[i].string))
    info.append(str(headline[i].string + text[i].string))

#Function to create the inverted index
def inverted_index():
    d = {}

    #Making Inverted Index
    for i in range(len(ids)):
        #Preprocessing the data of the document
        tokens = tokenization(info[i])
        lower = case_folding(tokens)
        stop = remove_stop_words(lower)
        porter = porter_stemming(stop)
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

    #Sorting the inverted index on basis of lexicographical orders of terms
    sorted_dict = dict(sorted(d.items(),key = lambda item: item[0]))
    
    #Storing the inverted index in memory
    with open('index.txt','w') as file_obj:
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

    d = sorted_dict

#Checking if data is not stored in memory then create inverted index
if(not exists('index.txt')):
    inverted_index()

#Fetch data from memory
with open('index.txt','r') as f:
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

def boolean_search():
    #If boolean result file is already present remove it
    if exists("results.boolean.txt"):
        os.remove("results.boolean.txt") 
    #Reading queries from file and storing them in a list
    with open('queries.boolean.txt','r') as boolean:
        queries = boolean.readlines()
    #Do process for all the queries of the file
    for query in queries:
        query = query.replace('\n','') #Replacing new line in readlines with nothing
        ans = set() #Set to store final document IDs for the query search
        full = set(ids) # Set which has Document IDs for the whole collection
        query = query.replace('"','')
        res = re.split(' |, |,', query)
        query_no = res.pop(0) #Storing query number by popping first element of query as first element is query_num
        operators = [] #Stack to store operators
        #Iterating the query
        while(res):
            val = res.pop(0)
            #If the element is a operator then store it in the stack and continue iterating the next elements
            if(val == 'NOT' or val == 'AND' or val == 'OR'):
                operators.append(val)
            #Otherwise it is a term
            else:
                curr = set() #Set to store document IDs of the current word
                num = 1 #Phrase search distance
                #If word is empty continue and see next words
                if(val == ''):
                    continue
                #If it has a '#' then it is proximity search and we update num with distance
                if(val[0] == '#'):
                    target  = val[1:].split('(')
                    num, val = int(target[0]), target[1]
                #Check if the word is in dictionary     
                if(stem(val.lower()) in d):
                    #Add all the documents of that word in the set
                    for i in d[stem(val.lower())].details:
                        curr.add(i)
                    #If the next term is again a word then it has to be either pharse or proximity search
                    if(res and res[0] != 'AND' and res[0] != 'OR' and res[0] != 'NOT'):
                        curr.clear()
                        val2 = res.pop(0) #Getting the next term
                        if(val2[-1] == ')'):
                            val2 = val2[:-1]
                        #Check if the other term is in dictionary
                        if(stem(val2.lower()) in d):
                            first = set(d[stem(val.lower())].details.keys())
                            second = set(d[stem(val2.lower())].details.keys())
                            common = first.intersection(second) #Getting common documents for the two words
                            #Iterating the positions of common documents for the two words
                            for i in common:
                                pos1 = d[stem(val.lower())].details[i]
                                pos2 = d[stem(val2.lower())].details[i]
                                p1, p2 = 0, 0
                                #Iterating till a match for phrase or proximity search or till one of the positions are exhausted(no match)
                                while(p1<len(pos1) and p2<len(pos2)):
                                    if(num == 1):#It iis a phrase search
                                        if((pos2[p2] - pos1[p1]) == num):#If the words are together and in that order add the document in the set and break to check for remaining common documents
                                            curr.add(i)
                                            break
                                        elif(pos1[p1]<pos2[p2]):
                                            p1 += 1
                                        else:
                                            p2 += 1
                                    else:#It is a proximity search
                                        if(abs(pos1[p1] - pos2[p2]) <= num):
                                            curr.add(i)#If it is within proximity range then add the document in the set and break to check for remaining common documents
                                            break
                                        elif(pos1[p1]<pos2[p2]):
                                            p1 += 1
                                        else:
                                            p2 += 1
                #Check if there are any operators in stack and do operations for all still stack becomes empty
                while(operators):
                    op = operators.pop()
                    if(op == 'NOT'):
                        curr = full - curr #NOT operation
                    elif(op == 'AND'):
                        curr = ans.intersection(curr) #AND operation
                    else:
                        curr = ans.union(curr) #OR operation
                ans = curr
        #If the query has output then sort on basis of document IDs and store it in the file
        if(ans):                   
            for i in sorted(ans):
                with open('results.boolean.txt','a') as file_obj:
                    file_obj.write(str(query_no) + ',' + str(i) + '\n')

if(exists("queries.boolean.txt")):
    boolean_search()

class TodoView(viewsets.ModelViewSet):  
    serializer_class = TodoSerializer   
    queryset = Todo.objects.all()     
