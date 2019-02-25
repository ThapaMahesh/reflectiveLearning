from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from datetime import date, datetime
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Subquery

from .forms import ProjectForm

from .models import Project, Member, Group
from reflections.models import Reflection
from users.models import CustomUser
from django.template.defaulttags import register


@register.filter
def check_for_feedback(reflection, user):
    feedback_by_users = [discussion.created_by_id for discussion in reflection.reflection_discussions.all()]
    if user.id in feedback_by_users:
    	return True
    else:
    	return False

# Create your views here.
@login_required
def addProject(request):
    if request.method == 'POST':
        allInputs = request.POST.copy()
        projectForm = ProjectForm(allInputs)
        if projectForm.is_valid():
            projectSave = projectForm.save(commit=False)
            projectSave.created_by = request.user
            projectSave.save()

            member = Member()
            member.project = projectSave
            member.joined_date = date.today()
            member.role = "admin"
            member.user = request.user
            member.save()

            messages.success(request, 'Your data was saved successfully!')
            return HttpResponseRedirect(reverse('dashboard'))
    else:
        projectForm = ProjectForm()
    return render(request, 'projects/add-project.html', {'type': 'add', 'projectForm': projectForm})

@login_required
def viewProject(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    # get all groups created by the user or is part of the group
    groups = Group.objects.filter(Q(project=project)).filter(Q(project__created_by_id=request.user.id) | Q(members__user_id=request.user.id)).distinct()
    members = project.project_members.all()

    # not member of the project or didn't create the project
    if project.created_by_id != request.user.id and request.user.id not in [member.user_id for member in members]:
    	messages.error(request, 'Unauthorized Request')
    	return HttpResponseRedirect(reverse('dashboard'))

    return render(request, 'projects/view-project.html', {'project': project, 'groups': groups, 'members': members})

@login_required
def deleteProject(request, project_id):
	project = get_object_or_404(Project, id=project_id)

	# if didn't create the project
	if project.created_by_id != request.user.id:
		messages.error(request, 'Unauthorized Request')
		return HttpResponseRedirect(reverse('dashboard'))

	project.delete()
	messages.success(request, 'Your data was removed successfully!')
	return HttpResponseRedirect(reverse('dashboard'))

@login_required
def editProject(request, project_id):
	project = get_object_or_404(Project, id=project_id)

	# if didn't create the project
	if project.created_by_id != request.user.id:
		messages.error(request, 'Unauthorized Request')
		return HttpResponseRedirect(reverse('dashboard'))

	if request.method == 'POST':
		allInputs = request.POST.copy()
		projectForm = ProjectForm(allInputs or None, instance=project)
		if projectForm.is_valid():
		    projectSave = projectForm.save(commit=False)
		    projectSave.created_by = request.user
		    projectSave.save()

		messages.success(request, 'Your data was saved successfully!')
		return HttpResponseRedirect(reverse('dashboard'))
	else:
		projectForm = ProjectForm(instance=project)
	return render(request, 'projects/add-project.html', {'type': 'edit', 'projectForm': projectForm})

@login_required
def addGroup(request, project_id):

	project = get_object_or_404(Project, id=project_id)

	# if didn't create the project
	if project.created_by_id != request.user.id:
		messages.error(request, 'Unauthorized Request')
		return HttpResponseRedirect(reverse('dashboard'))
    	
	if request.method == 'POST':
		try:
			allInputs = request.POST.copy()
			print('here1')
			group = Group.objects.filter(name=allInputs.get('name')).filter(project=project)
			print('here2')
			print(group)
			if group:
				messages.error(request, 'Group with same name already exists!')
			else:
				group = Group()
				group.name = allInputs.get('name')
				group.project = project
				group.created_at = datetime.now()
				group.save()


				member_exists = Member.objects.filter(user_id__in=allInputs.getlist('members[]')).filter(project=project).exists()
				if member_exists:
					for eachUserId in allInputs.getlist('members[]'):
						eachUser = CustomUser.objects.get(id=eachUserId)
						
						group.members.add(Member.objects.get(user=eachUser, project=project))

					messages.success(request, 'Group created successfully!')
				else:
					messages.error(request, 'Members do not exist in project to be assigned to  group')
					
				
				return HttpResponseRedirect(reverse('projects:view', args=[project.id]))
		except Exception as e:
			print(str(e))
			messages.error(request, 'Error while processing!')
			return HttpResponseRedirect(reverse('projects:view', args=[project.id]))
	else:
		messages.error(request, 'Invalid request!')
		return HttpResponseRedirect(reverse('dashboard'))


@login_required
def viewGroup(request, project_id, group_id):
	project = get_object_or_404(Project, id=project_id)
	group = get_object_or_404(Group, id=group_id)
	if group.project != project:
		messages.error(request, 'Invalid group request!')
		return HttpResponseRedirect(reverse('projects:view', args=[project_id]))
	members = group.members.all()

	# not member of the group or didn't create the group(project)
	if project.created_by_id != request.user.id and request.user.id not in [member.user_id for member in members]:
		messages.error(request, 'Unauthorized Request')
		return HttpResponseRedirect(reverse('dashboard'))

	group_reflections = Reflection.objects.filter(group=group).filter(is_group=True)
	your_reflections = Reflection.objects.filter(group=group).filter(is_group=False).filter(created_by=request.user)
	provide_feedback = Reflection.objects.filter(group=group).filter(~Q(created_by_id=request.user.id))

	return render(request, 'projects/view-group.html', {'provide_feedback': provide_feedback, 'members': members, 'group': group, 'group_reflections': group_reflections, 'your_reflections': your_reflections})

@login_required
def deleteGroup(request, project_id, group_id):
	project = get_object_or_404(Project, id=project_id)
	group = get_object_or_404(Group, id=group_id)

	if project.created_by_id != request.user.id:
		messages.error(request, 'Unauthorized Request')
		return HttpResponseRedirect(reverse('dashboard'))

	if project != group.project:
		messages.error(request, 'Invalid group request!')
	else:
		group.delete()
		messages.success(request, 'Your data was removed successfully!')
	return HttpResponseRedirect(reverse('projects:view', args=[project.id]))


@login_required
def addMember(request, project_id):
	if request.method == 'POST':
		try:
			project = get_object_or_404(Project, id=project_id)

			if project.created_by_id != request.user.id:
				messages.error(request, 'Unauthorized Request')
				return HttpResponseRedirect(reverse('dashboard'))

			allInputs = request.POST.copy()
			users = CustomUser.objects.filter(id__in=allInputs.getlist('members[]'))
			if users:
				for eachUser in users:
					member = Member.objects.get_or_create(
						user = eachUser,
						project = project,
						defaults= {
						'joined_date': date.today(),
						'role': 'member'
						}
						)

				messages.success(request, 'Member added to project successfully!')
			else:
				messages.error(request, 'Members not found or error while adding!')
			return HttpResponseRedirect(reverse('projects:view', args=[project.id]))
		except Exception as e:
			messages.error(request, 'Error while processing!')
			return HttpResponseRedirect(reverse('projects:view', args=[project.id]))
	else:
		messages.error(request, 'Invalid request!')
		return HttpResponseRedirect(reverse('dashboard'))


@login_required
def removeProjectMember(request, project_id, member_id):
	project = get_object_or_404(Project, id=project_id)
	member = get_object_or_404(Member, id=member_id)

	if project.created_by_id != request.user.id:
		messages.error(request, 'Unauthorized Request')
		return HttpResponseRedirect(reverse('dashboard'))

	if member.project != project:
		messages.error(request, 'Invalid Request')
		return HttpResponseRedirect(reverse('dashboard'))

	member.delete()
	messages.success(request, 'Member removed successfully!')
	return HttpResponseRedirect(reverse('projects:view', args=[project.id]))

@login_required
def addGroupMember(request, project_id, group_id):
	if request.method == 'POST':
		try:
			project = get_object_or_404(Project, id=project_id)
			group = get_object_or_404(Group, id=group_id)

			if group.project_id != project.id:
				messages.error(request, 'Invalid Request')
				return HttpResponseRedirect(reverse('dashboard'))

			if group.project.created_by != request.user:
				messages.error(request, 'Unauthorized Request')
				return HttpResponseRedirect(reverse('dashboard'))

			allInputs = request.POST.copy()
			member_exists = Member.objects.filter(user_id__in=allInputs.getlist('members[]')).filter(project=group.project)
			if len(allInputs.getlist('members[]')) != len(member_exists):
				messages.error(request, 'One or more members do not exist in the project of this group')
			else:
				for eachUserId in allInputs.getlist('members[]'):
					eachUser = CustomUser.objects.get(id=eachUserId)
					
					group.members.add(Member.objects.get(user=eachUser, project=project))

				messages.success(request, 'Member added to group successfully!')
				
			
			return HttpResponseRedirect(reverse('projects:view-group', args=[group.project_id, group.id]))
		except Exception as e:
			messages.error(request, 'Error while processing!')
			return HttpResponseRedirect(reverse('projects:view-group', args=[group.project_id, group.id]))
	else:
		messages.error(request, 'Invalid request!')
		return HttpResponseRedirect(reverse('dashboard'))


@login_required
def removeGroupMember(request, project_id, group_id, member_id):
	project = get_object_or_404(Project, id=project_id)
	group = get_object_or_404(Group, id=group_id)
	member = get_object_or_404(Member, id=member_id)

	if project.created_by_id != request.user.id:
		messages.error(request, 'Unauthorized Request')
		return HttpResponseRedirect(reverse('dashboard'))

	if group.project != project:
		messages.error(request, 'Invalid Request')
		return HttpResponseRedirect(reverse('dashboard'))

	if member not in group.members.all():
		messages.error(request, 'User is not member of the requested group')
		return HttpResponseRedirect(reverse('dashboard'))

	group.members.remove(member)

	messages.success(request, 'Member removed successfully!')
	return HttpResponseRedirect(reverse('projects:view-group', args=[project.id, group.id]))