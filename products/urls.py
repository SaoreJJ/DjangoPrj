from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Главная страница - список продуктов
    path('', views.ProductListView.as_view(), name='product_list'),

    # Создание продукта
    path('create/', views.ProductCreateView.as_view(), name='product_create'),

    # Детали продукта
    path('<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),

    # Редактирование продукта
    path('<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_update'),

    # Удаление продукта
    path('<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
]