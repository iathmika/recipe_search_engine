from django.shortcuts import render
from rest_framework import viewsets      
from django.http import HttpResponse
from django.template import loader
from .utils import InvertedIndex
from .utils import RankSearch
from .utils import BooleanSearch
from .models import RecipeData
import os
from os.path import exists
from pathlib import Path
from bson.json_util import dumps, loads
import json
import time
import traceback

import nltk
from nltk.corpus import wordnet
#nltk.download('wordnet')
#nltk.download('omw-1.4')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
app_path = Path(__file__).resolve().parent
index_file_path = os.path.join(app_path, 'sample_index.json')
scraped_file_path = os.path.join(app_path, 'scraped_recipies.json')

print ("Index file path :" + index_file_path)

## By default TFIDF technique is used ##
## 1 -> tfidf
## 2 -> bm25
## (!1 && !2) -> Boolean, Proximity, Phrase
search_type = "tfidf"

## This method reads the scraped data and updates the existing running index
def updateIndvertedIndex(scraped_file):
  #step 1: Dictionary already loaded
  recipe_obj = RecipeSearch.getInstance()
  print ("UpdateInvertedIndex object :", recipe_obj)
  assert(recipe_obj.indexObj.getIndexSize() > 0)
  with open(scraped_file, 'rb') as f:
    scraped_recipe_data = json.loads(f.read())
    new_recipe_id = 2299999
    ids = []
    info = []
    for recipe in scraped_recipe_data['data']:
      recipe['id'] = new_recipe_id
      #print("Title type : ", type(recipe['title']))
      #print("Ingredients type : ", type(recipe['ingredients']))
      doc_data = recipe['title'] + " " + ' '.join(recipe['ingredients'])
      ids.append(recipe['id'])
      info.append(doc_data)
      #if new_recipe_id == 2300010:
      #  break
      new_recipe_id += 1
   
    print("Before update : " + str(recipe_obj.indexObj.getIndexSize()))
    if len(ids) > 0:
      recipe_obj.indexObj.updateIndex(ids, info)
    print("After update : " + str(recipe_obj.indexObj.getIndexSize()))


class RecipeSearch:
  indexObj = None
  modelObj = None
  __instance = None
  @staticmethod
  def isInstanceEmpty():
    traceback.print_exc()
    print ("Getting call in isInstanceEmpty()")
    return (RecipeSearch.__instance == None)
  
  @staticmethod
  def getInstance():
    """ Static access method. """
    if RecipeSearch.__instance == None:
      print ("Printing new instance of RecipeSearch !!")
      RecipeSearch()
    return RecipeSearch.__instance

  @staticmethod
  def getRecipeIndexObj():
    return RecipeSearch.__instance.indexObj
  
  @staticmethod
  def getRecipeModelObj():
    return RecipeSearch.__instance.modelObj

  def __init__(self):
    """ Virtually private constructor. """
    if RecipeSearch.__instance != None:
      raise Exception("This class is a singleton!")
    else:
      RecipeSearch.__instance = self
      RecipeSearch.indexObj = None
      
  def index(request):
    ## Need to create landing page to show the user
    template = loader.get_template('landing.html')
    index_obj = RecipeSearch.getInstance().getRecipeIndexObj()
    
    index_obj.loadDocLenDictInMemory()
    #print ("Loaded document len dictionary size: ", indexObj.getDocLenDict())
    
    indx_size = str(index_obj.getIndexSize())
    print(" indx_size : ", indx_size)
    return HttpResponse(template.render())
  
  

  def searchQueryResult(request):
    print ("Request method :", request.method)
    query = request.GET.get("query")
    #search_type = request.GET.get("search_type")
    #print("Before expansion: ", query)

    ##########Query expansion########
    query = expand_query(query)

    #print("After expansion: ", query)



    index_obj = RecipeSearch.getInstance().getRecipeIndexObj()
    recipe_obj = RecipeSearch.getInstance().getRecipeModelObj()
    start = time.time()
    if (search_type == "tfidf"):
      rsl = RankSearch.rankByTFIDF(query, index_obj)
    elif (search_type == "bm25"):
      rsl = RankSearch.rankByBM25(query, index_obj)
    elif (search_type == "other"):
      rsl = BooleanSearch.boolean_search(query, index_obj)
    if rsl!=None:
      recipes = {"results" : []}
      recipes_cursor = recipe_obj.get_multiple_recipes(list(rsl.keys())[:300])
      
      list_cursor = list(recipes_cursor)
      start = time.time()
      for data in list_cursor:
          recipes["results"].append(data)
      print("Loop time: ", time.time() - start)
      # print("List cursor: ",list_cursor)
      # recipes["results"] = dumps(list_cursor, indent = 2)
      recipes_object = json.dumps(recipes)
      #print("List cursor: ",list_cursor)
      # print("Recipes_object: ",recipes_object)
    else:
      recipes_object = json.dumps({})
      print ("Sorry! No search results found")
    # recipes_object = json.dumps({})
    return HttpResponse(recipes_object) 


  def home(request):
    return HttpResponse("Hello World!")
    # recieved_var = testing_func("Whats-up")
    # return HttpResponse(recieved_var)
  
  def products(request):
    return HttpResponse('products')
  
  def customer(request):
    return HttpResponse('customer')

  def scrapeRecipes(request):
    if (RecipeSearch.isInstanceEmpty() == False):
     updateIndvertedIndex(scraped_file_path)
    return HttpResponse('Scraped Data')

if (RecipeSearch.isInstanceEmpty()):
  recipe_obj = RecipeSearch.getInstance()
  recipe_obj.indexObj = InvertedIndex.getInvertedIndexObj()
  recipe_obj.modelObj = RecipeData.getInstance()

  print("Recipe object: ", recipe_obj)
  print("Index object: ", recipe_obj.indexObj)
  print("Model object: ", recipe_obj.modelObj)

  ## Important step Check if index.txt exists or not, if not need to create one
  if (not exists(index_file_path)):
    print ("Getting call here incorrectly")
    recipe_obj.indexObj.buildIndex()

  ## Step 2: Load index in memory for searching query results
  start = time.time()
  recipe_obj.indexObj.loadIndexInMemory()
  print ("Dictionary size loaded : ", recipe_obj.indexObj.getIndexSize())
  recipe_data = RecipeData.getInstance()
  print("Time taken to load dictionary: ", time.time() - start)

# Function to expand a query
def expand_query(query):
  # tokenize the query
  words = nltk.word_tokenize(query)
  # print(words)

  # create a list to hold the expanded terms
  expanded_words = []

  # loop through each word in the query
  for word in words:
      # get the synonyms for each word
      synonyms = wordnet.synsets(word)
      expanded_words.append(word)
      print(synonyms)
      for syn in synonyms:
          for lemma in syn.lemmas():
              if lemma.name() not in expanded_words:
              # add the synonym to the list of expanded terms
                expanded_words.append(lemma.name())

  # return the expanded query as a string
  return ' '.join(expanded_words)



