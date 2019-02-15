import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import PromptsForm, ReflectionForm, DiscussionForm
from helpers.preprocess import PreProcess
from django.conf import settings
from reflections.models import Reflection


def index(reflectionText):
    processData = PreProcess(reflectionText)
    readability = processData.complexity()
    sentiment = processData.sentiment()
    wordFrequency = processData.wordFrequency()
    wordDict = {word[0]:word[1] for word in wordFrequency}
    return {'readability': readability, 'sentiment': sentiment, 'wordFrequency': wordDict}

def test(request):
    return HttpResponse(json.dumps(index("Hello World! This is a test message")))

@login_required
def addReflection(request):
    template = loader.get_template('reflections/add-reflection.html')
    context = {
    }
    return HttpResponse(template.render(context, request))

@login_required
def postReflection(request):
    if request.method == 'POST':
        allInputs = request.POST.copy()
        promptsForm = PromptsForm(allInputs)
        reflectionForm = ReflectionForm(allInputs)
        if promptsForm.is_valid() and reflectionForm.is_valid():
            allText = ""
            for key, value in request.POST.items():
                if key != 'has_experience' and key != 'csrfmiddlewaretoken' and key != 'current' and key != 'is_group' and key != 'title' and key != 'tags':
                    allText = allText + ' ' + value

            textAnalysis = index(allText)

            reflectionSave = reflectionForm.save(commit=False)
            reflectionSave.created_by = request.user
            reflectionSave.save()

            promptSave = promptsForm.save(commit=False)
            promptSave.updated_by = request.user
            promptSave.reflection = reflectionSave
            promptSave.readability = json.dumps(textAnalysis['readability'])
            promptSave.wordFrequency = json.dumps(textAnalysis['wordFrequency'])
            promptSave.sentiment = textAnalysis['sentiment']['compound']
            promptSave.save()

            messages.success(request, 'Your data was saved successfully!')
            return HttpResponseRedirect(reverse('reflections:view', args=[reflectionSave.id]))
    else:
        promptsForm = PromptsForm()
        reflectionForm = ReflectionForm()
        promptsForm.initial['current'] = 1
        reflectionForm.initial['is_group'] = 0
    return render(request, 'reflections/home.html', {'promptsForm': promptsForm, 'reflectionForm': reflectionForm, 'type': 'add'})

@login_required
def viewReflection(request, reflection_id):
    reflection = get_object_or_404(Reflection, id=reflection_id)
    details = reflection.reflection_prompts.all()[0]
    details.readability = json.loads(details.readability)
    details.wordFrequency = json.loads(details.wordFrequency)

    if request.method == "POST":
        allInputs = request.POST.copy()
        discussionForm = DiscussionForm(allInputs)
        if discussionForm.is_valid():
            discussionSave = discussionForm.save(commit=False)
            discussionSave.created_by = request.user
            discussionSave.reflection = reflection
            discussionSave.save()

            messages.success(request, 'Your data was saved successfully!')
            return HttpResponseRedirect(reverse('reflections:view', args=[reflection.id]))
    else:
        discussionForm = DiscussionForm()

    return render(request, 'reflections/view-reflection.html', {'reflection': reflection, 'details': details, 'discussionForm': discussionForm})

@login_required
def deleteReflection(request, reflection_id):
    reflection = get_object_or_404(Reflection, id=reflection_id)

    # reflection.reflection.delete()
    reflection.delete()
    messages.success(request, 'Your data was removed successfully!')
    return HttpResponseRedirect(reverse('myreflections'))

@login_required
def editReflection(request, reflection_id):
    reflection = get_object_or_404(Reflection, id=reflection_id)
    prompt = reflection.reflection_prompts.all()[0]

    if request.method == 'POST':
        allInputs = request.POST.copy()
        promptsForm = PromptsForm(allInputs or None, instance=prompt)
        reflectionForm = ReflectionForm(allInputs or None, instance=reflection)
        if promptsForm.is_valid() and reflectionForm.is_valid():
            allText = ""
            for key, value in request.POST.items():
                if key != 'has_experience' and key != 'csrfmiddlewaretoken' and key != 'current' and key != 'is_group' and key != 'title' and key != 'tags':
                    allText = allText + ' ' + value

            textAnalysis = index(allText)

            reflectionSave = reflectionForm.save(commit=False)
            reflectionSave.created_by = request.user
            reflectionSave.save()

            promptSave = promptsForm.save(commit=False)
            promptSave.updated_by = request.user
            promptSave.reflection = reflectionSave
            promptSave.readability = json.dumps(textAnalysis['readability'])
            promptSave.wordFrequency = json.dumps(textAnalysis['wordFrequency'])
            promptSave.sentiment = textAnalysis['sentiment']['compound']
            promptSave.save()

            messages.success(request, 'Your data was updated successfully!')
            return HttpResponseRedirect(reverse('reflections:view', args=[reflectionSave.id]))
    else:
        promptsForm = PromptsForm(instance=prompt)
        reflectionForm = ReflectionForm(instance=reflection)
        promptsForm.initial['has_experience'] = int(prompt.has_experience)
    return render(request, 'reflections/home.html', {'promptsForm': promptsForm, 'reflectionForm': reflectionForm, 'type': 'edit'})