from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
User = get_user_model()

#product
#category
#cardproduct
#card
#order
#----
#customer
#Specification

class Category(models.Model):
    name = models.CharField(max_length=255,verbose_name='Категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
   title= models.CharField(max_length=255,verbose_name="Наименование")
   slug = models.SlugField(unique=True)
   image= models.ImageField(verbose_name='Изображение')
   description = models.TextField(verbose_name='Описание',null=True)
   price = models.DecimalField(max_digits=9,decimal_places=1,verbose_name='Цена')
   category= models.ForeignKey(Category,verbose_name='Категория',on_delete=models.CASCADE)

   def __str__(self):
       return  self.title

class CardProduct(models.Model):
    user = models.ForeignKey('Customer',verbose_name='ПОкупатель',on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart',verbose_name='Корзина',on_delete=models.CASCADE,related_name='related_product')
    product = models.ForeignKey(Product,verbose_name='Товар',on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    total_price=models.DecimalField(max_digits=9,decimal_places=1,verbose_name='Общая Цена')

    def __str__(self):
        return "Продукт {} (корзина)".format(self.product.title)


class Cart(models.Model):
    owner = models.ForeignKey('Customer',verbose_name='Владелец',on_delete=models.CASCADE)
    products = models.ManyToManyField(CardProduct,blank=True,related_name='related_cart')
    total_products = models.PositiveIntegerField(default=1)
    tinal_price = models.DecimalField(max_digits=9,decimal_places=2,verbose_name='Цена')


class Customer(models.Model):
    user= models.ForeignKey(User,verbose_name='Пользователь',on_delete=models.CASCADE)
    phone= models.CharField(max_length=13,verbose_name='Телефон')
    address = models.CharField(max_length=255,verbose_name='Адрес')

    def __str__(self):
        return 'Покупатель {} {}'.format(self.user.first_name, self.user.last_name)

