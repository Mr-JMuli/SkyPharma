from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from .models import Category, Medicine, Cart, Order, OrderItem, RefillReminder
from .forms import UserRegistrationForm, MedicineForm, RefillReminderForm, CheckoutForm


def home(request):
    categories = Category.objects.all()[:6]
    featured_medicines = Medicine.objects.filter(featured=True)[:8]
    context = {
        'categories': categories,
        'featured_medicines': featured_medicines,
    }
    return render(request, 'pharmacy/home.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Skypharma.')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def medicine_list(request, category_id=None):
    medicines = Medicine.objects.all()
    categories = Category.objects.all()
    current_category = None
    
    if category_id:
        current_category = get_object_or_404(Category, id=category_id)
        medicines = medicines.filter(category=current_category)
    
    context = {
        'medicines': medicines,
        'categories': categories,
        'current_category': current_category,
    }
    return render(request, 'pharmacy/medicine_list.html', context)


def medicine_detail(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    related_medicines = Medicine.objects.filter(category=medicine.category).exclude(pk=pk)[:4]
    context = {
        'medicine': medicine,
        'related_medicines': related_medicines,
    }
    return render(request, 'pharmacy/medicine_detail.html', context)


def search_medicines(request):
    query = request.GET.get('q', '')
    medicines = Medicine.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    ) if query else Medicine.objects.none()
    
    context = {
        'medicines': medicines,
        'query': query,
    }
    return render(request, 'pharmacy/search_results.html', context)


@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user).select_related('medicine')
    total = sum(item.total_price for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'pharmacy/cart.html', context)


@login_required
def add_to_cart(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)
    
    cart_item = Cart.objects.filter(user=request.user, medicine=medicine).first()
    current_cart_qty = cart_item.quantity if cart_item else 0
    
    if current_cart_qty + 1 > medicine.stock:
        messages.error(request, f'Sorry, only {medicine.stock} units of {medicine.name} are available.')
        return redirect(request.META.get('HTTP_REFERER', 'medicine_list'))
    
    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        Cart.objects.create(user=request.user, medicine=medicine, quantity=1)
    
    messages.success(request, f'{medicine.name} added to cart!')
    return redirect(request.META.get('HTTP_REFERER', 'medicine_list'))


@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        if quantity > cart_item.medicine.stock:
            messages.error(request, f'Sorry, only {cart_item.medicine.stock} units of {cart_item.medicine.name} are available.')
            return redirect('cart')
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, 'Cart updated.')
    else:
        cart_item.delete()
        messages.success(request, 'Item removed from cart.')
    return redirect('cart')


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('cart')


@login_required
def checkout(request):
    from django.db import transaction
    
    cart_items = Cart.objects.filter(user=request.user).select_related('medicine')
    if not cart_items:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart')
    
    stock_errors = []
    for item in cart_items:
        if item.quantity > item.medicine.stock:
            stock_errors.append(f'{item.medicine.name} (requested: {item.quantity}, available: {item.medicine.stock})')
    
    if stock_errors:
        messages.error(request, f'Insufficient stock for: {", ".join(stock_errors)}. Please update your cart.')
        return redirect('cart')
    
    total = sum(item.total_price for item in cart_items)
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    for item in cart_items:
                        medicine = Medicine.objects.select_for_update().get(pk=item.medicine.pk)
                        if item.quantity > medicine.stock:
                            raise ValueError(f'Insufficient stock for {medicine.name}')
                    
                    order = Order.objects.create(
                        user=request.user,
                        total_amount=total,
                        shipping_address=form.cleaned_data['shipping_address'],
                        phone=form.cleaned_data['phone'],
                        notes=form.cleaned_data.get('notes', ''),
                    )
                    
                    for item in cart_items:
                        medicine = Medicine.objects.select_for_update().get(pk=item.medicine.pk)
                        OrderItem.objects.create(
                            order=order,
                            medicine=medicine,
                            quantity=item.quantity,
                            price=medicine.price,
                        )
                        medicine.stock -= item.quantity
                        medicine.save()
                    
                    cart_items.delete()
                
                messages.success(request, 'Order placed successfully!')
                return redirect('order_confirmation', order_id=order.id)
            except ValueError as e:
                messages.error(request, str(e))
                return redirect('cart')
    else:
        form = CheckoutForm()
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'form': form,
    }
    return render(request, 'pharmacy/checkout.html', context)


@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'pharmacy/order_confirmation.html', {'order': order})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'pharmacy/order_list.html', {'orders': orders})


@login_required
def order_tracking(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'pharmacy/order_tracking.html', {'order': order})


@login_required
def refill_reminders(request):
    reminders = RefillReminder.objects.filter(user=request.user, is_active=True)
    upcoming = reminders.filter(reminder_date__gte=timezone.now().date()).order_by('reminder_date')
    context = {
        'reminders': reminders,
        'upcoming': upcoming,
    }
    return render(request, 'pharmacy/refill_reminders.html', context)


@login_required
def add_reminder(request):
    if request.method == 'POST':
        form = RefillReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.user = request.user
            reminder.save()
            messages.success(request, 'Refill reminder added!')
            return redirect('refill_reminders')
    else:
        form = RefillReminderForm()
    return render(request, 'pharmacy/add_reminder.html', {'form': form})


@login_required
def delete_reminder(request, reminder_id):
    reminder = get_object_or_404(RefillReminder, id=reminder_id, user=request.user)
    reminder.delete()
    messages.success(request, 'Reminder deleted.')
    return redirect('refill_reminders')


def is_admin(user):
    return user.is_staff


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    total_users = User.objects.count()
    total_orders = Order.objects.count()
    total_medicines = Medicine.objects.count()
    total_sales = Order.objects.filter(status='delivered').aggregate(
        total=Sum('total_amount'))['total'] or 0
    
    recent_orders = Order.objects.all()[:5]
    low_stock = Medicine.objects.filter(stock__lt=10)[:5]
    
    context = {
        'total_users': total_users,
        'total_orders': total_orders,
        'total_medicines': total_medicines,
        'total_sales': total_sales,
        'recent_orders': recent_orders,
        'low_stock': low_stock,
    }
    return render(request, 'pharmacy/admin/dashboard.html', context)


@login_required
@user_passes_test(is_admin)
def admin_medicines(request):
    medicines = Medicine.objects.all()
    return render(request, 'pharmacy/admin/medicines.html', {'medicines': medicines})


@login_required
@user_passes_test(is_admin)
def admin_add_medicine(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Medicine added successfully!')
            return redirect('admin_medicines')
    else:
        form = MedicineForm()
    return render(request, 'pharmacy/admin/medicine_form.html', {'form': form, 'action': 'Add'})


@login_required
@user_passes_test(is_admin)
def admin_edit_medicine(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        form = MedicineForm(request.POST, request.FILES, instance=medicine)
        if form.is_valid():
            form.save()
            messages.success(request, 'Medicine updated successfully!')
            return redirect('admin_medicines')
    else:
        form = MedicineForm(instance=medicine)
    return render(request, 'pharmacy/admin/medicine_form.html', {'form': form, 'action': 'Edit'})


@login_required
@user_passes_test(is_admin)
def admin_delete_medicine(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        medicine.delete()
        messages.success(request, 'Medicine deleted successfully!')
        return redirect('admin_medicines')
    return render(request, 'pharmacy/admin/medicine_confirm_delete.html', {'medicine': medicine})


@login_required
@user_passes_test(is_admin)
def admin_orders(request):
    orders = Order.objects.all()
    return render(request, 'pharmacy/admin/orders.html', {'orders': orders})


@login_required
@user_passes_test(is_admin)
def admin_update_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f'Order #{order.id} status updated to {order.get_status_display()}')
    return redirect('admin_orders')


@login_required
@user_passes_test(is_admin)
def admin_users(request):
    users = User.objects.all()
    return render(request, 'pharmacy/admin/users.html', {'users': users})
