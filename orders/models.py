from django.db import models

from core.models import TimeStamp

class Order(TimeStamp):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, null=True)
    receiver = models.CharField(max_length=32, null=True)
    receiver_phone_number = models.CharField(max_length=32, null=True)
    address = models.CharField(max_length=64, null=True)
    status = models.ForeignKey("OrderStatus", on_delete=models.CASCADE)

    class Meta:
        db_table = "orders"


class OrderStatus(TimeStamp):
    status = models.CharField(max_length=32)

    class Meta:
        db_table = "order_status"


class OrderItem(TimeStamp):
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    status = models.ForeignKey("OrderItemStatus", on_delete=models.CASCADE)

    class Meta:
        db_table = "order_products"


class OrderItemStatus(TimeStamp):
    status = models.CharField(max_length=32)

    class Meta:
        db_table = "order_products_status"
