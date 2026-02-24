from django.db import models
from django.utils.text import slugify
from .validators import validate
from django.utils import timezone
import pytz


class Country(models.Model):
    name = models.CharField(max_length=100)
    timezone = models.CharField(max_length=50)  # e.g., "Asia/Jakarta", "America/New_York"


    def __str__(self):
        return self.name

class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="cities")
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


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

    # New columns
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        """
        Custom save to set created_at and updated_at based on country's timezone
        """
        # Determine timezone
        if self.country and self.country.timezone:
            tz = pytz.timezone(self.country.timezone)
        else:
            tz = timezone.get_current_timezone()  # fallback to project default

        now_in_country_tz = timezone.now().astimezone(tz)

        # If it's a new record, set created_at
        if not self.id:
            self.created_at = now_in_country_tz

        # Always update updated_at
        self.updated_at = now_in_country_tz
        super().save(*args, **kwargs)
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