from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from urlparse import urlparse
from datetime import datetime
from frontend.models import Project, Build, BuildStatus
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

def index(request):
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
            project.elapsed = (build.ended - build.started).total_seconds()
        elif build and build.started:
            project.elapsed = (datetime.now - build.started).total_seconds()
        else:
            project.elapsed = None

	context = {'projects': projects, 'active_tab': 'projects'}
    return render(request, 'frontend/index.html', context)

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

        return HttpResponseRedirect('/projects')
    else:
        return render(request, 'frontend/new.html', {
            'project_url': '',
            'error_message': "You didn't specify a URL!",
        })

def about(request):
    context = {'active_tab': 'about'}
    return render(request, 'frontend/about.html', context)

def howitworks(request):
    context = {'active_tab': 'how-it-works'}
    return render(request, 'frontend/how-it-works.html', context)
