from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from pathlib import Path
import os


# Create your views here.


def index(request):

    BASE_DIR = Path(__file__).resolve().parent.parent

    a = f"{BASE_DIR}/templates/index.html"

    return render(request, 'index.html')
