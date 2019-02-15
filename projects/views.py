from django.shortcuts import render
from .forms import ProjectForm

# Create your views here.
def addProject(request):
    # if request.method == 'POST':
    #     allInputs = request.POST.copy()
    #     projectForm = ProjectForm(allInputs)
    #     if projectForm.is_valid():
    #         projectSave = projectForm.save(commit=False)
    #         projectSave.created_by = request.user
    #         reflectionSave.save()

    #         promptSave = promptsForm.save(commit=False)
    #         promptSave.updated_by = request.user
    #         promptSave.reflection = reflectionSave
    #         promptSave.readability = json.dumps(textAnalysis['readability'])
    #         promptSave.wordFrequency = json.dumps(textAnalysis['wordFrequency'])
    #         promptSave.sentiment = textAnalysis['sentiment']['compound']
    #         promptSave.save()

    #         messages.success(request, 'Your data was saved successfully!')
    #         return HttpResponseRedirect(reverse('reflections:view', args=[reflectionSave.id]))
    # else:
    #     promptsForm = PromptsForm()
    #     reflectionForm = ReflectionForm()
    #     promptsForm.initial['current'] = 1
    #     reflectionForm.initial['is_group'] = 0
    return render(request, 'projects/add-project.html', {})