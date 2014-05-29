from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from urlparse import urlparse
from datetime import datetime
import json
from frontend.models import Project, Build, BuildStatus
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

from frontend.tasks import startBuild

def index(request):
	return HttpResponseRedirect('/projects/list')

def listing(request):
    projects = Project.objects.all().order_by('name')

    for project in projects:
        # Somehow I could do this all as one query, investigate later...
        try:
            build = Build.objects.filter(project_id=project.id).order_by('-id')[0]
            buildstatus = BuildStatus.objects.filter(build_id=build.id).order_by('-id')[0]
        except IndexError:
            build = None
            buildstatus = None

        project.started = build.started if build else None
        project.ended = build.ended if build else None
        project.status_name = buildstatus.status_name if buildstatus else None

        if build and build.ended:
            elapsed = (build.ended - build.started).total_seconds()
        elif build and build.started:
            now = timezone.make_aware(datetime.now(),timezone.get_default_timezone())
            elapsed = (now - build.started).total_seconds()
        else:
            elapsed = None

        if elapsed and elapsed > 90:
            elapsed = elapsed / 60
            project.elapsed = "%s minutes" % round(elapsed, 2)
        elif elapsed:
            project.elapsed = "%s seconds" % round(elapsed, 2)

    context = {'projects': projects, 'active_tab': 'projects'}
    return render(request, 'frontend/projects.html', context)

def new(request):
    context = {'active_tab': 'projects'}
    return render(request, 'frontend/new.html', context)

def save(request):
    if request.POST['project_url']:

        url_validator = URLValidator()
        try:
            url_validator(request.POST['project_url'])
        except ValidationError, e:
            return render(request, 'frontend/new.html', {
                'project_url': request.POST['project_url'],
                'error_message': "Enter a valid URL!",
        })

        username,repo = urlparse(request.POST['project_url']).path.split('/')[1:3]
        project_name = ' '.join(word.capitalize() for word in repo.split('-'))

        Project.objects.create(name=project_name, github_username=username, github_reponame=repo)

        return HttpResponseRedirect('/projects/list')
    else:
        return render(request, 'frontend/new.html', {
            'project_url': '',
            'error_message': "You didn't specify a URL!",
        })

def detail(request, project_id):
	try:
		project = Project.objects.filter(id=project_id)[0]
		context = {'project': project, 'active_tab': 'projects'}
		return render(request, 'frontend/detail.html', context)
	except IndexError:
		return HttpResponseRedirect('/projects/list')

def build(request, project_id):
    try:
        project = Project.objects.filter(id=project_id)[0]
        build = Build.objects.create(project_id=project_id)
        build.save()

        startBuild.delay(build.id, project.github_username, project.github_reponame)
        BuildStatus.objects.create(build_id=build.id, status_name="Build Queued")        

        return HttpResponseRedirect('/projects/list')
    except IndexError:
        return HttpResponseRedirect('/projects/list')

# I should move these to another project or something...
def about(request):
    context = {'active_tab': 'about'}
    return render(request, 'frontend/about.html', context)

def howitworks(request):
    context = {'active_tab': 'how-it-works'}
    return render(request, 'frontend/how-it-works.html', context)

@csrf_exempt
def builder(request):
    #POST /builder '{"build_id": $1, "status_name": "Building Project", "status_message": "Building the project"}'
    update_body = json.loads(request.body)

    try:
        if update_body['status_name'] == 'Starting':
            build = Build.objects.filter(id=update_body['build_id'])[0]
            build.started = timezone.make_aware(datetime.now(),timezone.get_default_timezone())
            build.save()
        elif update_body['status_name'] == 'Build Complete':
            build = Build.objects.filter(id=update_body['build_id'])[0]
            build.ended = timezone.make_aware(datetime.now(),timezone.get_default_timezone())
            build.save()
    except:
        BuildStatus.objects.create(build_id=update_body['build_id'], status_name=update_body['status_name'], status_message=update_body['status_message'])
        return HttpResponse('500')

    BuildStatus.objects.create(build_id=update_body['build_id'], status_name=update_body['status_name'], status_message=update_body['status_message'])

    return HttpResponse('200')
