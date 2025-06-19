"""
URL configuration for practice_1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from routing_app.views import *

urlpatterns = [
    
    # Users
    path("", index, name="home"),
    path("login/", login_user, name="login_page"),
    path("register/", register_user, name="register_page"),
    path("logout/", logout_user, name="logout_page"),
    
    
    # Catalogue rooot
    path("catalogue/", catalogue, name="catalogue_list"),
    path("catalogue/<int:pk>", catalogue_details, name="catalogue_detail"),
    path("catalogue/insert", CatalogueCreateView.as_view(), name="catalogue_insert"),
    path("catalogue/delete/<int:pk>", CatalogueDeleteView.as_view(), name="catalogue_delete"),
    path("catalogue/edit/<int:pk>", CatalogueUpdateView.as_view(), name="catalogue_edit"),
    path("catalogue/feedback", catalogue_feedback, name="feedback_page"),
    

    # Profile root
    path("profile/", profile, name="profile_page"),

    # Basket root
    path("basket/", basket, name="basket_page"),
    path("basket/delete/<int:pk>", BasketDeleteView.as_view(), name="basket_delete"),
    path("basket/clear", basket_clear, name="basket_clear"),
    path("basket/order", create_order, name="order_create"),
    
    # Orders root
    path("order/", orders, name="orders_page"),
    path("order/<uuid:pk>", order_details, name="order_details"),
    path("order/delete/<uuid:pk>", OrderDeleteView.as_view(), name="order_delete"),
    
    
    # Category root
    path("category/", CategoryListView.as_view(), name="category_list"),
    path("category/insert", CategoryCreateView.as_view(), name="category_insert"),
    path("category/edit/<int:pk>", CategoryUpdateView.as_view(), name="category_edit"),
    path("category/delete/<int:pk>", CategoryDeleteView.as_view(), name="category_delete"),
    
    # Tag root
    path("tag/", TagListView.as_view(), name="tag_list"),
    path("tag/insert", TagCreateView.as_view(), name="tag_insert"),
    path("tag/edit/<int:pk>", TagUpdateView.as_view(), name="tag_edit"),
    path("tag/delete/<int:pk>", TagDeleteView.as_view(), name="tag_delete")
]
    