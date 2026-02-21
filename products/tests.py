from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io

from .models import Product
from .forms import ProductForm


class ProductFormTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.valid_data = {
            'name': 'Тестовый продукт',
            'description': 'Отличный продукт для тестирования',
            'price': '100.50',
            'confirm_terms': True,
        }

    def test_valid_form(self):
        """Тест валидной формы"""
        form = ProductForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_forbidden_words_in_name(self):
        """Тест запрещенных слов в названии"""
        data = self.valid_data.copy()
        data['name'] = 'Продукт казино лучший'

        form = ProductForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('запрещенные слова', form.errors['name'][0].lower())

    def test_negative_price(self):
        """Тест отрицательной цены"""
        data = self.valid_data.copy()
        data['price'] = '-10'

        form = ProductForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('отрицательной', form.errors['price'][0].lower())

    def test_image_validation(self):
        """Тест валидации изображения"""
        # Создаем тестовое изображение
        image = Image.new('RGB', (100, 100), color='red')
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)

        image_file = SimpleUploadedFile(
            'test.jpg',
            image_io.getvalue(),
            content_type='image/jpeg'
        )

        data = self.valid_data.copy()
        data['image'] = image_file

        form = ProductForm(data=data, files={'image': image_file})
        self.assertTrue(form.is_valid())

    def test_large_image(self):
        """Тест слишком большого изображения"""
        # Создаем большой файл (симулируем)
        large_file = SimpleUploadedFile(
            'large.jpg',
            b'x' * (6 * 1024 * 1024),  # 6 MB
            content_type='image/jpeg'
        )

        data = self.valid_data.copy()
        data['image'] = large_file

        form = ProductForm(data=data, files={'image': large_file})
        self.assertFalse(form.is_valid())
        self.assertIn('превышает', form.errors['image'][0].lower())