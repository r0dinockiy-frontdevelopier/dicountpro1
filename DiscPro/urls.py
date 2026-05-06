from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('benefits/', views.benefits, name='benefits'),
    path('trust/', views.trust, name='trust'),
    path('discounts/', views.discount_list, name='discount_list'),
    path('discounts/category/<slug:cat_slug>/', views.category_discounts, name='category_discounts'),
    path('discounts/tag/<slug:tag_slug>/', views.tag_discounts, name='tag_discounts'),
    path('discounts/category/<slug:cat_slug>/tag/<slug:tag_slug>/', views.category_tag_discounts, name='category_tag_discounts'),
    path('discounts/<slug:discount_slug>/', views.discount_detail, name='discount_detail'),
    path('addpage/', views.addpage, name='addpage'),
    path('contact/', views.contact, name='contact'),
    path('upload/', views.upload_file, name='upload'),
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/<slug:supplier_slug>/', views.supplier_discounts, name='supplier_discounts'),
    path('clients/', views.client_list, name='client_list'),
    path('clients/<int:client_id>/', views.client_detail, name='client_detail'),
]