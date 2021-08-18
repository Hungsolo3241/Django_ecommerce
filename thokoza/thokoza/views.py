from django.shortcuts import render
from django.http import JsonResponse, request
import json
import datetime
from .models import *
from .utils import *


def store_v(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    content = {"products" : products, 'cartItems': cartItems}
    return render(request, 'thokoza/store.html', content)


# def detail_v(request):
#     product = Product.objects.get(id=pk)
#     content = {'product': product}

#     return render(request, 'thokoza/detail.html', content)


def cart_v(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
            
    content = {"items": items, "order": order, 'cartItems': cartItems}
    return render(request, 'thokoza/cart.html', content)


def checkout_v(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
            
    content = {"items": items, "order": order, 'cartItems': cartItems}
    return render(request, 'thokoza/checkout.html', content)

def updateItem_v(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
     
    return JsonResponse('Item added', safe=False)

def processOrder_v(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    
    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode']
        )

    return JsonResponse('Payment Complete', safe=False)