from django.shortcuts import render
from ebaysdk.finding import Connection as Finding
from .models import OrderedProduct, Product, SearchWord, Order
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import slugify, wordcount
from django.contrib import messages
from django.utils import timezone
import random
# Create your views here.

APP_ID = 'ApurvPat-FindingS-SBX-1b1a1f9b6-dfc400b9'

def createCatalog(words, SearchWords, request):
    api = Finding(id = APP_ID, config=None, http=True)
    response = api.execute('fAdvanced', {'SearchWord': wordcount, 'input':[{'EntriesPerPAge':50}]})
    prds = response.dic()
    prds = prds["SearchResult"]

    for prd in prds["Product"]:
        slug = slugify(prd["Name"])
        num = random.randint(1, 10000)
        slug += str(num)
        try:
            Product.objects.create(Name=prd["Name"], Price=float(prd["sellingStatus"]["convertedCurrentPrice"]["value"]), Img=prd["galleryURL"], slug=slug, keyWord=SearchWord)
        except:
            Product.objects.create(Name=prd["Name"], Price=float(prd["sellingStatus"]["convertedCurrentPrice"]["value"]), Img=prd["galleryURL"], slug=slug, keyWord=SearchWord)

def Catalog(request):
    all = []
    for i in range(0, 50):
        for j in range(0, SearchWord.object.all().count()):
            all.append(Product.objects.all()[(j*50)+i])
    return render(request, 'driver_catalog.html', {'all':all})

def addToCart(request, slug):
    prd = get_object_or_404(Product, slug=slug)
    orderItem, created = OrderedProduct.objects.get_or_create(item=prd, user = request.user, ordered=False)
    orderSet = Order.objects.filter(user=request.user, ordered=False)
    if orderSet.exists():
        order = orderSet[0]
        if order.items.filter(item__slug=prd.slug).exists():
            orderItem.quantity += 1
            orderItem.save()
            messages.info(request, "Quantity updated")
            return redirect("catalog:checkoutPage")
        else:
            messages.info(request, "Item added to cart")
            order.items.add(orderItem)
            return redirect("catalog:checkoutPage")
    else:
        order = Order.objects.create(user=request.user, orderDate=timezone.now())
        order.Products.add(orderItem)
        messages.info(request, "Item added to cart")
        return redirect("catalog:checkoutPage")

def removeFromCart(request, slug):
    prd = get_object_or_404(Product, slug=slug)
    orderSet = Order.objects.filter(user=request.user, ordered=False)
    if orderSet.exists():
        order = orderSet[0]
        if order.items.filter(item__slug=prd.slug).exists():
            orderItem = OrderedProduct.objects.filter(item=prd, user=request.user, ordered=False)[0]
            if orderItem.quantity > 1:
                orderItem.quantity -= 1
                orderItem.save()
                messages.info(request, "Item quantity updated")
                return redirect("catalog:checkoutPage")
            else:
                orderItem.quantity -= 1
                order.items.remove(orderItem)
                orderItem.delete()
                messages.info(request, "Item removed from cart")
                return redirect("catalog:checkoutPage")
        else:
            messages.info(request, "Item not in cart")
            return redirect("catalog:checkoutPage")
    else:
        messages.info(request, "No valid active order")
        return redirect("catalog:checkoutPage")