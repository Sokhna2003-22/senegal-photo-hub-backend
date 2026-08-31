from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['client', 'photographer', 'service_type', 'status', 'event_date', 'price']
    list_filter = ['status', 'service_type']
    search_fields = ['client__username', 'photographer__username']
    list_editable = ['status', 'price']