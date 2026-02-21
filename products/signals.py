from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Product


@receiver([post_save, post_delete], sender=Product)
def clear_product_cache(sender, **kwargs):
    """
    Очищает кеш продуктов при любых изменениях
    """
    cache.delete('all_active_products')

    # Если есть категория, очищаем и её кеш
    instance = kwargs.get('instance')
    if instance and instance.catalog:
        cache.delete(f'category_products_{instance.catalog.slug}')