from ebaysdk import finding
from ebaysdk.finding import Connection as finding
from ebaysdk.shopping import Connection as shopping
from bs4 import BeautifulSoup
from .models import Product, OrderedProduct, Order
from django.template.defaultfilters import random, slugify
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import dbConnectionFunctions as db
import string

APP_ID = 'ApurvPat-FindingS-PRD-ddc78fcfb-06024fa2'

def exists(list, element):
    for elem in list:
        if elem == element:
            return True
        
    return False

def find(list, element):
    index = 0
    for elem in list:
        if elem == element:
            return index
        index += 1

    return -1

def wishlist(request):
    if (request.session['isViewing']):
        org = db.getOrgNo(request.session['tempEmail'])
        email = request.session['tempEmail']
    else:
        org = request.session['orgID']
        email = request.session['email']

    id = db.getUserID(email)
    result = db.getProductsInWishlist(id, org)
    pointRate = db.getPointConversion(org)

    class Product:
        def __init__(self):
            id = -1
            name = ''
            price = ''
            pic = ''
    
    products = []

    for (id, name, price, img) in result:
        tempProduct = Product()
        tempProduct.id = id
        tempProduct.name = name
        tempProduct.price = int(price / pointRate)
        tempProduct.pic = img
        products.append(tempProduct)

    points = db.getDriverPoints(email, org)

    pic = db.getProfilePic(email)
    imgPath = 'img/' + pic

    context = {
        'points': points,
        'items': products,
        'pic': imgPath
    }
    return render(request, 'wishlist.html', context)

def driverOrderHistory(request):
    if (request.session['isViewing']):
        email = request.session['tempEmail']
        driverID = db.getUserID(request.session['tempEmail'])
        org = db.getOrgNo(request.session['tempEmail'])
    else:
        email = request.session['email']
        driverID = db.getUserID(request.session['email'])
        org = request.session['orgID']
    
    result = db.getDriverOrders(driverID, org)
    pointRate = db.getPointConversion(org)

    class Product:
        def __init__(self):
            name = ''
            price = 0
            qty = 0

    class Order:
        def __init__(self):
            id = -1
            date = '00/00/0000'
            self.totalCost = 0
            self.products = []
            status = ''

    orderIds = []
    orders = []

    for (orderID, date, productName, qty, price, status) in result:
        if (not exists(orderIds, orderID)):
            tempOrder = Order()
            tempOrder.id = orderID
            tempOrder.date = date
            tempOrder.status = status
            orders.append(tempOrder)

            orderIds.append(orderID)

        i = find(orderIds, orderID)
        tempProduct = Product()
        tempProduct.name = productName
        tempProduct.price = int(price / pointRate)
        tempProduct.qty = qty
        orders[i].products.append(tempProduct)
        orders[i].totalCost += int(price / pointRate) * qty

    pic = db.getProfilePic(email)
    imgPath = 'img/' + pic

    context = {
        'orders': orders,
        'pic': imgPath
    }        

    return render(request, 'driver_order_history.html', context)

def driverCart(request):
    if (request.session['isViewing']):
        org = db.getOrgNo(request.session['tempEmail'])
        email = request.session['tempEmail']
    else:
        org = request.session['orgID']
        email = request.session['email']

    id = db.getUserID(email)
    result = db.getProductsInCart(id, org)
    pointRate = db.getPointConversion(org)

    class Product:
        def __init__(self):
            id = -1
            name = ''
            price = ''
            pic = ''
    
    products = []

    for (id, name, price, img) in result:
        tempProduct = Product()
        tempProduct.id = id
        tempProduct.name = name
        tempProduct.price = int(price / pointRate)
        tempProduct.pic = img
        products.append(tempProduct)

    points = db.getDriverPoints(email, org)

    pic = db.getProfilePic(email)
    imgPath = 'img/' + pic

    context = {
        'points': points,
        'items': products,
        'pic': imgPath
    }
    return render(request, 'driver_cart.html', context)

def checkout(request):
    if (request.session['isViewing']):
        email = request.session['tempEmail']
        org = db.getOrgNo(email)
    else:
        email = request.session['email']
        org = request.session['orgID']
    
    points = db.getDriverPoints(email, org)
    driver_id = db.getUserID(email)
    driver_order = db.getDriverOrders(driver_id, org)
    
    defaultAddr = db.getDefaultAddress(email)

    result = db.getDriverAddresses(email)

    class Addr:
        def __init__(self):
            id = -1
            addr = ''
    
    addresses = []

    for (id, address) in result:
        if address == defaultAddr:
            tempAddr = Addr()
            tempAddr.id = id
            tempAddr.addr = address
            addresses.append(tempAddr)

    pic = db.getProfilePic(email)
    imgPath = 'img/' + pic

    class Order:
        def __init__(self):
            id = -1
            date = ''
            name = ''
            qty = ''
            price = 0.0

    order = []
    pointRate = db.getPointConversion(org)

    for(id, o_date, name, qty, price) in driver_order:
        tempOrder = Order()
        tempOrder.id = id
        tempOrder.date = o_date
        tempOrder.name = name
        tempOrder.qty = qty
        tempOrder.price = int(price / pointRate)
        order.append(tempOrder)
        

    context = {
        'points': points,
        'default': defaultAddr,
        'addresses': addresses,
        'order': order,
        'pic': imgPath
    }
    return render(request, 'checkout.html', context)

def productPage(request, id):
    if (request.session['isViewing']):
        email = request.session['tempEmail']
        org = db.getOrgNo(email)
    else:
        email = request.session['email']
        org = request.session['orgID']
    
    driverId = db.getUserID(email)
    points = db.getDriverPoints(email, org)
    pointRate = db.getPointConversion(org)

    class Product:
        def __init__(self):
            id = -1
            name = ''
            price = 0
            pic = ''

    result = db.getProduct(id)

    product = Product()
    product.id = id
    product.name = result[0]
    product.price = int(result[1] / pointRate)
    product.pic = result[2]

    inCart = db.checkIsInCart(driverId, org, id)

    if inCart:
        qty = db.getQuantity(driverId, org, id)
    else:
        qty = 0

    pic = db.getProfilePic(email)
    imgPath = 'img/' + pic

    context = {
        'points': points,
        'product': product,
        'isSponsor': request.session['isSponsor'],
        'isAdmin': request.session['isAdmin'],
        'pic': imgPath,
        'inCart': inCart,
        'qty': qty
    }

    return render(request, 'product.html', context)

def addProducts(request):
    api = finding(appid = APP_ID, config_file = None)

    if request.session['isViewing']:
        orgNo = db.getOrgNo(request.session['tempEmail'])
    else:
        orgNo = db.getOrgNo(request.session['email'])

    result = db.getKeywords(orgNo)
    keywords = []

    for (id, keyword) in result:
        keywords.append(keyword)
    
    apiRequest = {'keywords': keywords, 'outputSelector': 'SellerInfo',}
    apiResponse = api.execute('findItemsByKeywords', apiRequest)
    soup = BeautifulSoup(apiResponse.content, 'lxml')
    #entries = int (soup.find('totalentries').text)
    items = soup.find_all('item')

    db.clearCatalog(orgNo)
    
    for item in items:
        id_temp = item.itemid.string
        name_tmp = item.title.string
        price_tmp = float(item.currentprice.string)
        image_tmp = item.galleryurl.string
        db.createProduct(id_temp, name_tmp, price_tmp, image_tmp)

        db.addToCatalog(id_temp, orgNo)
        #cat = item.categoryname.string.lower()
        # Product.objects.create(name = name_tmp, price = price_tmp, image = image_tmp)

def product_list(request):
    if (request.session['isViewing']):
        org = db.getOrgNo(request.session['tempEmail'])
        email = request.session['tempEmail']
    else:
        org = request.session['orgID']
        email = request.session['email']

    result = db.getProductsInCatalog(org)
    pointRate = db.getPointConversion(org)

    class Product:
        def __init__(self):
            id = -1
            name = ''
            price = ''
            pic = ''
    
    products = []

    for (id, name, price, img) in result:
        tempProduct = Product()
        tempProduct.id = id
        tempProduct.name = name
        tempProduct.price = int(price / pointRate)
        tempProduct.pic = img
        products.append(tempProduct)

    points = db.getDriverPoints(email, org)

    pic = db.getProfilePic(email)
    imgPath = 'img/' + pic

    context = {
        'points': points,
        'items': products,
        'pic': imgPath
    }
    return render(request, "driver_catalog.html", context)

def sponsor_catalog(request):
    if (request.session['isViewing']):
        email = request.session['tempEmail']
        org = db.getOrgNo(request.session['tempEmail'])
    else:
        email = request.session['email']
        org = db.getOrgNo(request.session['email'])

    result = db.getProductsInCatalog(org)

    class Product:
        def __init__(self):
            id = -1
            name = ''
            price = ''
            pic = ''
    
    products = []

    for (id, name, price, img) in result:
        tempProduct = Product()
        tempProduct.id = id
        tempProduct.name = name
        tempProduct.price = price
        tempProduct.pic = img
        products.append(tempProduct)

    pic = db.getProfilePic(email)
    imgPath = 'img/' + pic

    context = {
        'items': products,
        'pic': imgPath
    }
    return render(request, "sponsor_catalog.html", context)

def createCatalog(request):
    #call add products here to create catalog
    pass

def add_to_cart(request, id):
    if (request.session['isViewing']):
        email = request.session['tempEmail']
        org = db.getOrgNo(request.session['email'])
    else:
        email = request.session['email']
        org = request.session['orgID']

    driverID = db.getUserID(email)
    inCart = db.checkIsInCart(driverID, org, id)

    if inCart:
        newQty = request.POST.get('qty')
        db.updateQuantityInCart(driverID, org, id, newQty)
    else:
        db.addToCart(driverID, org, id, 1)

    return product_list(request)
    # item = get_object_or_404(Product, slug=slug)
    # order_item, created = OrderedProduct.objects.get_or_create(
    #     item=item,
    #     user=request.user,
    #     ordered=False
    # )
    # order_qs = Order.objects.filter(user=request.user, ordered=False)
    # if order_qs.exists():
    #     order = order_qs[0]
    #     # check if the order item is in the order
    #     if order.items.filter(item__slug=item.slug).exists():
    #         order_item.quantity += 1
    #         order_item.save()
    #         messages.info(request, "This item quantity was updated.")
    #         return redirect("Catalog:driver_cart")
    #     else:
    #         order.items.add(order_item)
    #         messages.info(request, "This item was added to your cart.")
    #         return redirect("Catalog:driver_cart")
    # else:
    #     ordered_date = timezone.now()
    #     order = Order.objects.create(
    #         user=request.user, ordered_date=ordered_date)
    #     order.items.add(order_item)
    #     messages.info(request, "This item was added to your cart.")
    #     return redirect("Catalog:driver_cart")



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
