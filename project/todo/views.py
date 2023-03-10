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

# Build paths inside the project like this: BASE_DIR / 'subdir'.
app_path = Path(__file__).resolve().parent
index_file_path = os.path.join(app_path, 'sample_index.json')
print ("Index file path :" + index_file_path)

## By default TFIDF technique is used ##
## 1 -> tfidf
## 2 -> bm25
## (!1 && !2) -> Boolean, Proximity, Phrase
search_type = "tfidf"

class RecipeSearch:
  indexObj = None
  __instance = None
  @staticmethod
  def isInstanceEmpty():
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
    print(query)
    index_obj = RecipeSearch.getInstance().getRecipeIndexObj()
    start = time.time()
    if (search_type == "tfidf"):
      rsl = RankSearch.rankByTFIDF(query, index_obj)
    elif (search_type == "bm25"):
      rsl = RankSearch.rankByBM25(query, index_obj)
    elif (search_type == "other"):
      rsl = BooleanSearch.boolean_search(query, index_obj)
    output_str = "::::: Retreived Document IDs :::::: \n"
    """""
    recipes = {"results" : []}
    recipe_data = RecipeData.getInstance()
    recipes = recipe_data.get_multiple_recipes(list(rsl.keys()))

    if rsl != None:
      for did in rsl:
      # for did in rsl.keys():
        did = str(did-1)
        print("did: ",did)
        recipe_data = RecipeData.getInstance()
        title = recipe_data.get_recipe_fields(did)[0]
        ingredients = recipe_data.get_recipe_fields(did)[1]
        directions = recipe_data.get_recipe_fields(did)[2]     
        recipes["results"].append({"id" : did, "title": title, "ingredients": ingredients, "directions": directions})
        #output_str += str(did) + title + "\n"
      recipes_object = json.dumps(recipes) 
      print(recipes_object)
    else:
      print ("Sorry! No search results found")
    return HttpResponse(recipes_object) 
    
      recipe_data = RecipeData.getInstance()
      #If using Mongo DB fetch data
      # recipes = recipe_data.get_multiple_recipes(list(rsl.keys()))
      # output_str = ""
      # for data in recipes:
      #   output_str += str(data['id']) + data['title'] + data['ingredients'] + data['directions']
      ## Shivaz: Need for testing
      for did in rsl.keys():
        #Single MongoDB calls not efficient
        # title = recipe_data.get_recipe_fields(did)[0]
        # output_str += str(did) + title + "\n"
        output_str += str(did) + "\n"

    else:
      print ("Sorry! No search results found")
    print("Time taken for tfidf search: ", time.time() - start)
    return HttpResponse(output_str) 
   """

  def searchQueryResult(request):
    print ("Request method :", request.method)
    query = request.GET.get("query")
    print(query)
    index_obj = RecipeSearch.getInstance().getRecipeIndexObj()
    start = time.time()
    if (search_type == "tfidf"):
      rsl = RankSearch.rankByTFIDF(query, index_obj)
    elif (search_type == "bm25"):
      rsl = RankSearch.rankByBM25(query, index_obj)
    elif (search_type == "other"):
      rsl = BooleanSearch.boolean_search(query, index_obj)
    if rsl!=None:
      recipes = {"results" : []}
      recipe_data = RecipeData.getInstance()
      rsl_list = [str(i-1) for i in list(rsl.keys())]
      print("rsl_list: ",rsl_list)
      recipes_cursor = recipe_data.get_multiple_recipes(rsl_list)
      #print("recipe_cursor: ",recipes_cursor)
      #for data in recipes_cursor:
        #print("data: ",data)
           
      list_cursor = list(recipes_cursor)
      print("List cursor: ",list_cursor)
      recipes["results"] = dumps(list_cursor, indent = 2)
      recipes_object = json.dumps(recipes)
      #print("List cursor: ",list_cursor)
      print("Recipes_object: ",recipes_object)
    else:
      recipes_object = json.dumps({})
      print ("Sorry! No search results found")
    return HttpResponse(recipes_object) 


      


    



  def home(request):
    return HttpResponse("Hello World!")
    # recieved_var = testing_func("Whats-up")
    # return HttpResponse(recieved_var)
  
  def products(request):
    return HttpResponse('products')
  
  def customer(request):
    return HttpResponse('customer')


if (RecipeSearch.isInstanceEmpty()):
  recipe_obj = RecipeSearch.getInstance()
  recipe_obj.indexObj = InvertedIndex.getInvertedIndexObj()
  ## Important step Check if index.txt exists or not, if not need to create one
  if (not exists(index_file_path)):
    print ("Getting call here incorrectly")
    recipe_obj.indexObj.buildIndex()

  ## Step 2: Load index in memory for searching query results
  start = time.time()
  recipe_obj.indexObj.loadIndexInMemory()
  print("Time taken to load dictionary: ", time.time() - start)
  

