import json
import math

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
        try:
            type_id = request.GET.get("typeId", None)
            page = int(request.GET.get("page", 1))
            
            limit = 28
            offset = (page-1)*limit

            products = Product.objects.filter(type_id=type_id)
            all_rooms = list(products.values())[offset: offset+limit]
            page_count = math.ceil(len(products)/limit)
            
            result = {
                "page"        : page,
                "page_count"  : page_count,
                "rooms"       : all_rooms, 
                "total_count" : len(products),
                "products"    : []
            }
            
            products = products[offset: offset+limit]
            for product in products: 
                images = product.image_set.filter(product = product.id)
                
                result["products"].append(
                    {   
                        "name"       : product.name,
                        "price"      : product.price,
                        "colors"     : list(product.colors.all().values()),
                        "colors_num" : len(list(product.colors.values())),
                        "fit"        : product.fit.name,
                        "img_url"    : list(images.values())[:2],                        
                    }
                )
            return JsonResponse({"results": result}, status=200)
        
        except KeyError:
            return JsonResponse({'MESSAGE':'Page Does Not Exists'}, status=404)


class SearchView(View):
    def get(self, request):
        search_keyword = request.GET.get('keyword', None) 
        if not search_keyword:
            return JsonResponse({"MESSAGE" : "NO KEYWORD"}, status=400)
        
        products = Product.objects.filter(name__icontains=search_keyword)

        if not products.exists():
            return JsonResponse({"MESSAGE": "PRODUCT NOT FOUND"}, status=204)

        page = int(request.GET["page"]) 
        limit = int(request.GET["limit"]) 
        offset = (page-1)*limit 

        all_rooms = list(products.values())[offset: offset+limit]  

        page_count = math.ceil(len(products)/limit)   
        page_range = []

        for i in range(1, page_count+1): 
            page_range.append(i)
            result = {
            "page"        : page,
            "rooms"       : all_rooms,
            "page_count"  : page_count,
            "page_range"  : page_range,
            "total_count" : len(products),
            "products"    : []
        }

        for product in products: 
            images = product.image_set.filter(product = product.id)

            result["products"].append(
                {   
                    "name"       : product.name,
                    "price"      : product.price,
                    "colors"     : list(product.colors.all().values()),
                    "colors_num" : len(list(product.colors.values())),
                    "img_url"    : list(images.values())[:2],                        
                }
                )
        return JsonResponse({"results": result}, status=200)
