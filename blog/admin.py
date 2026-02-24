from django.contrib import admin

# Register your models here.

from .models import Post,Tara

class PostAdmin(admin.ModelAdmin):
    readonly_fields = ['slug',]

admin.site.register([Post,Tara])