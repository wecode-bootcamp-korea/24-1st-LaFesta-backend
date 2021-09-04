import json

from django.http import JsonResponse
from django.views import View

from .models import Product, Image


class ProductDetailView(View):
    def get(self, request, **kwargs):
        product = Product.objects.get(id=kwargs["product_id"])
        colors = product.colors.all()
        sizes = product.sizes.all()
        images = product.image_set.all()

        result = {
            "name": product.name,
            "price": product.price,
            "section": product.type.category.section.name,
            "category": product.type.category.name,
            "type": product.type.name,
            "fit": product.fit.name,
            "description_summary": product.description.summary,
            "description_extra_information": product.description.extra_information,
            "colors": list(colors.values()),
            "sizes": list(sizes.values()),
            "images": list(images.values()),
        }

        return JsonResponse({"results": result}, status=200)

class ProductListView(View):
    def get(self, request): 
        type_id = request.GET["typeId"]
        
        page = request.Get["page"]
        limit = 28
        offset = (page-1)*limit
        
        products = Product.objects.filter(type_id=type_id)
        
        rooms = products[offset: offset+limit]
        page_count = len(products)//limit
        page_range = range(1, page_count+1)
        
        result = {
            "page"        : page,
            "rooms"       : rooms,
            "page_count"  : page_count,
            "page_range"  : page_range,

            "total_count" : len(products),
            "products"    : []
        }
        
        for product in products:
            colors = product.colors.all()
            fits = product.fits.all()
            images = Image.objects.filter(product=product.id)

            result["products"].append(
                {   
                    "name"      : product.name,
                    "price"     : product.price,
                    "color_num" : len(list(colors.value())),
                    "colors"    : list(colors.value()),
                    "fits"      : list(fits.values()),
                    "img_url"   : list(images.values())[:2],                        
                }
            )
        return JsonResponse({"results": result}, status=200)