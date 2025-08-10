from django.db import models
from django.utils.text import slugify
from .validators import validate




# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=255,validators=[validate])
    body = models.TextField()
    LIST_CATEGORY =(
        ('Jurnal','Jurnal'),
        ('Berita','Berita'),
        ('Blog','Blog')
    )
    category = models.CharField(
        max_length=20,
        default='Select',
        choices=LIST_CATEGORY,
    
    )
    slug = models.SlugField(blank=True,editable=False)

    def save(self,** kwargs):
        self.slug = slugify(self.title)
        super(Post,self).save()
    def __str__(self):
        return "{}. {}".format(self.id , self.title)



class Tara(models.Model):
    judul = models.CharField(max_length=255,blank=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.EmailField(default='default@mail.com')
    def __str__(self):
        return "{}".format(self.judul)