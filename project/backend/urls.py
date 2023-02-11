from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from todo import views

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', include('todo.urls'))
]

