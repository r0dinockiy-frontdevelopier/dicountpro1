from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from .models import Discount, Category

def validate_russian(value):
    allowed_chars = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя0123456789- "
    if not all(c in allowed_chars for c in value):
        raise ValidationError("Допустимы только русские буквы, цифры, дефис и пробел")

class AddDiscountForm(forms.ModelForm):
    # Переопределяем поля с валидаторами
    title = forms.CharField(
        max_length=255,
        min_length=5,
        label="Название акции",
        widget=forms.TextInput(attrs={'class': 'form-input'}),
        validators=[validate_russian],
        error_messages={
            'min_length': 'Слишком короткое название (минимум 5 символов)',
            'required': 'Название обязательно'
        }
    )
    
    slug = forms.SlugField(
        max_length=255,
        label="URL",
        widget=forms.TextInput(attrs={'class': 'form-input'}),
        validators=[MinLengthValidator(5, message="Минимум 5 символов")]
    )
    
    discount_percent = forms.IntegerField(
        min_value=0,
        max_value=100,
        label="Скидка (%)",
        widget=forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'max': 100})
    )
    
    class Meta:
        model = Discount
        fields = ['title', 'slug', 'description', 'discount_percent', 'valid_from', 'valid_to', 'is_published', 'cat', 'photo']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 5}),
            'valid_from': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'valid_to': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'photo': forms.FileInput(attrs={'class': 'form-input'}),
        }
        labels = {
            'description': 'Описание',
            'valid_from': 'Действует с',
            'valid_to': 'Действует до',
            'is_published': 'Опубликовано',
            'cat': 'Категория',
            'photo': 'Изображение',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = "Выберите категорию"
        self.fields['cat'].required = True
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title and len(title) > 50:
            raise ValidationError("Длина названия не должна превышать 50 символов")
        return title
    
    def clean(self):
        cleaned_data = super().clean()
        valid_from = cleaned_data.get('valid_from')
        valid_to = cleaned_data.get('valid_to')
        
        if valid_from and valid_to and valid_from > valid_to:
            raise ValidationError("Дата начала не может быть позже даты окончания")
        
        return cleaned_data

class UploadFileForm(forms.Form):
    file = forms.FileField(label="Выберите файл")

class GPTQuestionForm(forms.Form):
    question = forms.CharField(
        label='Ваш вопрос',
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Спросите у нашего ИИ-ассистента о дисконтных программах...'}),
        max_length=500,
        required=True,
        error_messages={
            'required': 'Пожалуйста, введите вопрос',
            'max_length': 'Вопрос не должен превышать 500 символов'
        }
    )