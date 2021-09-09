import json

from django.http import JsonResponse
from django.views import View
from django.db import transaction
from django.db.models import F, Sum

from .models import Order, OrderStatus, OrderItem, OrderItemStatus
from core.utils import login_decorator


class CartView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)

            order, is_order_created = Order.objects.get_or_create(
                status_id=OrderStatus.Status.ON_CART.value, user=request.user
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

    @login_decorator
    def get(self, request):
        carts = OrderItem.objects.filter(
            order__status_id=OrderStatus.Status.ON_CART.value, order__user=request.user
        )

        results = {
            "products": [
                {
                    "product_id": cart.product.id,
                    "product_name": cart.product.name,
                    "quantity": cart.quantity,
                    "price": int(cart.product.price),
                    "total_price": int(cart.product.price * cart.quantity),
                }
                for cart in carts
            ],
            "number_of_products": carts.aggregate(number_of_products=Sum("quantity"))["number_of_products"],
            "net_price": carts.aggregate(net_price=Sum(F("product__price") * F("quantity")))["net_price"],
        }

        return JsonResponse({"results": results}, status=200)

    @login_decorator
    def delete(self, request, product_id):
        try:
            OrderItem.objects.filter(
                order__status_id=OrderStatus.Status.ON_CART.value,
                product_id=product_id,
            ).delete()

            return JsonResponse(
                {"message": f"PRODUCT {product_id} DELETED"}, status=200
            )
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)


class OrderView(View):
    @login_decorator
    def post(self, request):
        try:
            with transaction.atomic():
                data = json.loads(request.body)

                order = Order.objects.get(
                    status_id=OrderStatus.Status.ON_CART.value, user=request.user
                )
                order.orderitem_set.all().delete()

                for product in data["products"]:
                    OrderItem.objects.create(
                        product_id=product["product_id"],
                        quantity=product["quantity"],
                        status_id=OrderItemStatus.Status.DEFAULT.value,
                        order=order,
                    )

            return JsonResponse({"message": "ORDER RENEWED"}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)


class OrderInformationView(View):
    @login_decorator
    def patch(self, request):
        try:
            data = json.loads(request.body)

            order_on_cart = Order.objects.get(
                status_id=OrderStatus.Status.ON_CART.value, user=request.user
            )

            order_on_cart.address = data["address"]
            order_on_cart.receiver = data["receiver"]
            order_on_cart.receiver_phone_number = data["receiver_phone_number"]
            order_on_cart.save()

            return JsonResponse({"message": "ORDER INFORMATION UPDATED"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
