from django.contrib import admin, messages
from django.utils.html import mark_safe
from .models import Discount, Category, TagPost, UploadFiles, Supplier, Client, ClientProfile, DiscountUsage

class DiscountFilter(admin.SimpleListFilter):
    title = 'Размер скидки'
    parameter_name = 'discount_status'
    
    def lookups(self, request, model_admin):
        return [
            ('high', 'Высокая (50%+)'),
            ('medium', 'Средняя (20-49%)'),
            ('low', 'Низкая (до 19%)'),
        ]
    
    def queryset(self, request, queryset):
        if self.value() == 'high':
            return queryset.filter(discount_percent__gte=50)
        if self.value() == 'medium':
            return queryset.filter(discount_percent__range=(20, 49))
        if self.value() == 'low':
            return queryset.filter(discount_percent__lte=19)
        return queryset

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'discount_percent', 'valid_from', 'valid_to', 'is_published', 'cat', 'post_photo')
    list_display_links = ('id', 'title')
    list_editable = ('is_published',)
    ordering = ['-time_create', 'title']
    list_per_page = 10
    actions = ['set_published', 'set_draft']
    search_fields = ['title', 'description', 'cat__name']
    list_filter = [DiscountFilter, 'is_published', 'cat']
    readonly_fields = ['time_create', 'time_update', 'post_photo']
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'cat')
        }),
        ('Параметры скидки', {
            'fields': ('discount_percent', 'valid_from', 'valid_to')
        }),
        ('Изображение', {
            'fields': ('photo', 'post_photo')
        }),
        ('Содержание', {
            'fields': ('description',)
        }),
        ('Статус', {
            'fields': ('is_published', 'time_create', 'time_update')
        }),
    )
    
    @admin.display(description="Инфо")
    def brief_info(self, discount: Discount):
        return f"Описание: {len(discount.description)} симв."
    
    @admin.display(description="Изображение")
    def post_photo(self, discount: Discount):
        if discount.photo:
            return mark_safe(f'<img src="{discount.photo.url}" width="80" height="80" style="object-fit: cover; border-radius: 8px;">')
        return "Без фото"
    
    @admin.action(description="Опубликовать выбранные программы")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Discount.Status.PUBLISHED)
        self.message_user(request, f"Опубликовано {count} программ(ы).")
    
    @admin.action(description="Снять с публикации")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Discount.Status.DRAFT)
        self.message_user(request, f"{count} программ(ы) сняты с публикации!", messages.WARNING)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    ordering = ['name']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(TagPost)
class TagPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'slug')
    list_display_links = ('id', 'tag')
    ordering = ['tag']
    prepopulated_fields = {'slug': ('tag',)}
    search_fields = ['tag']

@admin.register(UploadFiles)
class UploadFilesAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'upload_date')
    list_display_links = ('id', 'file')

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'contact_person', 'phone', 'email')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'contact_person', 'email')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('created_at',)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone', 'discount_card_number', 'total_purchases')
    list_display_links = ('id', 'user')
    search_fields = ('user__username', 'phone', 'discount_card_number')
    list_filter = ('registration_date',)

@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'loyalty_level', 'bonus_points', 'personal_discount')
    list_display_links = ('id', 'client')
    list_filter = ('loyalty_level',)

@admin.register(DiscountUsage)
class DiscountUsageAdmin(admin.ModelAdmin):
    list_display = ('id', 'discount', 'client', 'used_at', 'purchase_amount', 'saved_amount')
    list_display_links = ('id', 'discount')
    list_filter = ('used_at',)
    search_fields = ('discount__title', 'client__user__username')