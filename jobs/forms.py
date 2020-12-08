from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import Grade, Specialty


class NewUser(UserCreationForm):
    password1 = forms.CharField(
        label=_("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Повторите пароль"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Повторите введеный пароль"),
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')
        labels = {
            'username': 'Логин',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин')
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )


class ApplicationForm(forms.Form):
    written_username = forms.CharField(label='Фамилия и имя')
    written_phone = forms.CharField(label='Номер телефона')
    written_cover_letter = forms.CharField(widget=forms.Textarea, label='Письмо')


class CompanyForm(forms.Form):
    name = forms.CharField(max_length=64, required=True, label='Название компании')
    location = forms.CharField(max_length=64, required=True, label='География')
    logo = forms.ImageField(required=False, label='Логотип')
    description = forms.CharField(widget=forms.Textarea, required=True, label='Информация о компании')
    employee_count = forms.IntegerField(required=True, label='Количество человек в компании')


class VacancyForm(forms.Form):
    title = forms.CharField(max_length=64, required=False, label='Название вакансии')
    specialty = forms.ModelChoiceField(queryset=Specialty.objects.all(), required=False, label='Специализация')
    salary_min = forms.IntegerField(required=False, label='Зарплата от')
    salary_max = forms.IntegerField(required=False, label='Зарплата до')
    skills = forms.CharField(widget=forms.Textarea, required=False, label='Требуемые навыки')
    description = forms.CharField(widget=forms.Textarea, required=False, label='Описание вакансии')


class ResumeForm(forms.Form):
    name = forms.CharField(required=False, label='Имя')
    surname = forms.CharField(required=False, label='Фамилия')
    status = forms.BooleanField(label='Готов к работе', required=False)
    salary = forms.IntegerField(required=False, label='Ожидаемое вознаграждение')
    specialty = forms.ModelChoiceField(queryset=Specialty.objects.all(), required=False, label='Специализация')
    grade = forms.ModelChoiceField(queryset=Grade.objects.all(), required=False, label='Квалификация')
    education = forms.CharField(widget=forms.Textarea, required=False, label='Образование')
    experience = forms.CharField(widget=forms.Textarea, required=False, label='Опыт работы')
    portfolio = forms.URLField(required=False, label='Ссылка на порфтолио')


class SearchForm(forms.Form):
    s = forms.CharField(label='')
