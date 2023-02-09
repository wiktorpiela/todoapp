from django.contrib import admin
from .models import Task

class CreationDate(admin.ModelAdmin):
    readonly_fields = ("create_date",)

admin.site.register(Task, CreationDate)


