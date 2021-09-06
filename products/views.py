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
        page = int(request.GET["page"])

        limit = 28
        offset = (page-1)*limit 
        products = Product.objects.filter(type_id=type_id)
        
        all_rooms = list(products.values())[offset: offset+limit]  
        
        page_count = int(len(products)/limit)
        page_range = []
        for i in range(1, page_count+1):
            page_range.append(i)
    
        result = {
            "page" : page,
            "rooms" : all_rooms, 
            "page_count" : page_count,
            "page_range" : page_range,
            "total_count" : len(products),
            "products" : []
        }
        for product in products: 
            colors = product.colors.all()
            images = Image.objects.filter(product=product.id)
            result["products"].append(
                {   
                    "name" : product.name,
                    "price": product.price,
                    "colors" : list(colors.values()),
                    "colors_num" : len(list(colors.values())),
                    "img_url" : list(images.values())[:2],                        
                }
            )
        return JsonResponse({"results": result}, status=200)
        