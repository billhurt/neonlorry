from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.latest_products, name='index'),
    path('<slug:slug>', views.product_detail, name='product_detail'),
    path('shop/<slug:category_slug>/', views.category_list, name='category_list'),
    path('shop/', views.all_products, name="shop"),
    path('about/', TemplateView.as_view(template_name="store/about.html"), name="about"),
]
