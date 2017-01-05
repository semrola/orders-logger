from django.db import models

# Create your models here.


class Store(models.Model):
    name = models.CharField(max_length=100)
    homepage = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    ordered = models.DateTimeField()
    shipped = models.DateTimeField(blank=True, null=True)
    received = models.DateTimeField(blank=True, null=True)
    shippingDateTo = models.DateTimeField(blank=True, null=True)
    shippingDateFrom = models.DateTimeField(blank=True, null=True)
    shippingDaysTo = models.IntegerField(blank=True, null=True)
    shippingDaysFrom = models.IntegerField(blank=True, null=True)

    # FKs
    store = models.ForeignKey(Store, blank=True, null=True)

    def __str__(self):
        items = self.item_set.all()
        if len(items) > 0:
            out = ', '.join([str(o.name) for o in items])
        else:
            out = "Order " + str(self.id)
        return out


class Item(models.Model):
    name = models.CharField(max_length=80)
    url = models.CharField(max_length=250, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    shipped = models.DateTimeField(blank=True, null=True)
    received = models.DateTimeField(blank=True, null=True)
    shippingDateTo = models.DateTimeField(blank=True, null=True)
    shippingDateFrom = models.DateTimeField(blank=True, null=True)
    shippingDaysTo = models.IntegerField(blank=True, null=True)
    shippingDaysFrom = models.IntegerField(blank=True, null=True)

    # FKs
    order = models.ForeignKey(Order)

    def __str__(self):
        return self.name + " " + str(self.price)


class Comment(models.Model):
    content = models.TextField()
    published = models.DateTimeField()
    last_edited = models.DateTimeField()

    #FKs
    store = models.ForeignKey(Store, blank=True, null=True)
    order = models.ForeignKey(Order, blank=True, null=True)
    item = models.ForeignKey(Item, blank=True, null=True)

