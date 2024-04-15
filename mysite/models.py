from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.
class User(models.Model):
	username = models.CharField(max_length=20)

class Zip(models.Model):
	user = models.ForeignKey(User, on_delete=CASCADE)
	code = models.IntegerField()
	temp = models.CharField(max_length=6)