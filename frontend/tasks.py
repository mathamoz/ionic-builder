from __future__ import absolute_import

from celery import shared_task

@shared_task
def startBuild(build_id, username, reponame):
	import docker

	c = docker.Client(base_url='unix://var/run/docker.sock', version='1.9', timeout=10)

	print "Creating container..."
	container = c.create_container('ionic-build', "/bin/bash -c './build.sh %s %s %s'" % (build_id, username, reponame))

	container_id = container['Id']

	print "Starting container %s..." % container_id
	c.start(container_id)

	print "Building..."
	c.wait(container_id)

	print "Copying build artifact..."
	c.copy(container_id, "/root/%s-%s.tar.gz ." % (username, reponame))

	print "Removing build container..."
	c.remove_container(container_id)
