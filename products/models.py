
from django.core.validators import MinValueValidator
from django.utils.text import slugify
import os
from django.db import models
from django.urls import reverse

class Catalog(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название каталога',
        help_text='Введите название каталога'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='URL-адрес'
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='children',
        verbose_name='Родительский каталог'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Каталог'
        verbose_name_plural = 'Каталоги'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['parent']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:catalog_detail', kwargs={'slug': self.slug})

class Product(models.Model):
    catalog = models.ForeignKey(
        'Catalog',
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Каталог',
        help_text='Выберите каталог'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название продукта',
        help_text='Введите название продукта'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
        verbose_name='URL-адрес'
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Подробное описание продукта'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Цена',
        help_text='Цена в рублях'
    )
    image = models.ImageField(
        upload_to='products/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name='Изображение',
        help_text='Загрузите изображение продукта'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['price']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_image_filename(self):
        if self.image:
            return os.path.basename(self.image.name)
        return None