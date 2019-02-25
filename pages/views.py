from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.template import loader
from thesis_prj import settings
from django.db.models import Q
from django.contrib import messages
from django.core.mail import send_mail
from .forms import ContactForm


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


def send_email(request):
	if request.POST:
		form = ContactForm(request.POST)
		if form.is_valid():
			subject = form.cleaned_data['subject']
			from_email = form.cleaned_data['name'] + '<'+form.cleaned_data['email']+'>'
			message = form.cleaned_data['message']
			try:
				print(subject)
				send_mail( subject, message, from_email, ['bdrmaheshthapa@gmail.com'], fail_silently=False )
				messages.success(request, 'Email sent to developer successfully!')
			except Exception as e:
				print(str(e))
				messages.error(request, 'Invalid mail request. Please try again with correct details')
			return HttpResponseRedirect(reverse('email'))
		else:
			messages.error(request, 'Email details incomplete')
			return HttpResponseRedirect(reverse('email'))
	else:
		form = ContactForm()
		return render(request, "pages/email.html", {'form': form})