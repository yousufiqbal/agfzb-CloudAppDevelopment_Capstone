from django.db import models
from django.utils.timezone import now


# Create your models here.

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


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
