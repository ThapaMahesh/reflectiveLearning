from django import forms
from django.forms import ModelForm
from .models import Project, Member, Group



class ProjectForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control' }))
    description = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'class':'form-control' }))
    start_date = forms.CharField(widget=forms.DateInput(format="%Y-%m-%d", attrs={'class':'form-control' }))
    end_date = forms.CharField(widget=forms.DateInput(format="%Y-%m-%d", attrs={'class':'form-control' }))

    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date']