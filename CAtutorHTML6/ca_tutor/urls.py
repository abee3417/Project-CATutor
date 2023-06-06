from django.urls import path
from . import views

app_name = 'ca_tutor'

urlpatterns = [
    path('', views.index, name='index'),
    path('code/', views.code, name='code'),
    path('result/', views.result, name='result'),
]