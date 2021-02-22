from django.shortcuts import render
from ebaysdk.finding import Connection as Finding
from Catalog.models import Product, SearchWord
from django.shortcuts import render
from django.template.defaultfilters import slugify, wordcount
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
