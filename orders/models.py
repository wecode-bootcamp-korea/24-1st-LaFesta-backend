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
    class Status(models.IntegerChoices):
        DEPOSIT           = 1
        ON_DELIVERY       = 2
        DELIVERY_COMPLETE = 3
        PURCHASE_COMPLETE = 4
        ON_CART           = 5

    status = models.CharField(max_length=32)

    class Meta:
        db_table = "order_status"


class OrderItem(TimeStamp):
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(null=True)
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    status = models.ForeignKey("OrderItemStatus", null=True ,on_delete=models.CASCADE)

    class Meta:
        db_table = "order_products"


class OrderItemStatus(TimeStamp):
    class Status(models.IntegerChoices):
        DEFAULT           = 1
        EXCHANGE          = 2
        EXCHANGE_COMPLETE = 3
        REFUND            = 4
        REFUND_COMPLETE   = 5

    status = models.CharField(max_length=32)

    class Meta:
        db_table = "order_products_status"
