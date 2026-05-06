from django.db import models
from django.urls import reverse

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Discount.Status.PUBLISHED)

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Название категории")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True, verbose_name="Тег")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag_discounts', kwargs={'tag_slug': self.slug})


class Supplier(models.Model):
    """Модель поставщика - для связи Один ко многим с Discount"""
    name = models.CharField(max_length=200, verbose_name="Название поставщика")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    contact_person = models.CharField(max_length=100, verbose_name="Контактное лицо", blank=True)
    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True)
    email = models.EmailField(verbose_name="Email", blank=True)
    website = models.URLField(verbose_name="Сайт", blank=True)
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    
    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('supplier_discounts', kwargs={'supplier_slug': self.slug})
    
class Discount(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255, verbose_name="Название акции")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Описание")
    discount_percent = models.PositiveSmallIntegerField(default=0, verbose_name="Скидка (%)")
    valid_from = models.DateField(verbose_name="Действует с")
    valid_to = models.DateField(verbose_name="Действует до")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.IntegerField(choices=Status.choices, default=Status.DRAFT, verbose_name="Статус")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категория", null=True, blank=True)
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags', verbose_name="Теги")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, null=True, verbose_name="Изображение")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='discounts', verbose_name="Поставщик")
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-time_create']
        indexes = [models.Index(fields=['time_create']), models.Index(fields=['slug'])]
        verbose_name = "Дисконтная программа"
        verbose_name_plural = "Дисконтные программы"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('discount_detail', kwargs={'discount_slug': self.slug})
    
class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model', verbose_name="Файл")
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")
    
    class Meta:
        verbose_name = "Загруженный файл"
        verbose_name_plural = "Загруженные файлы"
    
    def __str__(self):
        return self.file.name
    


class Client(models.Model):
    """Модель клиента - для связи Один к одному с дополнительной информацией"""
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, verbose_name="Пользователь", null=True, blank=True)
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.TextField(verbose_name="Адрес", blank=True)
    birth_date = models.DateField(verbose_name="Дата рождения", null=True, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    total_purchases = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Сумма покупок")
    discount_card_number = models.CharField(max_length=50, unique=True, verbose_name="Номер дисконтной карты", blank=True)
    
    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ['-total_purchases']
    
    def __str__(self):
        if self.user:
            return self.user.username
        return f"Клиент #{self.id}"
    
    def get_absolute_url(self):
        return reverse('client_detail', kwargs={'client_id': self.id})


class ClientProfile(models.Model):
    """Дополнительный профиль клиента - расширение OneToOne связи"""
    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='profile', verbose_name="Клиент")
    loyalty_level = models.CharField(max_length=50, default="Обычный", verbose_name="Уровень лояльности")
    bonus_points = models.IntegerField(default=0, verbose_name="Бонусные баллы")
    personal_discount = models.IntegerField(default=0, verbose_name="Персональная скидка (%)")
    preferences = models.TextField(blank=True, verbose_name="Предпочтения")
    
    class Meta:
        verbose_name = "Профиль клиента"
        verbose_name_plural = "Профили клиентов"
    
    def __str__(self):
        return f"Профиль: {self.client}"


class DiscountUsage(models.Model):
    """Модель использования дисконта - для связи Один ко многим от Discount"""
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, related_name='usages', verbose_name="Дисконт")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='discount_usages', verbose_name="Клиент")
    used_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата использования")
    purchase_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма покупки")
    saved_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сэкономлено")
    
    class Meta:
        verbose_name = "Использование дисконта"
        verbose_name_plural = "Использования дисконтов"
        ordering = ['-used_at']
    
    def __str__(self):
        return f"{self.discount.title} - {self.client} - {self.used_at}"