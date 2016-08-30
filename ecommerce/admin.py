from django.contrib import admin
from .models import NonMediaItem

# Register your models here.

class NonMediaItemAdmin(admin.ModelAdmin):
    pass


admin.site.register(NonMediaItem, NonMediaItemAdmin)