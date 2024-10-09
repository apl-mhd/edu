from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from pathlib import Path
import os


# Create your views here.


def index(request):
    return render(request, 'index.html')


def student(request):
    return render(request, 'student.html')