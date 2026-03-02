from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import ProductForm
from .models import Product


class HomeView(TemplateView):
    template_name = "catalog/home.html"


class ContactsView(TemplateView):
    template_name = "catalog/contacts.html"


class ProductListView(ListView):
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        qs = super().get_queryset().select_related("category", "owner")

        user = self.request.user
        if not user.is_authenticated:
            # Аноним видит только опубликованные
            return qs.filter(is_published=True)

        # Модератор/админ видит все
        if user.is_staff or user.has_perm("catalog.can_unpublish_product"):
            return qs

        # Обычный пользователь видит опубликованные + свои
        return qs.filter(Q(is_published=True) | Q(owner=user))


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        user = request.user

        # Опубликован — всем можно
        if obj.is_published:
            return super().dispatch(request, *args, **kwargs)

        # Не опубликован — только владелец или модератор/админ
        if user.is_authenticated and (user == obj.owner or user.is_staff or user.has_perm("catalog.can_unpublish_product")):
            return super().dispatch(request, *args, **kwargs)

        raise PermissionDenied("Этот товар не опубликован.")


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("catalog:product_detail", kwargs={"pk": self.object.pk})


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def test_func(self):
        # Редактировать может только владелец
        return self.request.user == self.get_object().owner

    def form_valid(self, form):
        # Снять с публикации может только модератор/админ
        if "is_published" in form.changed_data and form.cleaned_data.get("is_published") is False:
            user = self.request.user
            if not (user.is_staff or user.has_perm("catalog.can_unpublish_product")):
                raise PermissionDenied("Снимать с публикации может только модератор.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("catalog:product_detail", kwargs={"pk": self.object.pk})


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:product_list")

    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        # Удалить может владелец или тот, у кого есть право delete_product (модератор)
        return user == obj.owner or user.is_staff or user.has_perm("catalog.delete_product")