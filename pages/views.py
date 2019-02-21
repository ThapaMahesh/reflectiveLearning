from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.template import loader
from thesis_prj import settings
from django.db.models import Q
from django.contrib import messages

from reflections.models import Reflection

def home(request):
	template = loader.get_template('pages/home.html')
	context = {
    }
	return HttpResponse(template.render(context, request))

def index(request):
	template = loader.get_template('pages/dashboard.html')
	context = {
    }
	return HttpResponse(template.render(context, request))

def error_404(request):
	data = {}
	return render(request,'404.html', data)

@login_required
def reflections(request):
	all_reflections = Reflection.objects.filter(created_by_id=request.user.id)
	provided_feedback = Reflection.objects.filter(reflection_discussions__created_by_id=request.user.id).filter(~Q(created_by_id=request.user.id))
	provide_feedback = Reflection.objects.filter(~Q(reflection_discussions__created_by_id=request.user.id)).filter(~Q(created_by_id=request.user.id))
	template = loader.get_template('pages/reflections.html')
	context = {
		'reflections': all_reflections,
		'provide_feedback': provide_feedback,
		'provided_feedback': provided_feedback,
	}
	return HttpResponse(template.render(context, request))


def error_404_view(request):
	return render(request,'pages/error_404.html', {})


# class HomePageView(TemplateView):
#     template_name = 'home.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.request.user.is_authenticated:
#         	context['projects'] = self.request.user.project_created.all()
#         return context