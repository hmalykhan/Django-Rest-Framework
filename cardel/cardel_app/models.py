from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

def alphanumeric(value):
        if not str(value).isalnum():
            raise ValidationError("Only alphanumeric characters are allowed.") 
        
# Models are the coding representation of tables in databases we can create, alter and make relations of tables throug models.
# Migration is chainging the database instance at schema level thorugh code in programming language and versioning.

class ShowRoomList(models.Model):
     name = models.CharField(max_length=100)
     location = models.CharField(max_length=100)
     website = models.URLField(max_length=100)

     def __str__(self):
          return self.name 
        
class CarList(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    active = models.BooleanField(default=False)
    chassisnumber = models.CharField(max_length=100, null=True, blank=True, validators=[alphanumeric])
    price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    showroom = models.ForeignKey(ShowRoomList, on_delete=models.CASCADE, related_name="Showrooms", null=True )

    def __str__(self):
          return self.name 
    
class Review(models.Model):
     apiuser = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
     rating = models.IntegerField(validators=[MinValueValidator, MaxValueValidator])
     comments = models.CharField(max_length=200, null=True )
     car = models.ForeignKey(CarList, on_delete=models.CASCADE, related_name="Reviews", null=True)
     created = models.DateTimeField(auto_now_add=True)
     updated = models.DateTimeField(auto_now=True)
     
     def __str__(self):
          return f"""the rating of the car {self.car.name} is {self.rating}."""