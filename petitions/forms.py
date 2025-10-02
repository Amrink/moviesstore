from django import forms
from .models import Petition

class PetitionForm(forms.ModelForm):
    class Meta:
        model = Petition
        fields = ['movie_title', 'description']
        widgets = {
            'movie_title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),

        }
