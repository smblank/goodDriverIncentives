from ebaysdk import finding
from ebaysdk.finding import Connection as finding
from bs4 import BeautifulSoup
from .models import Product, OrderedProduct, Order
from django.template.defaultfilters import random, slugify
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail

APP_ID = 'ApurvPat-FindingS-PRD-ddc78fcfb-06024fa2'

def driverCatalog(request):
    return render(request, 'driver_catalog.html')

def wishlist(request):
    return render(request, 'wishlist.html')

def driverOrderHistory(request):
    return render(request, 'driver_order_history.html')

def sponsorCatalog(request):
    return render(request, 'sponsor_catalog.html')

def driverCart(request):
    return render(request, 'driver_cart.html')

def addProducts(request):
    api = finding(appid = APP_ID, config_file = None)
    request = {'keywords': {'TV', 'Computer', 'Phone'}, 'outputSelector': 'SellerInfo',}
    response = api.execute('findItemsByKeywords', request)
    soup = BeautifulSoup(response.content, 'lxml')
    #entries = int (soup.find('totalentries').text)
    items = soup.find_all('item')
    
    for item in items:
        name_tmp = item.title.string.lower().strip()
        price_tmp = float(item.currentprice.string)
        image_tmp = item.viewitemurl.string.lower()
        #cat = item.categoryname.string.lower()
        Product.objects.create(name = name_tmp, price = price_tmp, image = image_tmp)

def product_list(request):
    context = {
        'items': Product.objects.all()
    }
    return render(request, "driver_catalog.html", context)

def sponsor_catalog(request):
    context = {
        'items': Product.objects.all()
    }
    return render(request, "sponsor_catalog.html", context)

def createCatalog(request):
    #call add products here to create catalog
    pass

def add_to_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_item, created = OrderedProduct.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("Catalog:driver_cart")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("Catalog:driver_cart")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("Catalog:driver_cart")

def remove_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderedProduct.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("Catalog:driver_cart")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("Catalog:driver_cart", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("Catalog:driver_cart", slug=slug)

def checkoutPage(request):
    firstName = request.GET.get('firstName')
    lastName = request.GET.get('lastName')
    email = request.GET.get('email')
    address = request.GET.get('address')
    address2 = request.GET.get('address2')
    country = request.GET.get('country')
    state = request.GET.get('state')
    zipCode = request.GET.get('zipCode')
    sum = 0
    itemStr ='Thank you for your purchase, ' + firstName + '\n\n'
    itemStr = itemStr + firstName + ' ' + lastName + '\n'
    itemStr = itemStr + address + '\n'
    if address2 != '':
        itemStr = itemStr + address2 + '\n'
    itemStr = itemStr + state + ', ' + country + '\n'
    itemStr = itemStr + zipCode + '\n' + '\n'
    items = Order.objects.filter(user=request.user, ordered=False)
    for item in items[0].items.all():
        sum += item.item.price*item.quantity
        itemStr += item.item.title + '\t'
        itemStr += str(item.item.price)
        itemStr += '\n'
    
    itemStr = itemStr + "\nTotal Cost: " + str(sum)

    order = Order.objects.filter(user=request.user, ordered=False)[0]
    order.ordered = True
    order.save()
    for item in order.items.all():
        print(item.item.title)
        item.ordered = True
        item.save()
    return redirect("catalog:catalog")

def cancelOrder(request, pk):
    sum = 0
    order = Order.objects.filter(user=request.user, pk=pk, ordered=True)[0]
    itemStr ='Hi, ' + request.user.username + '\n\n' + 'You cancelled your order #' + str(pk) + '.\nPlease find the details of your refund below.\n\n'
    for item in order.items.all():
        itemStr+= item.item.title + '\t' + str(item.quantity) + '\n'
        sum += item.item.price*item.quantity


    itemStr += '\nTotal Refund: ' + str(sum)

    subj = 'Order #' + str(pk) + ' Cancellation'

    order.delete()
    message = 'Order ' + str(pk + ' successfully cancelled')
    messages.info(request, message)
    return redirect("catalog:pastOrders")
