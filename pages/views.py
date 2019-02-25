from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.template import loader
from thesis_prj import settings
from django.contrib import messages
from django.db.models import Q

from reflections.models import Reflection
from projects.models import Project

def home(request):
	template = loader.get_template('pages/home.html')
	context = {
    }
	return HttpResponse(template.render(context, request))

@login_required
def index(request):
	projects = Project.objects.filter(Q(created_by_id=request.user.id) | Q(project_members__user_id=request.user.id)).distinct()
	template = loader.get_template('pages/dashboard.html')
	context = {
		"projects": projects
    }
	return HttpResponse(template.render(context, request))

def error_404(request):
	data = {}
	return render(request,'404.html', data)