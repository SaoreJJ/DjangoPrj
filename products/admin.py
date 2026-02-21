from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import Product
from .forms import ProductForm


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ['name', 'price', 'is_active', 'created_at', 'image_preview']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['price', 'is_active']
    readonly_fields = ['created_at', 'updated_at', 'image_preview']
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'description', 'price')
        }),
        ('Изображение', {
            'fields': ('image', 'image_preview'),
            'classes': ('collapse',)
        }),
        ('Статус', {
            'fields': ('is_active',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 100px;" />',
                obj.image.url
            )
        return "Нет изображения"

    image_preview.short_description = 'Превью'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['confirm_terms'].required = False
        return form