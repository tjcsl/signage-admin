from django.contrib import admin

from . import models

# Register your models here.

class SignAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Sign, SignAdmin)
