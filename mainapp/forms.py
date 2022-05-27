from django import forms
from .models import building

class buildingForm(forms.ModelForm):
    class Meta:
        model = building
        fields = "__all__"