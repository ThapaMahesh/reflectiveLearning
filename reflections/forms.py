from django import forms
from django.forms import ModelForm
from .models import Prompts, Reflection, Discussion
from django_select2.forms import Select2TagWidget


CHOICES = (('1', 'Yes',), ('0', 'No',))

REFLECTION_CHOICES = (
            ('4', 'Demonstrates superior skills of critical thinking, understanding of the presented concepts. The reflection is insighful and thoroughly analysed with well supported viewpoints.'),
            ('3', 'Demonstrates skills of thoughtful understanding of the concept with general supportive viewpoints.'),
            ('2', 'Demonstrates minimal skill of reflection and understanding of the concepts. The thoughts and arguments are not properly supported. The reflection could use revision.'),
            ('1', 'Demonstrates lack of reflection skills and the thoughts and arguments are not supported. The reflection should be revised.')
    )

EXPERIENCE_CHOICES = (
            ('4', 'Discusses learning experience related and specific experience to support reflection.'),
            ('3', 'Discusses relavant or closely related experience to support reflection.'),
            ('2', 'Vaguely explains the previous knowledge to support reflection.'),
            ('1', 'No previous experience are disucssed.')
    )

LEARNING_CHOICES = (
            ('4', 'Shows high level understanding of the experience by presenting multiple learning scenarious with supported arguments.'),
            ('3', 'Shows general understanding of the experience and presents at least one scenario with supported arguments.'),
            ('2', 'Learnings shows lack of understanding of the experience and the presented learnings are not supported or lacks support.'),
            ('1', 'Shows no clear understanding of the experience and learnings lack support or shows no implications of learning outcomes.')
    )

class PromptsForm(ModelForm):
    situation = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'class':'form-control' }), error_messages={'required': 'Situation is Required'})
    has_experience = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class':'form-check-input experience_check'}), choices=CHOICES)
    experience = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'class':'form-control' }), required=False)
    experience_helpful = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'class':'form-control' }), required=False)
    factors = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'class':'form-control' }), error_messages={'required': 'Factors in Reasoning section is Required'})
    emotions = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'class':'form-control' }), error_messages={'required': 'Emotions in Reasoning section is Required'})
    solutions = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'class':'form-control' }), error_messages={'required': 'Solutions in Conclusion section is Required'})
    learnings = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'class':'form-control' }), error_messages={'required': 'Learnings in Conclusion section is Required'})
    current = forms.CharField(widget=forms.HiddenInput)

    class Meta:
        model = Prompts
        fields = ['situation', 'has_experience', 'experience', 'experience_helpful', 'factors', 'emotions', 'solutions', 'learnings', 'current']
        exclude = ['updated_by_id', 'reflection_id']


class ReflectionForm(ModelForm):
    is_group = forms.CharField(widget=forms.HiddenInput)
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), error_messages={'required': 'Title is Required'})
    tags = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control keywords', 'data-role':"tagsinput"}), error_messages={'required': 'Tags is Required'})
    
    class Meta:
        model = Reflection
        fields = ['is_group', 'title', 'tags']
        exclude = ['created_by_id']

class DiscussionForm(ModelForm):
    feedback = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))

    class Meta:
        model = Discussion
        fields = ['feedback']

class FeedbackForm(ModelForm):
    reflection_feedback = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class':'form-check-input'}), choices=REFLECTION_CHOICES, error_messages={'required': 'Feedback on reflection is required'})
    experience_feedback = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class':'form-check-input'}), choices=EXPERIENCE_CHOICES, error_messages={'required': 'Feedback on experience is required'})
    learning_feedback = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class':'form-check-input'}), choices=LEARNING_CHOICES, error_messages={'required': 'Feedback on learning is required'})
    feedback = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), error_messages={'required': 'Your constructive feedback is required'})

    class Meta:
        model = Discussion
        fields = ['reflection_feedback', 'experience_feedback', 'learning_feedback', 'feedback']