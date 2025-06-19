from rest_framework import routers
from django.urls import path, include
from .views import *

urlpatterns = [
    path("", home, name="api_page")
]

router = routers.SimpleRouter()

router.register('category', CategoryViewSet, basename='category')
router.register('tag', TagViewSet, basename='tag')
router.register('goods', GoodsViewSet, basename='goods')
router.register('client', ClientViewSet, basename='client')
router.register('order', OrderViewSet, basename='order')
router.register('ordergoods', OrderGoodsViewSet, basename='ordergoods')
router.register('basketgoods', BasketGoodsViewSet, basename='basketgoods')
urlpatterns += router.urls
