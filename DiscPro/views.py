from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ValidationError
from .models import Discount, Category, TagPost, UploadFiles, Supplier, Client, ClientProfile, DiscountUsage
from .forms import AddDiscountForm, UploadFileForm,  GPTQuestionForm
import uuid
import os
from django.conf import settings
from .services.yandex_gpt import ask_yandex_gpt

menu = [
    {'title': 'Главная', 'url_name': 'home'},
    {'title': 'О проекте', 'url_name': 'about'},
    {'title': 'Выгоды', 'url_name': 'benefits'},
    {'title': 'Доверие', 'url_name': 'trust'},
    {'title': 'Дисконты', 'url_name': 'discount_list'},
    {'title': 'Поставщики', 'url_name': 'supplier_list'},
    {'title': 'Клиенты', 'url_name': 'client_list'},
    {'title': 'Добавить акцию', 'url_name': 'addpage'},
    {'title': 'Загрузка файлов', 'url_name': 'upload'},
    {'title': 'Контакты', 'url_name': 'contact'},
]

def index(request):
    data = {'title': 'DiscountPRO', 'menu': menu}
    return render(request, 'DiscPro/index.html', data)

def discount_list(request):
    discounts = Discount.published.all()
    categories = Category.objects.all()
    tags = TagPost.objects.all()
    data = {
        'title': 'Дисконтные программы',
        'menu': menu,
        'posts': discounts,
        'categories': categories,
        'tags': tags,
        'current_category': None,
        'current_tag': None,
    }
    return render(request, 'DiscPro/discount_list.html', data)

def category_discounts(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    discounts = Discount.published.filter(cat=category)
    categories = Category.objects.all()
    tags = TagPost.objects.all()
    data = {
        'title': category.name,
        'menu': menu,
        'posts': discounts,
        'categories': categories,
        'tags': tags,
        'current_category': category,
        'current_tag': None,
    }
    return render(request, 'DiscPro/discount_list.html', data)

def tag_discounts(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    discounts = Discount.published.filter(tags=tag)
    categories = Category.objects.all()
    tags = TagPost.objects.all()
    data = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'posts': discounts,
        'categories': categories,
        'tags': tags,
        'current_category': None,
        'current_tag': tag,
    }
    return render(request, 'DiscPro/discount_list.html', data)

def category_tag_discounts(request, cat_slug, tag_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    tag = get_object_or_404(TagPost, slug=tag_slug)
    discounts = Discount.published.filter(cat=category, tags=tag)
    categories = Category.objects.all()
    tags = TagPost.objects.all()
    data = {
        'title': f'{category.name} | #{tag.tag}',
        'menu': menu,
        'posts': discounts,
        'categories': categories,
        'tags': tags,
        'current_category': category,
        'current_tag': tag,
    }
    return render(request, 'DiscPro/discount_list.html', data)

def discount_detail(request, discount_slug):
    discount = get_object_or_404(Discount, slug=discount_slug, is_published=Discount.Status.PUBLISHED)
    data = {
        'title': discount.title,
        'menu': menu,
        'post': discount,
    }
    return render(request, 'DiscPro/discount_detail.html', data)

def addpage(request):
    if request.method == 'POST':
        form = AddDiscountForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('discount_list')
    else:
        form = AddDiscountForm()
    return render(request, 'DiscPro/addpage.html', {'title': 'Добавление акции', 'menu': menu, 'form': form})

def about(request):
    data = {
        'title': 'О проекте',
        'menu': menu,
    }
    return render(request, 'DiscPro/about.html', data)

def benefits(request):
    data = {'title': 'Выгоды', 'menu': menu}
    return render(request, 'DiscPro/benefits.html', data)

def trust(request):
    testimonials = [
        {'text': 'С DiscountPro мы увеличили повторные покупки на 42%', 'author': 'Иван Ожгихин', 'position': 'Директор по маркетингу', 'initials': 'ИО'},
        {'text': 'Невероятно удобная аналитика!', 'author': 'Злата Мякинина', 'position': 'Владелец сети магазинов', 'initials': 'ЗМ'},
        {'text': 'Внедрение заняло всего 4 дня', 'author': 'Максим Прочувайлов', 'position': 'CEO, Fashion Store', 'initials': 'МП'},
    ]
    data = {'title': 'Доверие', 'menu': menu, 'testimonials': testimonials}
    return render(request, 'DiscPro/trust.html', data)

def contact(request):
    gpt_answer = None
    form = GPTQuestionForm()
    
    if request.method == 'POST':
        form = GPTQuestionForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data['question']
            gpt_answer = ask_yandex_gpt(question)
    
    context = {
        'title': 'Контакты | DiscountPRO',
        'menu': menu,
        'yandex_maps_api_key': settings.YANDEX_MAPS_API_KEY,
        'office_address': 'г. Казань ул. Карла Маркса 72кО',
        'form': form,
        'gpt_answer': gpt_answer,
    }
    return render(request, 'DiscPro/contact.html', context)

def upload_file(request):
    uploaded_file = None
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
            uploaded_file = form.cleaned_data['file'].name
    else:
        form = UploadFileForm()
    
    # Получаем список всех загруженных файлов
    files = UploadFiles.objects.all().order_by('-upload_date')
    
    data = {
        'title': 'Загрузка файлов',
        'menu': menu,
        'form': form,
        'uploaded_file': uploaded_file,
        'files': files,
    }
    return render(request, 'DiscPro/upload.html', data)

def supplier_list(request):
    suppliers = Supplier.objects.all()
    data = {
        'title': 'Поставщики',
        'menu': menu,
        'suppliers': suppliers,
    }
    return render(request, 'DiscPro/supplier_list.html', data)

def supplier_discounts(request, supplier_slug):
    supplier = get_object_or_404(Supplier, slug=supplier_slug)
    discounts = Discount.objects.filter(supplier=supplier, is_published=Discount.Status.PUBLISHED)
    data = {
        'title': f'Дисконты от {supplier.name}',
        'menu': menu,
        'posts': discounts,
        'supplier': supplier,
        'categories': Category.objects.all(),
        'tags': TagPost.objects.all(),
    }
    return render(request, 'DiscPro/discount_list.html', data)

def client_list(request):
    clients = Client.objects.all()
    data = {
        'title': 'Клиенты',
        'menu': menu,
        'clients': clients,
    }
    return render(request, 'DiscPro/client_list.html', data)

def client_detail(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    usages = DiscountUsage.objects.filter(client=client)
    data = {
        'title': f'Клиент: {client}',
        'menu': menu,
        'client': client,
        'usages': usages,
    }
    return render(request, 'DiscPro/client_detail.html', data)