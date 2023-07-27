from django.contrib import admin

from .models import Player, Events, Coach, Payment

# Register your models here.

admin.site.register(Player)
admin.site.register(Events)
admin.site.register(Coach)
admin.site.register(Payment)
