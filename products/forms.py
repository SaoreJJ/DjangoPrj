from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
import os
from PIL import Image

from .models import Product


class ProductForm(forms.ModelForm):
    # Задание 1: Список запрещенных слов
    FORBIDDEN_WORDS = [
        'казино',
        'криптовалюта',
        'крипта',
        'биржа',
        'дешево',
        'бесплатно',
        'обман',
        'полиция',
        'радар'
    ]

    # Дополнительное поле для подтверждения
    confirm_terms = forms.BooleanField(
        label='Я подтверждаю, что ознакомлен с правилами',
        required=True,
        error_messages={'required': 'Необходимо подтвердить условия'}
    )

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Введите название продукта',
                'autofocus': True
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Опишите продукт подробно',
                'rows': 5
            }),
            'price': forms.NumberInput(attrs={
                'placeholder': '0.00',
                'step': '0.01'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'name': 'Название продукта',
            'description': 'Описание',
            'price': 'Цена (руб.)',
            'image': 'Изображение',
            'is_active': 'Активный продукт',
        }
        help_texts = {
            'name': 'Максимум 200 символов',
            'description': 'Будьте подробны, но лаконичны',
            'price': 'Цена должна быть положительной',
            'image': 'JPEG или PNG, до 5 МБ',
        }
        error_messages = {
            'name': {
                'required': 'Название обязательно для заполнения',
                'max_length': 'Название слишком длинное',
            },
            'price': {
                'required': 'Цена обязательна для заполнения',
                'invalid': 'Введите корректную цену',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Задание 3: Стилизация всех полей формы
        for field_name, field in self.fields.items():
            # Пропускаем чекбоксы для отдельной обработки
            if field_name in ['is_active', 'confirm_terms']:
                continue

            # Добавляем CSS классы
            if field_name == 'description':
                field.widget.attrs.update({
                    'class': 'form-control form-control-lg',
                    'style': 'resize: vertical; min-height: 120px;'
                })
            elif field_name == 'price':
                field.widget.attrs.update({
                    'class': 'form-control price-input',
                    'style': 'max-width: 200px;'
                })
            elif field_name == 'image':
                field.widget.attrs.update({
                    'class': 'form-control file-input',
                    'accept': '.jpg,.jpeg,.png'
                })
            else:
                field.widget.attrs.update({
                    'class': 'form-control'
                })

            # Добавляем HTML5 атрибуты
            if field.required:
                field.widget.attrs['required'] = 'required'

            # Адаптивные placeholder
            if not field.widget.attrs.get('placeholder'):
                field.widget.attrs['placeholder'] = f'Введите {field.label.lower()}'

        # Специальная стилизация для чекбоксов
        self.fields['is_active'].widget.attrs.update({
            'class': 'form-check-input'
        })
        self.fields['confirm_terms'].widget.attrs.update({
            'class': 'form-check-input'
        })

    # Задание 1: Валидация запрещенных слов
    def _contains_forbidden_words(self, text):
        """Проверяет текст на наличие запрещенных слов"""
        text_lower = text.lower()
        found_words = []

        for word in self.FORBIDDEN_WORDS:
            if word in text_lower:
                found_words.append(word)

        return found_words

    def clean_name(self):
        name = self.cleaned_data.get('name', '')

        if not name:
            raise ValidationError('Название не может быть пустым')

        # Проверка на запрещенные слова
        forbidden_words = self._contains_forbidden_words(name)
        if forbidden_words:
            raise ValidationError(
                f'Название содержит запрещенные слова: {", ".join(forbidden_words)}'
            )

        # Дополнительная проверка длины
        if len(name) < 3:
            raise ValidationError('Название должно содержать минимум 3 символа')

        return name.strip()

    def clean_description(self):
        description = self.cleaned_data.get('description', '')

        # Проверка на запрещенные слова
        forbidden_words = self._contains_forbidden_words(description)
        if forbidden_words:
            raise ValidationError(
                f'Описание содержит запрещенные слова: {", ".join(forbidden_words)}'
            )

        # Дополнительная проверка
        if description and len(description) < 10:
            raise ValidationError('Описание должно содержать минимум 10 символов')

        return description.strip()

    # Задание 2: Валидация цены
    def clean_price(self):
        price = self.cleaned_data.get('price')

        if price is None:
            raise ValidationError('Цена обязательна для заполнения')

        # Проверка на отрицательное значение
        if price < 0:
            raise ValidationError('Цена не может быть отрицательной')

        # Проверка на слишком высокую цену
        if price > 1000000:
            raise ValidationError('Цена не может превышать 1 000 000 рублей')

        # Проверка на слишком низкую цену (кроме 0)
        if 0 < price < 0.01:
            raise ValidationError('Минимальная цена - 0.01 рубля')

        # Форматирование до 2 знаков после запятой
        return round(price, 2)

    # Дополнительное задание: Валидация изображения
    def clean_image(self):
        image = self.cleaned_data.get('image')

        # Если изображение не загружено, возвращаем None
        if not image:
            return image

        # Проверка расширения файла
        valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        ext = os.path.splitext(image.name)[1].lower()

        if ext not in valid_extensions:
            raise ValidationError(
                f'Неподдерживаемый формат файла. '
                f'Разрешены: {", ".join(valid_extensions)}'
            )

        # Проверка размера файла (5 МБ)
        max_size = 5 * 1024 * 1024  # 5 МБ в байтах
        if image.size > max_size:
            size_mb = image.size / (1024 * 1024)
            raise ValidationError(
                f'Размер файла ({size_mb:.2f} МБ) превышает максимальный (5 МБ)'
            )

        # Проверка содержимого изображения
        try:
            img = Image.open(image)
            img.verify()  # Проверка целостности файла

            # Проверка на слишком большие размеры
            img = Image.open(image)  # Открываем снова после verify
            width, height = img.size
            if width > 5000 or height > 5000:
                raise ValidationError(
                    f'Изображение слишком большое: {width}x{height}px. '
                    f'Максимум: 5000x5000px'
                )

            # Проверка на слишком маленькие размеры
            if width < 100 or height < 100:
                raise ValidationError(
                    f'Изображение слишком маленькое: {width}x{height}px. '
                    f'Минимум: 100x100px'
                )

        except Exception as e:
            raise ValidationError(
                f'Некорректный файл изображения: {str(e)}'
            )

        # Проверка имени файла
        if len(image.name) > 100:
            raise ValidationError('Имя файла слишком длинное')

        # Запрещенные символы в имени файла
        forbidden_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        if any(char in image.name for char in forbidden_chars):
            raise ValidationError('Имя файла содержит запрещенные символы')

        return image

    # Общая валидация формы
    def clean(self):
        cleaned_data = super().clean()

        # Дополнительные кросс-полевые проверки
        name = cleaned_data.get('name')
        description = cleaned_data.get('description')

        if name and description:
            # Проверка, что описание не слишком похоже на название
            if name.lower() in description.lower() and len(description) < 50:
                self.add_error(
                    'description',
                    'Описание должно быть более развернутым, а не повторять название'
                )

        return cleaned_data