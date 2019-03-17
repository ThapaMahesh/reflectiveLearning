from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.template import loader
from thesis_prj import settings
from django.contrib import messages
from datetime import datetime
from django.db.models import Q
from django.urls import reverse
from django.core.mail import send_mail
import json

from reflections.models import Reflection
from projects.models import Project, Member
from .forms import SearchForm, ContactForm

def home(request):
	template = loader.get_template('pages/home.html')
	context = {
    }
	return HttpResponse(template.render(context, request))

@login_required
def index(request):
	active_projects = Project.objects.filter(Q(created_by_id=request.user.id) | Q(project_members__user_id=request.user.id)).filter(Q(end_date__gte=datetime.now())).distinct()
	archive_projects = Project.objects.filter(Q(created_by_id=request.user.id) | Q(project_members__user_id=request.user.id)).filter(Q(end_date__lt=datetime.now())).distinct()
	template = loader.get_template('pages/dashboard.html')
	context = {
		"active_projects": active_projects,
		"archive_projects": archive_projects
    }
	return HttpResponse(template.render(context, request))


@login_required
def search(request):
	if request.method == "POST":
		allInputs = request.POST.copy()
		searchForm = SearchForm(allInputs)

		members = request.user.user_members.all()
		group_ids = []
		for eachMember in members:
			member_groups = eachMember.group_set.all()
			for eachGroup in member_groups:
				group_ids.append(eachGroup.id)
			

		search_reflections = Reflection.objects.all()
		tag_list = []

		if request.POST.get('title') and request.POST['title'] != "":
			search_reflections = search_reflections.filter(Q(title__icontains=request.POST['title']))

		if request.POST.get('tags') and request.POST['tags'] != "":
			tag_list = [tag for tag in allInputs.getlist('tags')]
			search_reflections = search_reflections.filter(Q(reflection_tags__in=tag_list))

		if (request.POST.get('start_date') and request.POST.get('end_date')) and (request.POST['start_date'] != "" and request.POST['end_date'] != ""):
			search_reflections = search_reflections.filter(Q(created_at__gte=request.POST['start_date'])).filter(Q(created_at__lte=request.POST['end_date']))
		if 'include_group' not in request.POST:
			search_reflections = search_reflections.filter(Q(is_group=False)).filter(Q(created_by=request.user))
		else:
			search_reflections = search_reflections.filter(Q(created_by=request.user) | (Q(is_group=True) & Q(group_id__in=group_ids) ) )

		selected_tags = [x for x in tag_list]
	else:
		searchForm = SearchForm()
		search_reflections = Reflection.objects.none()
		selected_tags = []
	return render(request, 'pages/search.html', {'searchForm': searchForm, 'search_reflections': search_reflections, 'selected_tags': selected_tags})

def error_404(request):
	data = {}
	return render(request,'404.html', data)

def send_email(request):
	if request.POST:
		form = ContactForm(request.POST)
		if form.is_valid():
			subject = form.cleaned_data['subject']
			from_email = form.cleaned_data['name'] + '<student@rl-feedback.com>'
			message = form.cleaned_data['message']
			try:
				print(subject)
				send_mail( subject, message, from_email, ['bdrmaheshthapa@gmail.com'], fail_silently=False )
				messages.success(request, 'Email sent to developer successfully!')
			except Exception as e:
				print(str(e))
				messages.error(request, 'Invalid mail request. Please try again with correct details')
			return HttpResponseRedirect(reverse('pages:email'))
		else:
			messages.error(request, 'Email details incomplete')
			return HttpResponseRedirect(reverse('pages:email'))
	else:
		form = ContactForm()
		return render(request, "pages/email.html", {'form': form})