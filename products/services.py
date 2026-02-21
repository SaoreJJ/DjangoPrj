from django.core.cache import cache
from django.conf import settings
from .models import Product


def get_products_by_category(category_slug):
    """
    Возвращает список продуктов в указанной категории
    с поддержкой кеширования
    """
    cache_key = f'category_products_{category_slug}'

    # Если кеширование включено, пробуем получить из кеша
    if settings.CACHE_ENABLED:
        products = cache.get(cache_key)
        if products is not None:
            return products

    # Получаем продукты из БД
    products = Product.objects.filter(
        catalog__slug=category_slug,
        is_active=True,
        is_published=True
    ).select_related('catalog').order_by('-created_at')

    # Кешируем результат
    if settings.CACHE_ENABLED:
        cache.set(cache_key, products, 60 * 15)  # 15 минут

    return products


def get_all_products():
    """
    Возвращает список всех активных опубликованных продуктов
    с низкоуровневым кешированием
    """
    cache_key = 'all_active_products'

    if settings.CACHE_ENABLED:
        products = cache.get(cache_key)
        if products is not None:
            return products

    products = list(Product.objects.filter(
        is_active=True,
        is_published=True
    ).select_related('catalog', 'owner').order_by('-created_at'))

    if settings.CACHE_ENABLED:
        cache.set(cache_key, products, 60 * 15)

    return products