import json

from django.http import JsonResponse
from django.views import View

from .models import Order, OrderStatus, OrderItem, OrderItemStatus
from core.utils import login_decorator


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

    def get(self, request):
        result = []
        carts = OrderItem.objects.filter(
            order__status_id=OrderStatus.Status.ON_CART.value
        )

        results = {
            "products": [
                {
                    "product_id": cart.product.id,
                    "product_name": cart.product.name,
                    "quantity": cart.quantity,
                    "price": cart.product.price,
                    "total_price": int(cart.product.price * cart.quantity),
                }
                for cart in carts
            ],
            "number_of_products": len(carts),
            "net_price": sum(
                [product["total_price"] for product in result["products"]]
            ),
        }

        return JsonResponse({"results": results}, status=200)

class OrderView(View):
    @login_decorator
    def post(self, request):
        try:
            confirmed_items = json.loads(request.body)["products"]

            cart_orders = Order.objects.prefetch_related("orderitem_set").get(
                status_id=OrderStatus.Status.ON_CART.value
            )
            cart_orders.user = request.user
            cart_orders.save()

            cart_items = cart_orders.orderitem_set.all()

            for cart_item in cart_items:
                id = f"{cart_item.product_id}"
                if id not in confirmed_items.keys():
                    cart_item.delete()
                    cart_item.quantity = confirmed_items[id]["quantity"]
                else:
                    cart_item.save()

            return JsonResponse({"message": "ORDER RENEWED"}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
