import json
from googletrans import Translator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import PromptsForm, ReflectionForm, DiscussionForm, FeedbackForm
from helpers.preprocess import PreProcess
from django.conf import settings
from datetime import datetime
from reflections.models import Reflection, Discussion, Tags
from projects.models import Group
from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def index(reflectionText, norsk):
    processData = PreProcess(reflectionText, norsk)
    readability = processData.complexity()
    sentiment = processData.sentiment()
    wordFrequency = processData.wordFrequency()
    wordDict = {word[0]:word[1] for word in wordFrequency}
    return {'readability': readability, 'sentiment': sentiment, 'wordFrequency': wordDict}

def test(request):
    return HttpResponse(json.dumps(index("Hello World! This is a test message")))


@login_required
def postReflection(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    reflection_type = 'group' if request.GET.get('type') == "group" else 'individual'

    group_members = [eachMember.user_id for eachMember in group.members.all()]

    if request.user.id not in group_members:
        messages.error(request, 'User is not member of the requested group')
        return HttpResponseRedirect(reverse('pages:dashboard'))

    if request.method == 'POST':
        allInputs = request.POST.copy()
        promptsForm = PromptsForm(allInputs)
        reflectionForm = ReflectionForm(allInputs)
        if promptsForm.is_valid() and reflectionForm.is_valid():
            allText = ""
            for key, value in request.POST.items():
                if key != 'has_experience' and key != 'csrfmiddlewaretoken' and key != 'current' and key != 'is_group' and key != 'title' and key != 'tags':
                    if request.POST['has_experience'] == "0" and (key == 'experience' or key == 'experience_helpful'):
                        # add nothing
                        value = ''
                    allText = allText + ' ' + value

            if request.POST['has_experience'] == "1" and (request.POST['experience'] == "" or request.POST['experience_helpful'] == ""):
                messages.error(request, 'Experience data is missing.')
                return render(request, 'reflections/home.html', {'promptsForm': promptsForm, 'reflectionForm': reflectionForm, 'type': 'add'})

            textAnalysis = index(allText, request.user.norsk)
            if request.user.norsk:
                translator = Translator()
                translation_text = translator.translate(allText)
                new_textAnalysis = index(translation_text.text, request.user.norsk)
                textAnalysis['sentiment'] = new_textAnalysis['sentiment']


            reflectionSave = reflectionForm.save(commit=False)
            # reflectionSave.tags = ",".join(str(x) for x in allInputs.getlist('tags'))
            reflectionSave.created_by = request.user
            reflectionSave.updated_by = request.user
            reflectionSave.group = group
            reflectionSave.save()

            tag_list = allInputs.getlist('tags')[0].split(',')

            for eachTag in tag_list:
                tag_lower = eachTag.lower()
                tag_exits = Tags.objects.filter(name=tag_lower).exists()
                if tag_exits == False:
                    new_tag = Tags.objects.create(name=tag_lower)
                else:
                    new_tag = Tags.objects.filter(name=tag_lower).first()
                new_tag.reflection.add(reflectionSave)

            promptSave = promptsForm.save(commit=False)
            promptSave.updated_by = request.user
            promptSave.reflection = reflectionSave

            if request.POST['has_experience'] == "0":
                promptSave.experience = ""
                promptSave.experience_helpful = ""

            promptSave.readability = json.dumps(textAnalysis['readability'])
            promptSave.wordFrequency = json.dumps(textAnalysis['wordFrequency'])

            promptSave.sentiment = textAnalysis['sentiment']['compound']
            promptSave.save()

            messages.success(request, 'Your data was saved successfully!')
            return HttpResponseRedirect(reverse('reflections:view', args=[reflectionSave.id, group.id]))
        else:
            messages.error(request, 'Error while saving data!')
    else:
        promptsForm = PromptsForm()
        reflectionForm = ReflectionForm()
        promptsForm.initial['current'] = 1
        reflectionForm.initial['is_group'] = 1 if request.GET.get('type') == "group" else 0
    return render(request, 'reflections/add-reflection.html', {'reflection_type': reflection_type, 'group': group, 'promptsForm': promptsForm, 'reflectionForm': reflectionForm, 'type': 'add'})

@login_required
def viewReflection(request, reflection_id, group_id):
    group = get_object_or_404(Group, id=group_id)
    reflection = get_object_or_404(Reflection, id=reflection_id)

    if reflection.group != group:
        messages.error(request, 'Invalid Request!')
        return HttpResponseRedirect(reverse('pages:dashboard'))

    group_members = [eachMember.user_id for eachMember in group.members.all()]
    if request.user.id not in group_members:
        messages.error(request, 'User is not member of the requested group')
        return HttpResponseRedirect(reverse('pages:dashboard'))

    REFLECTION_CHOICES = {'4': 'Demonstrates superior skills of critical thinking, understanding of the presented concepts. The reflection is insighful and thoroughly analysed with well supported viewpoints.',
                '3': 'Demonstrates skills of thoughtful understanding of the concept with general supportive viewpoints.',
                '2': 'Demonstrates minimal skill of reflection and understanding of the concepts. The thoughts and arguments are not properly supported. The reflection could use revision.',
                '1': 'Demonstrates lack of reflection skills and the thoughts and arguments are not supported. The reflection should be revised.'
                }

    EXPERIENCE_CHOICES = {'4': 'Discusses learning experience related and specific experience to support reflection.',
                '3': 'Discusses relavant or closely related experience to support reflection.',
                '2': 'Vaguely explains the previous knowledge to support reflection.',
                '1': 'No previous experience are disucssed.'
        }

    LEARNING_CHOICES = {
                '4': 'Shows high level understanding of the experience by presenting multiple learning scenarious with supported arguments.',
                '3': 'Shows general understanding of the experience and presents at least one scenario with supported arguments.',
                '2': 'Learnings shows lack of understanding of the experience and the presented learnings are not supported or lacks support.',
                '1': 'Shows no clear understanding of the experience and learnings lack support or shows no implications of learning outcomes.'
        }

    details = reflection.reflection_prompts.all()[0]
    details.readability = json.loads(details.readability)
    details.wordFrequency = json.loads(details.wordFrequency)

    if request.method == "POST":
        allInputs = request.POST.copy()
        discussionForm = FeedbackForm(allInputs) if not reflection.is_group else DiscussionForm(allInputs)
        if discussionForm.is_valid():
            discussionSave = discussionForm.save(commit=False)
            discussionSave.created_by = request.user
            discussionSave.reflection = reflection
            discussionSave.save()

            messages.success(request, 'Your data was saved successfully!')
            return HttpResponseRedirect(reverse('reflections:view', args=[reflection.id, group_id]))
    else:
        discussionForm = FeedbackForm() if not reflection.is_group else DiscussionForm()

    return render(request, 'reflections/view-reflection.html', {'LEARNING_CHOICES': LEARNING_CHOICES, 'EXPERIENCE_CHOICES': EXPERIENCE_CHOICES, 'REFLECTION_CHOICES': REFLECTION_CHOICES, 'group': group, 'reflection': reflection, 'details': details, 'discussionForm': discussionForm})

@login_required
def deleteReflection(request, reflection_id, group_id):
    group = get_object_or_404(Group, id=group_id)
    reflection = get_object_or_404(Reflection, id=reflection_id)

    if reflection.group != group:
        messages.error(request, 'Invalid Request!')
        return HttpResponseRedirect(reverse('pages:dashboard'))

    if reflection.created_by != request.user:
        messages.error(request, 'Unauthorized request!')
        return HttpResponseRedirect(reverse('pages:dashboard'))        

    # reflection.reflection.delete()
    reflection.delete()
    messages.success(request, 'Your data was removed successfully!')
    return HttpResponseRedirect(reverse('projects:view-group', args=[group.project_id, group_id]))

@login_required
def editReflection(request, reflection_id, group_id):
    group = get_object_or_404(Group, id=group_id)
    reflection = get_object_or_404(Reflection, id=reflection_id)

    if reflection.group != group:
        messages.error(request, 'Invalid Request!')
        return HttpResponseRedirect(reverse('pages:dashboard'))

    group_members = [eachMember.user_id for eachMember in group.members.all()]

    if request.user.id not in group_members:
        messages.error(request, 'User is not member of the requested group')
        return HttpResponseRedirect(reverse('pages:dashboard'))

    if reflection.created_by != request.user and not reflection.is_group:
        messages.error(request, 'Unauthorized request')
        return HttpResponseRedirect(reverse('pages:dashboard'))

    prompt = reflection.reflection_prompts.all()[0]

    if request.method == 'POST':
        allInputs = request.POST.copy()
        promptsForm = PromptsForm(allInputs or None, instance=prompt)
        reflectionForm = ReflectionForm(allInputs or None, instance=reflection)
        if promptsForm.is_valid() and reflectionForm.is_valid():
            allText = ""
            for key, value in request.POST.items():
                if key != 'has_experience' and key != 'csrfmiddlewaretoken' and key != 'current' and key != 'is_group' and key != 'title' and key != 'tags':
                    if request.POST['has_experience'] == "0" and (key == 'experience' or key == 'experience_helpful'):
                        # add nothing
                        value = ''
                    allText = allText + ' ' + value

            if request.POST['has_experience'] == "1" and (request.POST['experience'] == "" or request.POST['experience_helpful'] == ""):
                messages.error(request, 'Experience data is missing.')
                return render(request, 'reflections/home.html', {'promptsForm': promptsForm, 'reflectionForm': reflectionForm, 'type': 'edit'})

            textAnalysis = index(allText, request.user.norsk)
            print(textAnalysis)
            if request.user.norsk:
                translator = Translator()
                translation_text = translator.translate(allText)
                new_textAnalysis = index(translation_text.text, request.user.norsk)
                textAnalysis['sentiment'] = new_textAnalysis['sentiment']
                print(new_textAnalysis)

            reflectionSave = reflectionForm.save(commit=False)
            # reflectionSave.tags = ",".join(str(x) for x in allInputs.getlist('tags'))
            # reflectionSave.created_by = request.user
            reflectionSave.updated_by = request.user
            reflectionSave.updated_at = datetime.now()
            reflectionSave.save()

            tag_list = allInputs.getlist('tags')[0].split(',')

            reflectionSave.reflection_tags.clear()

            for eachTag in tag_list:
                tag_lower = eachTag.lower()
                tag_exits = Tags.objects.filter(name=tag_lower).exists()
                if tag_exits:
                    new_tag = Tags.objects.filter(name=tag_lower).first()
                    new_tag.reflection.add(reflectionSave)
                    continue
                new_tag = Tags()
                new_tag.name=tag_lower
                new_tag.save()

                new_tag.reflection.add(reflectionSave)

            promptSave = promptsForm.save(commit=False)
            promptSave.updated_by = request.user
            promptSave.reflection = reflectionSave

            if request.POST['has_experience'] == "0":
                promptSave.experience = ""
                promptSave.experience_helpful = ""

            promptSave.readability = json.dumps(textAnalysis['readability'])
            promptSave.wordFrequency = json.dumps(textAnalysis['wordFrequency'])
            promptSave.sentiment = textAnalysis['sentiment']['compound']
            promptSave.save()

            messages.success(request, 'Your data was updated successfully!')
            return HttpResponseRedirect(reverse('reflections:view', args=[reflectionSave.id, group_id]))
    else:
        tags = ",".join([x.name for x in reflection.reflection_tags.all()])
        promptsForm = PromptsForm(instance=prompt)
        reflectionForm = ReflectionForm(instance=reflection)
        promptsForm.initial['has_experience'] = int(prompt.has_experience)
        reflectionForm.initial['tags'] = tags
    return render(request, 'reflections/add-reflection.html', {'group': group, 'promptsForm': promptsForm, 'reflectionForm': reflectionForm, 'type': 'edit'})


@login_required
def deleteFeedback(request, reflection_id, feedback_id):
    reflection = get_object_or_404(Reflection, id=reflection_id)
    feedback = get_object_or_404(Discussion, id=feedback_id)

    if reflection_id != feedback.reflection_id:
        messages.error(request, 'Invalid Request.')
        return HttpResponseRedirect(reverse('myreflections'))

    if feedback.created_by_id != request.user.id:
        messages.error(request, 'Unauthorized access.')
        return HttpResponseRedirect(reverse('myreflections'))

    feedback.delete()
    
    messages.success(request, 'Feedback deleted successfully!')
    return HttpResponseRedirect(reverse('reflections:view', args=[reflection_id, reflection.group_id]))

@login_required
def downloadReflection(request, reflection_id):
    reflection = get_object_or_404(Reflection, id=reflection_id)
    prompt = reflection.reflection_prompts.all()[0]


    content = ['\nSituation:\n'+prompt.situation, '\nExperience:\n'+prompt.experience if prompt.has_experience else '', '\nReflection and Analysis:\n', prompt.experience_helpful if prompt.has_experience else '', prompt.actions, prompt.factors, prompt.emotions, '\nLearnings and Conclusion:\n'+prompt.solutions, prompt.learnings]

    response_content = "\n".join(content)

    response = HttpResponse(response_content, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename={0}'.format('myreflection.doc')
    return response