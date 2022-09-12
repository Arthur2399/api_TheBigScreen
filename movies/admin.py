from django.contrib import admin
from movies import models
# Register your models here.

admin.site.register(models.categories)
admin.site.register(models.actors)
admin.site.register(models.movies)