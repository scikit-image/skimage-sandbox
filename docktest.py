# need to easy_install - https://github.com/dotcloud/docker-py for this to work
import docker

sample_code = """import time;

a = 2;
b = 3;

print a+b;
"""

# CONSTANTS
socket='unix://var/run/docker.sock'
version='1.9'
timeout=10
image='fedora'

# DEBUG 
# print "Create Client"
c = docker.Client(base_url=socket, version=version, timeout=timeout)

# print "Listing Containers"
# containers = c.containers(quiet=False, all=True, trunc=True, latest=False, since=None,
#              before=None, limit=-1)

