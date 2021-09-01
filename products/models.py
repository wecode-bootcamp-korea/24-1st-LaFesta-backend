from django.db import models


class Type(models.Model):
    name = models.CharField(max_length=32)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)

    class Meta:
        db_table = "types"


class Category(models.Model):
    name = models.CharField(max_length=32)
    section = models.ForeignKey("Section", on_delete=models.CASCADE)

    class Meta:
        db_table = "categories"


class Section(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        db_table = "sections"


class Product(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=18)
    type = models.ForeignKey("Type", on_delete=models.CASCADE)
    fit = models.ForeignKey("Fit", null=True, on_delete=models.SET_NULL)
    description = models.ForeignKey("Description", null=True, on_delete=models.SET_NULL)
    colors = models.ManyToManyField("Color", related_name="products", through="ProductColor")
    sizes = models.ManyToManyField("Size", related_name="products", through="ProductSize")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products"


class Fit(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        db_table = "fits"


class Size(models.Model):
    size = models.SmallIntegerField()

    class Meta:
        db_table = "sizes"


class ProductSize(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    size = models.ForeignKey("Size", on_delete=models.CASCADE)

    class Meta:
        db_table = "products_sizes"


class Color(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        db_table = "colors"


class ProductColor(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    color = models.ForeignKey("Color", on_delete=models.CASCADE)

    class Meta:
        db_table = "products_colors"


class Description(models.Model):
    summary = models.TextField(null=True)
    extra_information = models.CharField(max_length=128, null=True)

    class Meta:
        db_table = "descriptions"


class Image(models.Model):
    image_url = models.CharField(max_length=256)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)

    class Meta:
        db_table = "images"
