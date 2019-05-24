from django.db import models

# Create your models here.
class Station(models.Model):
    name = models.CharField(max_length=200)
  
    def __str__(self):
        return self.name

class TableIndex(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class TableBasic(models.Model):
    row = models.ForeignKey(TableIndex, on_delete=models.CASCADE)
    left_campus = models.TimeField(auto_now=False)
    arrive_station = models.TimeField(auto_now=False)
    arrive_campus = models.TimeField(auto_now=False)