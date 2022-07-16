from django.contrib import admin
from .models import *
from django.forms import ModelChoiceField,ModelForm,ValidationError

from PIL import Image


class NotebookAdminForm(ModelForm):
    MIN_RESOLUTION = (400, 400)
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['image'].help_text = 'Загружайте изображение с мин разрешением {}x{}'.format(*self.MIN_RESOLUTION)

    def clean_image(self):
        image =self.cleaned_data['image']
        img = Image.open(image)
        min_height , min_width = self.MIN_RESOLUTION
        if (img.width <min_width or img.height <min_height):
            raise ValidationError('Изображение меньше установленного')
        return  image
class NotebookAdmin(admin.ModelAdmin):
    form = NotebookAdminForm
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='notebook'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartphoneAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='Smaprtphone'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(SmartPhone, SmartphoneAdmin)
admin.site.register(CardProduct)
admin.site.register(Cart)
admin.site.register(Customer)
