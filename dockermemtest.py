# need to easy_install - https://github.com/dotcloud/docker-py for this to work
import docker
import subprocess

import base64

# Code to test MEM usage. Expected usage is ~208 Megabytes
sample_code = """testlist = []
for i in range(0,5000000):
  testlist.append('thisisarandomstring')

import resource
print resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
"""

# CONSTANTS
socket='unix://var/run/docker.sock'
version='1.11'
timeout=10
# image='fedora'
image='docker-skimage'

# DEBUG 
# print "Create Client"
import pdb
c = docker.Client(base_url=socket, version=version, timeout=timeout)

# removed parameter memswap_limit, present in docker-py REAMDE.
# ERROR - unexpected keyword argument
# TODO - verify

# setting the mem_limit does not show up expected results on `docker inspect`
# and it runs the entire code, whereas, 
# `docker run -i -m=mem_limit docker-skimage python` works.
# will have to confirm with Joffrey if it even works.
container = c.create_container(image, command='python', hostname=None, user=None,
                   detach=False, stdin_open=True, tty=False, mem_limit='1000k',
                   ports=None, environment=None, dns=None, volumes=None,
                   volumes_from=None, network_disabled=False, name=None,
                   entrypoint=None, cpu_shares=None, working_dir=None,)

container_id = container.get('Id');

if container_id is None:
	print "Failed to create container!" 
	exit(0);

# removed dns=None, dns_search=None, volumes_from=None, network_mode=None 
# originally present in docker-py README. 
# ERROR - unexpected keyword argument
# TODO - verify
# pdb.set_trace()
start = c.start(container, binds=None, port_bindings=None, lxc_conf=None,
        publish_all_ports=False, links=None, privileged=False,)

# Generate Handle for accessing the child's streams
handle = subprocess.Popen(['docker', 'attach', container_id], stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE,)

# Separate STDOUT and STDERR
out, err = handle.communicate(sample_code);

print out, err

# ## Travel the docker filesystem default directory for files of our interest
# start = c.restart(container)

# # Generate Handle for accessing the child's streams
# handle = subprocess.Popen(['docker', 'attach', container_id], stdin=subprocess.PIPE,
#                         stdout=subprocess.PIPE, stderr=subprocess.PIPE,)

# # Separate STDOUT and STDERR
# out, err = handle.communicate(list_files_code);
