import json

from django.http import JsonResponse
from django.views import View

from .models import Order, OrderStatus, OrderItem, OrderItemStatus


class CartView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            order, is_order_created = Order.objects.get_or_create(
                status_id=OrderStatus.Status.ON_CART.value
            )
            order_item, is_order_item_created = OrderItem.objects.get_or_create(
                product_id=data["product_id"], order_id=order.id
            )

            if is_order_item_created:
                order_item.quantity = 1
                order_item.status_id = OrderItemStatus.Status.DEFAULT.value
            else:
                order_item.quantity += 1

            order_item.save()
            return JsonResponse({"message": "ADDED TO CART"}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
