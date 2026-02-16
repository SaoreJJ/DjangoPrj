from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product
from .forms import ProductForm
from django.core.exceptions import PermissionDenied
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages


class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 10


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('products:product_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Продукт успешно создан!")
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"

    def get_success_url(self):
        messages.success(self.request, "Продукт успешно обновлен!")
        return reverse_lazy("products:product_detail", kwargs={"pk": self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        # Проверяем: владелец ИЛИ пользователь с правом can_unpublish_product (модератор)
        if not (obj.owner == request.user or request.user.has_perm('products.can_unpublish_product')):
            raise PermissionDenied("У вас нет прав на удаление")
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Продукт успешно удален!")
        return super().delete(request, *args, **kwargs)

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "products/product_confirm_delete.html"
    success_url = reverse_lazy("products:product_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Продукт успешно удален!")
        return super().delete(request, *args, **kwargs)

class ProductUnpublishView(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if request.user.has_perm('products.can_unpublish_product'):
            product.is_published = False
            product.save()
            messages.success(request, 'Продукт снят с публикации')
        else:
            raise PermissionDenied("У вас нет прав на отмену публикации")
        return redirect('products:product_detail', pk=pk)