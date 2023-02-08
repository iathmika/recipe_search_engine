## Usage: Whenever you add a new "view" (i.e. controller method) for todo application 
## Don't touch the backend/urls.py, just add it here in below urlpatterns list as below

from django.urls import path
from todo import views

urlpatterns = [
    path('', views.home),
    path('products/', views.products),
    path('customer/', views.customer),
    path('index/', views.index),
]
