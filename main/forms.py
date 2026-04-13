from django import forms
from .models import Appeal

class AppealForm(forms.ModelForm):
    class Meta:
        model = Appeal
        fields = ['name', 'contact_info', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_info': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }