from django import template
from ..models import Category, TagPost

register = template.Library()

# Данные для выгод (в будущем можно брать из БД)
benefits_list = [
    {
        'icon': 'fas fa-chart-bar',
        'title': 'Увеличение выручки',
        'text': 'Рост продаж до 35% благодаря персонализированным предложениям и точечным скидкам'
    },
    {
        'icon': 'fas fa-filter',
        'title': 'Точная сегментация',
        'text': 'Анализ поведения клиентов и создание таргетированных дисконтных программ'
    },
    {
        'icon': 'fas fa-clock',
        'title': 'Экономия времени',
        'text': 'Автоматизация рутинных задач экономит до 20 часов работы в неделю'
    },
    {
        'icon': 'fas fa-chart-pie',
        'title': 'Полная аналитика',
        'text': 'Детальные отчеты по эффективности каждой акции и скидки в режиме реального времени'
    },
    {
        'icon': 'fas fa-shield-alt',
        'title': 'Контроль мошенничества',
        'text': 'Защита от злоупотреблений скидками и дублирования карт лояльности'
    },
    {
        'icon': 'fas fa-mobile-alt',
        'title': 'Мобильное приложение',
        'text': 'Управляйте программами лояльности через удобное мобильное приложение'
    },
    {
        'icon': 'fas fa-database',
        'title': 'Централизованные данные',
        'text': 'Единая база клиентов и транзакций для всех точек продаж'
    },
    {
        'icon': 'fas fa-rocket',
        'title': 'Быстрый запуск',
        'text': 'Внедрение и интеграция системы за 3-5 дней без остановки работы'
    },
]


@register.inclusion_tag('DiscPro/includes/benefits_grid.html')
def show_benefits():
    """
    Включающий тег для отображения сетки преимуществ.
    Использование в шаблоне:
        {% load discpro_tags %}
        {% show_benefits %}
    """
    return {'benefits': benefits_list}

@register.inclusion_tag('DiscPro/list_categories.html')
def show_categories(cat_selected_id=0):
    cats = Category.objects.all()
    return {"cats": cats, "cat_selected": cat_selected_id}

@register.inclusion_tag('DiscPro/list_tags.html')
def show_all_tags():
    return {"tags": TagPost.objects.all()}