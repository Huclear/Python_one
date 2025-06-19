from rest_framework import serializers
from routing_app.models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'name',
            'description'
        ]
        
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'name',
            'description'
        ]

class GoodsSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(label="Price", max_digits=10, decimal_places=2)
    
    class Meta:
        model = Goods
        fields = [
            'name',
            'description',
            'price',
            'image',
            'dateCreated',
            'dateEdited',
            'category',
            'tags',
        ]

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            'login',
            'password',
            'salt',
            'firstName',
            'lastName'
        ]

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'deliveryAddress',
            'dateCreated',
            'client'
        ]

class OrderGoodsSerializer(serializers.ModelSerializer):
    discount = serializers.DecimalField(label="Price", max_digits=10, decimal_places=2)
    
    class Meta:
        model = OrderGoods
        fields = [
            'order',
            'good',
            'amount',
            'discount'
        ]

class BasketGoodsSerializer(serializers.ModelSerializer):
    discount = serializers.DecimalField(label="Price", max_digits=10, decimal_places=2)
    
    class Meta:
        model = BasketGoods
        fields = [
            'client',
            'good',
            'amount',
            'discount'
        ]