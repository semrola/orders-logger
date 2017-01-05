from rest_framework import serializers
from .models import Item, Order, Store, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item


class OrderSerializer(serializers.ModelSerializer):
    #toString = Order.__str__()
    name = serializers.SerializerMethodField()
    storename = serializers.SerializerMethodField()

    class Meta:
        model = Order
        exclude = ('store',)

    def get_name(self, obj):
        return Order.__str__(obj)

    def get_storename(self, obj):
        return obj.store.__str__()
