from django.db import models


class Advertisement(models.Model):
    remote_id = models.CharField('Удаленный идентификатор', unique=True, max_length=50)
    title = models.CharField('Название', max_length=100)
    description = models.CharField('Описание', max_length=500, default="")
    created = models.DateTimeField(auto_now_add=True)
    link = models.URLField('Ссылка на рекламу')
    category = models.CharField('Категория рекламы', max_length=100)
    price = models.FloatField('Цена')
    currency = models.CharField('Валюта', default='RUB', max_length=10)

    class Meta:
        verbose_name = 'Содержимое рекламы'
        verbose_name_plural = 'Содержимое реклам'
