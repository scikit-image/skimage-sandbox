# need to easy_install - https://github.com/dotcloud/docker-py for this to work
import docker
import subprocess

import base64

# Code to test MEM usage. Expected usage is ~208 Megabytes
sample_code = """
a = []
for i in range(0, 100000):
      a.append('abcdefgh')

import resource
print resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
"""

# to check standalone usage
empty_code = """import resource
print resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
"""

# skimage code
sample_code_file = """
import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt

from skimage.morphology import convex_hull_image

from matplotlib import _pylab_helpers

image = np.array(
    [[0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 1, 0, 0, 0, 0],
     [0, 0, 0, 1, 0, 1, 0, 0, 0],
     [0, 0, 1, 0, 0, 0, 1, 0, 0],
     [0, 1, 0, 0, 0, 0, 0, 1, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0]], dtype=float)

original_image = np.copy(image)

chull = convex_hull_image(image)
image[chull] += 1
# image is now:
#[[ 0.  0.  0.  0.  0.  0.  0.  0.  0.]
# [ 0.  0.  0.  0.  2.  0.  0.  0.  0.]
# [ 0.  0.  0.  2.  1.  2.  0.  0.  0.]
# [ 0.  0.  2.  1.  1.  1.  2.  0.  0.]
# [ 0.  2.  1.  1.  1.  1.  1.  2.  0.]
# [ 0.  0.  0.  0.  0.  0.  0.  0.  0.]]


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 6))
ax1.set_title('Original picture')
ax1.imshow(original_image, cmap=plt.cm.gray, interpolation='nearest')
ax2.set_title('Transformed picture')
ax2.imshow(image, cmap=plt.cm.gray, interpolation='nearest')

dpi = 80

fig_managers = _pylab_helpers.Gcf.get_all_fig_managers()
for idx, figman in enumerate(fig_managers):
  figman.canvas.figure.savefig('image{0}.png'.format(idx), dpi=80)

plt.show()

import resource
print resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
"""


# CONSTANTS
socket='unix://var/run/docker.sock'
version='1.12'
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

# the code in sample_code returns in kilobytes.
# mem_limit accepts values in bytes, for ex - this container has 5 MB
container = c.create_container(image, command='python', hostname=None, user=None,
                   detach=False, stdin_open=True, tty=False, mem_limit=52428800,
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
out, err = handle.communicate(empty_code);

print out, err

# ## Travel the docker filesystem default directory for files of our interest
# start = c.restart(container)

# # Generate Handle for accessing the child's streams
# handle = subprocess.Popen(['docker', 'attach', container_id], stdin=subprocess.PIPE,
#                         stdout=subprocess.PIPE, stderr=subprocess.PIPE,)

# # Separate STDOUT and STDERR
# out, err = handle.communicate(list_files_code);
