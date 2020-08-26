from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

# Create your views here.

def home(request):
#    return HttpResponse("Hello world!!!")
    return render(request, "home.html", {"usuario":"Fabio"})

def contact(request):
    return render(request, "contact.html")
    