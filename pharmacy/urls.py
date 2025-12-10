from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    
    path('medicines/', views.medicine_list, name='medicine_list'),
    path('medicines/category/<int:category_id>/', views.medicine_list, name='medicine_by_category'),
    path('medicines/<int:pk>/', views.medicine_detail, name='medicine_detail'),
    path('search/', views.search_medicines, name='search_medicines'),
    
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:medicine_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    path('checkout/', views.checkout, name='checkout'),
    path('order/confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/', views.order_tracking, name='order_tracking'),
    
    path('reminders/', views.refill_reminders, name='refill_reminders'),
    path('reminders/add/', views.add_reminder, name='add_reminder'),
    path('reminders/delete/<int:reminder_id>/', views.delete_reminder, name='delete_reminder'),
    
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/medicines/', views.admin_medicines, name='admin_medicines'),
    path('dashboard/medicines/add/', views.admin_add_medicine, name='admin_add_medicine'),
    path('dashboard/medicines/edit/<int:pk>/', views.admin_edit_medicine, name='admin_edit_medicine'),
    path('dashboard/medicines/delete/<int:pk>/', views.admin_delete_medicine, name='admin_delete_medicine'),
    path('dashboard/orders/', views.admin_orders, name='admin_orders'),
    path('dashboard/orders/<int:order_id>/update/', views.admin_update_order, name='admin_update_order'),
    path('dashboard/users/', views.admin_users, name='admin_users'),
]
