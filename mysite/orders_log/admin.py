from django.contrib import admin
from .models import Comment
from .models import Order
from .models import Store
from .models import Item

# Register your models here.
admin.site.register(Comment)
admin.site.register(Store)
admin.site.register(Item)
admin.site.register(Order)
