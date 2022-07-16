from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()


# product
# category
# cardproduct
# card
# order
# ----
# customer
# Specification

class LatestProductManager:

    @staticmethod
    def get_products_for_main_page(self,*args,**kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products= []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products =  ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(
                        products, key=lambda x:x.__class__._meta.model_name.startswith(with_respect_to), reverse=True
                    )
        return products


class LatestProducts:
    objects = LatestProductManager()

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name="Наименование")
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=1, verbose_name='Цена')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


# class NoteBookProduct(models.Model):
#     pass

class CardProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='ПОкупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_product')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_obj = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=9, decimal_places=1, verbose_name='Общая Цена')

    def __str__(self):
        return "Продукт {} (корзина)".format(self.product.title)


class Cart(models.Model):
    owner = models.ForeignKey('Customer', verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CardProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=1)
    tinal_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=13, verbose_name='Телефон')
    address = models.CharField(max_length=255, verbose_name='Адрес')

    def __str__(self):
        return 'Покупатель {} {}'.format(self.user.first_name, self.user.last_name)


class Notebook(Product):
    diagonal = models.CharField(max_length=255, verbose_name='Диагональ')
    display_type = models.CharField(max_length=255, verbose_name='Тип дисплея')
    processor_freq = models.CharField(max_length=255, verbose_name='Тип процессора')
    ram = models.CharField(max_length=8, verbose_name='RAM')
    video = models.CharField(max_length=8, verbose_name='GPU')
    time_without_change = models.CharField(max_length=23, verbose_name='Время работы от батареи')

    def __str__(self):
        return "{}:{}".format(self.category.name, self.title)


class SmartPhone(Product):
    diagonal = models.CharField(max_length=255, verbose_name='Диагональ')
    display_type = models.CharField(max_length=255, verbose_name='Тип дисплея')
    resolution = models.CharField(max_length=255, verbose_name='Разрешение экрана')
    accum_volume = models.CharField(max_length=255, verbose_name='Батарея')
    ram = models.CharField(max_length=8, verbose_name='RAM')
    sd = models.BooleanField(default=True, verbose_name='SD')
    sd_volume_max = models.CharField(max_length=255, verbose_name='максимальный обьем sd')
    main_cam_mp = models.CharField(max_length=255, verbose_name='Перед камера')
    frontal_cam_mp = models.CharField(max_length=255, verbose_name='Фронт камера')

    def __str__(self):
        return "{}:{}".format(self.category.name, self.title)
