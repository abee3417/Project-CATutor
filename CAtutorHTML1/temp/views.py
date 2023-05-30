from django.shortcuts import render, redirect

def index(request):
    return render(request, 'temp/index.html')

def code(request):
    return render(request, 'temp/code.html')