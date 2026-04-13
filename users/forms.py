import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import RegexValidator
from .models import CustomUser

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', required=True)
    last_name = forms.CharField(label='Фамилия', required=True)
    
    phone_regex = RegexValidator(
        regex=r'^[\d\s\+]+$', 
        message="Номер телефона может содержать только цифры, пробелы и знак плюса."
    )
    phone_number = forms.CharField(label='Номер телефона', validators=[phone_regex], required=True)
    email = forms.EmailField(label='Почта', required=True)
    
    role = forms.ChoiceField(
        label='Роль', 
        choices=CustomUser.ROLE_CHOICES, 
        widget=forms.RadioSelect,
        required=True
    )
    iin = forms.CharField(label='ИИН', required=False)

    # Новые поля для учеников с нужными виджетами
    grade_number = forms.ChoiceField(
        label='Класс', 
        choices=[('', 'Выберите класс...')] + CustomUser.GRADE_CHOICES, 
        required=False, 
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    grade_letter = forms.ChoiceField(
        label='Буква', 
        choices=CustomUser.LETTER_CHOICES, 
        required=False, 
        widget=forms.RadioSelect
    )
    subgroup = forms.ChoiceField(
        label='Подгруппа', 
        choices=CustomUser.SUBGROUP_CHOICES, 
        required=False, 
        widget=forms.RadioSelect
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name', 'last_name', 'patronymic', 'phone_number', 'email', 'role', 'iin', 'grade_number', 'grade_letter', 'subgroup')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = "Пароль"
        self.fields['password2'].label = "Повторить пароль"

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        grade_number = cleaned_data.get('grade_number')
        grade_letter = cleaned_data.get('grade_letter')
        subgroup = cleaned_data.get('subgroup')

        # Проверка класса только для учеников
        if role == 'student':
            if not grade_number:
                self.add_error('grade_number', 'Укажите ваш класс.')
            if not grade_letter:
                self.add_error('grade_letter', 'Укажите букву класса.')
            if not subgroup:
                self.add_error('subgroup', 'Укажите номер подгруппы.')
                
        return cleaned_data

    # ... метод clean_password1 остается без изменений ...

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if password:
            if len(password) < 8:
                raise forms.ValidationError('Пароль должен содержать минимум 8 символов.')
            if not re.search(r'\d', password):
                raise forms.ValidationError('Пароль должен содержать хотя бы одну цифру.')
            if not re.search(r'[^a-zA-Z0-9\.,а-яА-ЯёЁ\s]', password):
                raise forms.ValidationError('Добавьте хотя бы один спецсимвол (кроме точек и запятых).')
        return password

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Почта', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'patronymic', 'phone_number', 'email', 'avatar', 'grade_number', 'grade_letter', 'subgroup']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }