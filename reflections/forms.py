from django import forms
from django.forms import ModelForm
from .models import Prompts, Reflection, Discussion
from django_select2.forms import Select2TagWidget


CHOICES = (('1', 'Yes',), ('0', 'No',))


class PromptsForm(ModelForm):
    situation = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'class':'form-control' }))
    has_experience = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class':'form-check-input experience_check'}), choices=CHOICES)
    experience = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'class':'form-control' }))
    experience_helpful = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'class':'form-control' }))
    factors = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'class':'form-control' }))
    emotions = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'class':'form-control' }))
    solutions = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'class':'form-control' }))
    learnings = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'class':'form-control' }))
    current = forms.CharField(widget=forms.HiddenInput)

    class Meta:
        model = Prompts
        fields = ['situation', 'has_experience', 'experience', 'experience_helpful', 'factors', 'emotions', 'solutions', 'learnings', 'current']
        exclude = ['updated_by_id', 'reflection_id']


class ReflectionForm(ModelForm):
    is_group = forms.CharField(widget=forms.HiddenInput)
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    tags = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control keywords'}))

    class Meta:
        model = Reflection
        fields = ['is_group', 'title', 'tags']
        exclude = ['created_by_id']

class DiscussionForm(ModelForm):
    feedback = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))

    class Meta:
        model = Discussion
        fields = ['feedback']