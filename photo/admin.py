from django.contrib import admin
from photo.models import Image


class ImageAdmin(admin.ModelAdmin):
    exclude = []


admin.site.register(Image, ImageAdmin)
