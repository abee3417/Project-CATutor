from django.shortcuts import render, redirect

def index(request):
    return render(request, 'catutor/index.html')

def code(request):
    return render(request, 'catutor/code.html')

def result(request):
    return render(request, 'catutor/result.html')