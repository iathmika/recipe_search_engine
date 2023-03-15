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
import json

# Build paths inside the project like this: BASE_DIR / 'subdir'.
app_path = Path(__file__).resolve().parent
index_file_path = os.path.join(app_path, 'index.txt')
print ("Index file path :" + index_file_path)

class RecipeSearch:
  indexObj = None 
  def index(request):
    indexObj = InvertedIndex.getInvertedIndexObj()
    ## Need to create landing page to show the user
    template = loader.get_template('landing.html')
    
    ## Important step Check if index.txt exists or not, if not need to create one
    if (not exists(index_file_path)):
      print ("Getting call here incorrectly")
      indexObj.buildIndex()
  
    ## Step 2: Load index in memory for searching query results
    indexObj.loadIndexInMemory()
    print ("Loaded dictionary size: ", indexObj.getIndexSize())
    #return HttpResponse(template.render())
    indx_size = str(indexObj.getIndexSize())
    print(" indx_size : ", indx_size)
    return HttpResponse(template.render())
  
  def searchQueryResult(request):
    print ("Request method :", request.method)
    indexObj = InvertedIndex.getInvertedIndexObj()
    # There should be an assert that index is all ready loaded when we get a call in this search controller
    indexObj.loadIndexInMemory()
    ## This controller function is invoked when user inputs the query in the search box
    query = request.GET.get("query")
    print(query)
    flag = 1
    if(flag):
      rsl = RankSearch.processRankedQuery(query, indexObj)
    else:
      rsl = BooleanSearch.boolean_search(query,indexObj)  
    output_str = "::::: Retreived Document IDs :::::: \n"

    recipes = {"results" : []}
    if rsl != None:
      for did in rsl:
      # for did in rsl.keys():
        #did = str(did-1)
        #print("did: ",did)
        recipe_data = RecipeData.getInstance()
        print(recipe_data,"Working")
        title = recipe_data.get_recipe_fields(did)[0]
        ingredients = recipe_data.get_recipe_fields(did)[1]
        directions = recipe_data.get_recipe_fields(did)[2]   
        link = recipe_data.get_recipe_fields(did)[3]  
        recipes["results"].append({"id" : did, "title": title, "ingredients": ingredients, "directions": directions, "link":link})
        #output_str += str(did) + title + "\n"
      recipes_object = json.dumps(recipes) 
      #print(recipes_object)
    else:
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
 
