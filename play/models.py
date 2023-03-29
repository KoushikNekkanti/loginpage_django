from django.db import models
from django.contrib.auth.models import User

class To_do(models.Model):
  
    add_date = models.DateTimeField()
    text = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
 
class Note(models.Model):
    add_date = models.DateTimeField()
    text = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
 

    
