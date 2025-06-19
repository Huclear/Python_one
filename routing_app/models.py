import uuid
import re
import random
from django.core.validators import RegexValidator
from django.db import models

class Item():
    def __init__(self, id):
        self.id = id
        self.name = 'Test name' + str(id)
        self.description = 'Test description' + str(id)
        self.description = 'Test description' + str(id)
        self.random_1 = random.randint(1, id + 1)
        self.random_2 = random.randint(id, id * 2 + 1)
        self.random_3 = random.randint(id-id*2-1, 0)
        
class Category(models.Model):
    name = models.CharField(verbose_name='name', max_length=255)
    
    description = models.TextField(null=True, blank=True, verbose_name='description')
    
    def __str__(self):
        return self.name
    
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

class Tag(models.Model):
    name = models.CharField(verbose_name='name', max_length=255)
    
    description = models.TextField(null=True, blank=True, verbose_name='description')
    
    def __str__(self):
        return self.name
    
    
    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'

class Goods(models.Model):
    name = models.CharField(verbose_name='name', max_length=255)
    
    description = models.TextField(null=True, blank=True, verbose_name='description')
    
    price = models.FloatField(verbose_name='price', default=1.0)
    
    image = models.ImageField(verbose_name='image', upload_to='image/%Y/%m/%d', null=True, blank=True)
    
    dateCreated = models.DateTimeField(verbose_name='date_created', auto_now_add=True)
    
    dateEdited = models.DateTimeField(verbose_name='date_edited', auto_now=True)
    
    category = models.ForeignKey(Category, verbose_name='category', on_delete=models.CASCADE)
    
    tags = models.ManyToManyField(Tag, verbose_name='tags')
    
    def __str__(self):
        return self.name
    
    
    class Meta:
        verbose_name = 'good'
        verbose_name_plural = 'goods'
        
class Client(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='id')
    
    login=models.CharField(verbose_name='login', max_length=255)
    
    password=models.TextField(verbose_name='password', null=False, blank=False)
    
    salt=models.CharField(verbose_name='salt', max_length=200)
    
    firstName = models.CharField(verbose_name='first_name', max_length=255)
    
    lastName = models.CharField(verbose_name='last_name', max_length=255)
    
    email = models.CharField(verbose_name='email_address', max_length=50, null=True, validators=[
        RegexValidator(
            regex=r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',
            message="Enter a valid phone number",
            code="invalid_phone",
        )])
    
    
    
    def __str__(self):
        return f'{self.firstName} {self.lastName}'
    
    
    class Meta:
        verbose_name = 'client'
        verbose_name_plural = 'clients',

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='id')
    
    deliveryAddress = models.TextField(verbose_name='delivery_address')
    
    dateCreated = models.DateTimeField(verbose_name='date_created', auto_now=False, auto_now_add=True)
    
    client = models.ForeignKey(Client, verbose_name='client', on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'

class OrderGoods(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='id')
    
    order = models.ForeignKey(Order, verbose_name='order', on_delete=models.CASCADE)
    
    good = models.ForeignKey(Goods, verbose_name='good', on_delete=models.CASCADE)
    
    amount = models.PositiveIntegerField(verbose_name='amount_good', default=1)
    
    discount=models.FloatField(verbose_name='discount_per_unit', default = 0.0)
    
    class Meta:
        verbose_name = 'order_good'
        verbose_name_plural = 'order_goods'  
        
class BasketGoods(models.Model):
    client = models.ForeignKey(Client, verbose_name='client', on_delete=models.CASCADE)
    
    good = models.ForeignKey(Goods, verbose_name='good', on_delete=models.CASCADE)
    
    amount = models.PositiveIntegerField(verbose_name='amount_good', default=1)
    
    discount=models.FloatField(verbose_name='discount_per_unit', default = 0.0)
    
    def __str__(self):
        return f'{client.__str__()} - {good.__str__()}'
    
    
    class Meta:
        verbose_name = 'basket_goods'
        verbose_name_plural = 'basket_goods'
        
class FavoriteGoods(models.Model):
    client = models.ForeignKey(Client, verbose_name='client', on_delete=models.CASCADE)
    
    good = models.ForeignKey(Goods, verbose_name='good', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Favorite: {client.__str__()} - {good.__str__()}'
    
    class Meta:
        verbose_name = 'favorite_goods'
        verbose_name_plural = 'favorites_goods'