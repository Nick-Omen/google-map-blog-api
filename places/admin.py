from django.contrib import admin
from places.models import Place


class PlaceAdmin(admin.ModelAdmin):
    exclude = ['slug']


admin.site.register(Place, PlaceAdmin)
