from django.db import models

# Create your models here.
class List(models.Model):
    text = models.TextField()


class Item(models.Model):
    text = models.TextField()
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    



        
    

    