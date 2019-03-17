from django import forms
# from django.forms import forms
from reflections.models import Tags

class SearchForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'width':"100%", 'class':'form-control' }), required=False)
    tags = forms.ModelChoiceField(widget=forms.Select(attrs={'class':'form-control', 'multiple':'multiple'}), queryset=Tags.objects.all(), empty_label=None, required=False)
    # tags = forms.CharField(widget=forms.TextInput(attrs={'width':"100%", 'class':'form-control' }), required=False)
    start_date = forms.CharField(widget=forms.DateInput(format="%Y-%m-%d", attrs={'class':'form-control' }), required=False)
    end_date = forms.CharField(widget=forms.DateInput(format="%Y-%m-%d", attrs={'class':'form-control' }), required=False)
    include_group = forms.BooleanField(required=False, initial=False, label='Include Group')

class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    subject = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    # email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'class':'form-control' }))