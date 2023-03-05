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

# Build paths inside the project like this: BASE_DIR / 'subdir'.
app_path = Path(__file__).resolve().parent
index_file_path = os.path.join(app_path, 'index.txt')
print ("Index file path :" + index_file_path)

## By default TFIDF technique is used ##
## 1 -> tfidf
## 2 -> bm25
## (!1 && !2) -> Boolean, Proximity, Phrase
search_type = "tfidf" 

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

    indexObj.loadDocLenDictInMemory()
    print ("Loaded document len dictionary size: ", indexObj.getDocLenDict())

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
    if (search_type == "tfidf"):
      rsl = RankSearch.rankByTFIDF(query, indexObj)
    elif (search_type == "bm25"):
      rsl = RankSearch.rankByBM25(query, indexObj)
    elif (search_type == "other"):
      rsl = BooleanSearch.boolean_search(query, indexObj)
    output_str = "::::: Retreived Document IDs :::::: \n"
    if rsl != None:
      for did in rsl.keys():
        recipe_data = RecipeData.getInstance()
        title = recipe_data.get_recipe_fields(did)[0]
        output_str += str(did) + title + "\n"
    else:
      print ("Sorry! No search results found")
    return HttpResponse(output_str) 
   
  def home(request):
    return HttpResponse("Hello World!")
    # recieved_var = testing_func("Whats-up")
    # return HttpResponse(recieved_var)
  
  def products(request):
    return HttpResponse('products')
  
  def customer(request):
    return HttpResponse('customer')
 
