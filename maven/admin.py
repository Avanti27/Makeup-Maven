from django.contrib import admin

# Register your models here.

from maven.models import Products
class productAdmin(admin.ModelAdmin):
    list_display = ["price","category", "is_active"]
    list_filter = ["category", "is_active"]


admin.site.register(Products, productAdmin)
