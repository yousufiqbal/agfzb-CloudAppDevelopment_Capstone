from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
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
    if request.method == "GET":
      url = "https://us-south.functions.appdomain.cloud/api/v1/web/e17fb9fd-6ce8-4a0c-9841-4611c4d679f7/dealership-package/get-dealership.json"
      # Get dealers from the URL
      dealerships = get_dealers_from_cf(url)
      # Concat all dealer's short name
      dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
      # Return a list of dealer short name
      return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealerId):
    if request.method == "GET":
      url = "https://us-south.functions.appdomain.cloud/api/v1/web/e17fb9fd-6ce8-4a0c-9841-4611c4d679f7/dealership-package/get-reviews-of-dealership.json"
      # Get dealers from the URL
      reviews = get_dealer_reviews_from_cf(url, dealerId=dealerId)
      # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
      # Return a list of dealer short name
      return HttpResponse(reviews)


# Create a `add_review` view to submit a review
def add_review(request, dealerId):
  if request.user.is_authenticated and request.method == "POST":
    review = {
      "name" : request.POST['name'],
      "dealership" : dealerId,
      "review" : request.POST['review'],
      "purchase" : request.POST['purchase'],
      "purchase_date": request.POST['purchase_date'],
      "car_make": request.POST['car_make'],
      "car_model": request.POST['car_model'],
      "car_year": request.POST['car_year']
    }
    json_payload = {
      "review": review
    }
    url='https://us-south.functions.appdomain.cloud/api/v1/web/e17fb9fd-6ce8-4a0c-9841-4611c4d679f7/dealership-package/add-review-to-dealership.json'
    result = post_request(url, json_payload)
    print(result)
    return HttpResponse(result)
  else:
    return redirect('djangoapp:index')