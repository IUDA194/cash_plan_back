from django.contrib import admin
from plans.models import Operation

from unfold.admin import ModelAdmin


@admin.register(Operation)
class CustomAdminClass(ModelAdmin):
    pass
