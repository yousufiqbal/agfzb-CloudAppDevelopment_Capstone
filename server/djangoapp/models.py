from django.db import models
from django.utils.timezone import now

class CarMake(models.Model):
  name = models.CharField(max_length=200)
  description = models.CharField(max_length=500)

  def __str__(self):
    return self.name


class CarModel(models.Model):
  TYPES = [ ('Sedan', 'Sedan'), ('SUV', 'SUV'), ('Wagon', 'Wagon'), ]
  car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
  name = models.CharField(max_length=200)
  dealer_id = models.IntegerField()
  type = models.CharField(max_length=100, choices=TYPES)
  year = models.DateField()

  def __str__(self):
    return self.name


class CarDealer:

  def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
    self.address = address
    self.city = city
    self.full_name = full_name
    self.id = id
    self.lat = lat
    self.long = long
    self.short_name = short_name
    self.st = st
    self.zip = zip

  def __str__(self):
    return "Dealer name: " + self.full_name


class DealerReview:
  
  def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
    self.dealership = dealership
    self.name = name
    self.purchase = purchase
    self.review = review
    self.purchase_date = purchase_date
    self.car_make = car_make
    self.car_model = car_model
    self.car_year = car_year
    self.sentiment = sentiment
    self.id = id

  def __str__(self):
    return "Review: " + self.review + ' Sentiment: ' + self.sentiment + '<br>'