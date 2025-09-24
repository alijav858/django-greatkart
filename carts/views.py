from django.shortcuts import render, redirect
from store.models import Product
from .models import Cart,CartItems
from django.core.exceptions import ObjectDoesNotExist

def _cart_id(request):
    cart = request.session.session_key

    if not cart:
        cart = request.session.create()

    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )    
    cart.save()    

    try:
        cart_items = CartItems.objects.get(product=product, cart=cart)
        cart_items.quantity += 1
        cart_items.save()

    except CartItems.DoesNotExist:
        cart_items = CartItems.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )    

    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItems.objects.filter(cart=cart, is_active=True)
        for items in cart_items:
            total += (items.product.price * items.quantity)
            quantity += items.quantity

    except ObjectDoesNotExist:
        cart_items=[]

    return render(request, 'store/cart.html', {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items})
# Create your views here.


