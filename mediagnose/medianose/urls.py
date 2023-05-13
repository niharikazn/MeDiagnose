from django.urls import path,include
from . import views
from . import admin

urlpatterns = [
    path('', views.index, name='index'),
path('index', views.index, name='index'),
path('diagnose', views.diagnose, name='diagnose'),
path('diagnoser', views.diagnoser, name='diagnoser')
]