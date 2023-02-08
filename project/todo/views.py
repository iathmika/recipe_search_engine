from django.shortcuts import render
from .serializers import TodoSerializer 
from rest_framework import viewsets      
from .models import Todo           
from django.http import HttpResponse
from django.template import loader
from .utils import InvertedIndex
from os.path import exists

## Create an index of inverted index when search engine is intialized
indexObj = InvertedIndex.getInvertedIndexObj()

class TodoView(viewsets.ModelViewSet):
  serializer_class = TodoSerializer   
  queryset = Todo.objects.all()

def index(request):
  ## Need to create landing page to show the user
  #template = loader.get_template('landing.html')
  
  ## Important step Check if index.txt exists or not, if not need to create one
  if (not exists('index.txt')):
    indexObj.buildIndex()

  ## Step 2: Load index in memory for searching query results
  indexObj.loadIndexInMemory()
  print ("Loaded dictionary size: ", indexObj.getIndexSize())
  #return HttpResponse(template.render())
  indx_size = str(indexObj.getIndexSize())
  print(" indx_size : ", indx_size)
  return HttpResponse("Searching results returned : " + indx_size)

#def SearchQueryResult(request, query):
#  ## This controller function is invoked when user inputs the query in the search box
   
def home(request):
  recieved_var = testing_func("Whats-up")
  return HttpResponse(recieved_var)

def products(request):
  return HttpResponse('products')

def customer(request):
  return HttpResponse('customer')
 
