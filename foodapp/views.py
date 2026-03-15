from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import FoodItem, Order


# MENU PAGE
def menu(request):
    foods = FoodItem.objects.all()
    return render(request, 'menu.html', {'foods': foods})


# ADD TO CART
def add_to_cart(request, food_id):
    cart = request.session.get('cart', {})

    if str(food_id) in cart:
        cart[str(food_id)] += 1
    else:
        cart[str(food_id)] = 1

    request.session['cart'] = cart
    return redirect('menu')


# VIEW CART
def view_cart(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0

    for food_id, quantity in cart.items():
        food = FoodItem.objects.get(id=food_id)
        subtotal = food.price * quantity
        total += subtotal

        items.append({
            'food': food,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'cart.html', {'items': items, 'total': total})


# PLACE ORDER
@login_required
def place_order(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('menu')

    if request.method == 'POST':
        pickup_time = request.POST.get('pickup_time')
        pickup_time = datetime.strptime(pickup_time, "%Y-%m-%dT%H:%M")

        total = 0
        for food_id, quantity in cart.items():
            food = FoodItem.objects.get(id=food_id)
            total += food.price * quantity

        Order.objects.create(
            user=request.user,
            total_price=total,
            pickup_time=pickup_time,
            status="Confirmed"
        )

        # Clear cart after order

        request.session['cart'] = {}

        return redirect('menu')

    return render(request, 'place_order.html')

# ======================
# CLEAR CART
# ======================
def clear_cart(request):
    request.session['cart'] = {}
    return redirect('view_cart')