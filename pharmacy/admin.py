from django.contrib import admin
from .models import Category, Medicine, Cart, Order, OrderItem, RefillReminder


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'featured', 'requires_prescription']
    list_filter = ['category', 'featured', 'requires_prescription']
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock', 'featured']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['medicine', 'quantity', 'price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'shipping_address']
    list_editable = ['status']
    inlines = [OrderItemInline]


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'medicine', 'quantity', 'created_at']
    list_filter = ['created_at']


@admin.register(RefillReminder)
class RefillReminderAdmin(admin.ModelAdmin):
    list_display = ['user', 'medicine_name', 'reminder_date', 'is_active']
    list_filter = ['is_active', 'reminder_date']
    search_fields = ['medicine_name', 'user__username']
