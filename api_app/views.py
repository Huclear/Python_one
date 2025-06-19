from django.shortcuts import render
from .serializers import *
from rest_framework import viewsets
from routing_app.models import *
from .permissions import *

def home(request):
    return render(request, "home.html")

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [CustomPermissions]

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class GoodsViewSet(viewsets.ModelViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    permission_classes = [CustomPermissions]
    
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [CustomPermissions]
    
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [CustomPermissions]
    
class OrderGoodsViewSet(viewsets.ModelViewSet):
    queryset = OrderGoods.objects.all()
    serializer_class = OrderGoodsSerializer
    permission_classes = [CustomPermissions]
    
class BasketGoodsViewSet(viewsets.ModelViewSet):
    queryset = BasketGoods.objects.all()
    serializer_class = BasketGoodsSerializer
    permission_classes = [CustomPermissions]