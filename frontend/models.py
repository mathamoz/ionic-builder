from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=200)
    # I'm not actually sure what the max length of either of these fields is...
    github_username = models.CharField(max_length=200)
    github_reponame = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now=True)

class Build(models.Model):
    project = models.ForeignKey(Project)
    container_id = models.CharField(null=True, max_length=64)
    created = models.DateTimeField(auto_now=True)
    started = models.DateTimeField(null=True)
    ended = models.DateTimeField(null=True)

class BuildStatus(models.Model):
    build = models.ForeignKey(Build)
    status_name = models.CharField(max_length=32)
    status_message = models.TextField(null=True)
    logged = models.DateTimeField(auto_now=True)
