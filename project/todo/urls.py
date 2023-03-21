## Usage: Whenever you add a new "view" (i.e. controller method) for todo application 
## Don't touch the backend/urls.py, just add it here in below urlpatterns list as below

from django.urls import path
from todo import views

urlpatterns = [
    path('home/', views.RecipeSearch.home),
    path('products/', views.RecipeSearch.products),
    path('customer/', views.RecipeSearch.customer),
    path('', views.RecipeSearch.index, name='landing'),
    path('search/', views.RecipeSearch.searchQueryResult, name='search_result'),
    path('scrape/', views.RecipeSearch.scrapeRecipes, name='scrape_land'),
    path('recommendations/', views.RecipeSearch.getRecommendation, name='recommendation_results'),
    path('nutrition/', views.RecipeSearch.getNutritionValue, name='nutrition_results'),
]
