from django.contrib import admin
from .models import Car, CarImage


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 3


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'brand', 'condition', 'year', 'price')
    list_filter = ('condition', 'year', 'fuel_type')
    search_fields = ('model_name', 'brand')
    inlines = [CarImageInline]