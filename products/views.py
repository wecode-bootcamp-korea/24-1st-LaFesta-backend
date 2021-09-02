import json

from django.http import JsonResponse
from django.views import View

from .models import Product, Image


class ProductDetailView(View):
    def get(self, request, **kwargs):
        result = {}
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
