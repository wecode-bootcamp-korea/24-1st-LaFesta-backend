from django.db import models

from core.models import TimeStamp

class Order(TimeStamp):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    address = models.CharField(max_length=64)
    memo = models.TextField()
    status = models.ForeignKey("OrderStatus", on_delete=models.CASCADE)

    class Meta:
        db_table = "orders"


class OrderStatus(TimeStamp):
    DEPOSIT = "D"
    ON_DELIVERY = "OD"
    DELIVERY_COMPLETE = "DC"
    PURCHASE_COMPLETE = "PC"

    ORDER_CHOICE = [
        (DEPOSIT, "deposit"),
        (ON_DELIVERY, "on_delivery"),
        (DELIVERY_COMPLETE, "delivery_complete"),
        (PURCHASE_COMPLETE, "purchase_complete"),
    ]
    status = models.CharField(max_length=32, choices=ORDER_CHOICE)

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
    EXCHANGE = "E"
    EXCHANGE_COMPLETE = "EC"
    REFUND = "R"
    REFUND_COMPLETE = "RC"

    ORDER_PRODUCTS_CHOICE = [
        (EXCHANGE, "exchange"),
        (EXCHANGE_COMPLETE, "exchange_complete"),
        (REFUND, "refund"),
        (REFUND_COMPLETE, "refund_complete"),
    ]
    status = models.CharField(max_length=32, choices=ORDER_PRODUCTS_CHOICE)

    class Meta:
        db_table = "order_products"
