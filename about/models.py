from django.db import models
from .validators import validate
# Create your models here.

class AboutDb(models.Model):
    nama=models.CharField(max_length=100)
    alamat=models.CharField(max_length=10000)
    handphone=models.BigIntegerField(validators=[validate])
    SEX={
        'Man':'Man',
        'Women':'Women'
    }
    sex=models.CharField(max_length=5,choices=SEX,default='Select')
    def __str__(self):
        return "{}. {}".format(self.id , self.nama)