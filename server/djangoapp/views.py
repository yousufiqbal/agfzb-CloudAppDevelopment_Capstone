from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
  return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
  return render(request, 'djangoapp/contact.html')

def login_request(request):
  context = {}
  if request.method == "POST":
      username = request.POST['username']
      password = request.POST['password']
      user = authenticate(username=username, password=password)
      if user is not None:
          login(request, user)
          return redirect('djangoapp:index')
      else:
          return render(request, 'djangoapp/index.html', context)
  else:
    # If not a POST request redirect to main page..
    return redirect('djangoapp:index')

def logout_request(request):
  logout(request)
  return redirect('djangoapp:index')

def registration_request(request):
  if request.method == 'GET':
    return render(request, 'djangoapp/registration.html')

  elif request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']

    try: 
      User.objects.get(username=username)
      context = { "error" : "Already a user"}
      return render(request, 'djangoapp/index.html', context)

    except User.DoesNotExist:
      user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
      login(request, user)
      return redirect('djangoapp:index')

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

