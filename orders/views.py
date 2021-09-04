import json

from django.http import JsonResponse
from django.views import View

from .models import Order, OrderStatus, OrderItem, OrderItemStatus


class OrderProductCartView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not OrderItem.objects.filter(product_id=data["product_id"]).exists():
                self.add_to_cart(data["product_id"])
                return JsonResponse({"message": "ADDED TO CART"}, status=201)

            order_items = OrderItem.objects.filter(product_id=data["product_id"])
            for order_item in order_items:
                if order_item.order.status.status=="OC":
                    order_item.quantity += 1
                    order_item.save()
                    return JsonResponse({"message": "ADD ONE MORE TO CART"}, status=201)

            self.add_to_cart(data["product_id"])
            return JsonResponse({"message": "ADDED TO CART"}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

    def add_to_cart(self, product_id):
        on_cart = OrderStatus.objects.get(status="OC")
        default_item_status = OrderItemStatus.objects.get(status="DE")
        order_created = Order.objects.create(status=on_cart)
        OrderItem.objects.create(
            product_id=product_id,
            quantity=1,
            order=order_created,
            status=default_item_status,
        )
