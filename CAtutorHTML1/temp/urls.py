from django.urls import path
from . import views

app_name = 'temp'

urlpatterns = [
    path('', views.index, name='index'),
    path('code/', views.code, name='code'),
]