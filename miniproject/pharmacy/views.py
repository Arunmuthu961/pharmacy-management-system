from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from pharmacy.models import Medicine, Cart, Prescription
from pharmacy.forms import RegisterForm, LoginForm

# Home Page
@login_required
def home(request):
    return render(request, 'pharmacy/home.html')
# Register
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                login(request, user)
                print("User created successfully:", username)
                return redirect('home')
            except Exception as e:
                print("Error while creating user:", e)
                return render(request, 'pharmacy/register.html', {
                    'form': form,
                    'error': 'Something went wrong while saving. Please try again.'
                })
    else:
        form = RegisterForm()
    
    return render(request, 'pharmacy/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('home')
        return render(request, 'pharmacy/login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = LoginForm()
    return render(request, 'pharmacy/login.html', {'form': form})

# Logout
def logout_view(request):
    logout(request)
    return render(request, 'pharmacy/logout.html')

# Medicine Detail View
@login_required
def medicine_detail(request, id):
    medicine = get_object_or_404(Medicine, id=id)
    return render(request, 'pharmacy/medicine_detail.html', {'medicine': medicine})

# Add to Cart
@login_required
def add_to_cart(request, id):
    medicine = get_object_or_404(Medicine, id=id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, medicine=medicine)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

# ✅ View Cart Page (Corrected version)
@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)

    # Add subtotal to each item
    for item in cart_items:
        item.subtotal = item.medicine.price * item.quantity

    total_price = sum(item.subtotal for item in cart_items)

    return render(request, 'pharmacy/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })


# Remove item from cart
@login_required
def remove_cart(request, id):
    item = get_object_or_404(Cart, id=id, user=request.user)
    item.delete()
    return redirect('cart')

# Checkout Page
@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.medicine.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        if cart_items.exists():
            from pharmacy.models import Order, OrderItem
            order = Order.objects.create(user=request.user, total_amount=total_price)
            for item in cart_items:
                OrderItem.objects.create(order=order, medicine=item.medicine, quantity=item.quantity)
            cart_items.delete()
        return render(request, 'pharmacy/order_success.html')

    return render(request, 'pharmacy/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

# Upload Prescription
@login_required
def upload_prescription(request):
    if request.method == 'POST' and request.FILES.get('image'):
        Prescription.objects.create(user=request.user, image=request.FILES['image'])
        messages.success(request, 'Prescription uploaded successfully.')
        return redirect('home')
    return render(request, 'pharmacy/upload_prescription.html')

# Update Cart Quantity
@require_POST
@login_required
def update_cart(request, id):
    cart_item = get_object_or_404(Cart, id=id, user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')
@login_required
def medicine_list(request):
    medicines = Medicine.objects.all()
    return render(request, 'pharmacy/medicine_list.html', {'medicines': medicines})

