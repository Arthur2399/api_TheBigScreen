from django.contrib import admin
from user import models
# Register your models here.
class ImageAdmin(admin.ModelAdmin):
    verbose_name="Usuario Extension"

admin.site.register(models.image,ImageAdmin)