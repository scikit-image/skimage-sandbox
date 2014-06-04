# need to easy_install - https://github.com/dotcloud/docker-py for this to work
import docker
import subprocess

sample_code = """import time;

a = 2;
b = 3;

print a+b;
"""

# CONSTANTS
socket='unix://var/run/docker.sock'
version='1.11'
timeout=10
image='fedora'

# DEBUG 
# print "Create Client"
c = docker.Client(base_url=socket, version=version, timeout=timeout)

# removed parameter memswap_limit, present in docker-py REAMDE.
# ERROR - unexpected keyword argument
# TODO - verify
container = c.create_container(image, command='python', hostname=None, user=None,
                   detach=False, stdin_open=True, tty=False, mem_limit=0,
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
start = c.start(container, binds=None, port_bindings=None, lxc_conf=None,
        publish_all_ports=False, links=None, privileged=False,)

# Generate Handle for accessing the child's streams
handle = subprocess.Popen(['docker', 'attach', container_id], stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE,)

# Separate STDOUT and STDERR
out, err = handle.communicate(sample_code);

print out,

# print "Listing Containers"
# containers = c.containers(quiet=False, all=True, trunc=True, latest=False, since=None,
#              before=None, limit=-1)
