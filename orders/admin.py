from django.contrib import admin

from .models import Order, OrderItem

admin.site.register(OrderItem)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'created', 'dispatch_status', 'full_name', 'email']
    list_filter = ['created']
    list_editable = ['dispatch_status']
    list_per_page = 10
    inlines = [
        OrderItemInline,
    ]