# need to easy_install - https://github.com/dotcloud/docker-py for this to work
import docker
import subprocess

import base64

sample_code = """import time;

a = 2;
b = 3;

print a+b;
"""

# escaping the newline
sample_code_file_old = """import time;

import shutil;

a = 'A';
b = 'B';
c = 'C';

d = 2;
e = 3;

n = '\\n';

out = open('output.txt', 'w');

for i in range(1, 8):
	out.write(a+b+c+n);
	a = chr(ord(a) + 3);
	b = chr(ord(b) + 3);
	c = chr(ord(c) + 3); 

out.close();
shutil.copyfile('output.txt', 'anotheroutput.txt');
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
"""

list_files_code = """import os

for file in os.listdir("."):
    if file.endswith(".png"):
        print file;
"""

# CONSTANTS
socket='unix://var/run/docker.sock'
# For the server online
# socket='tcp://192.168.59.103:2375'
version='1.11'
timeout=10
# image='fedora'
image='docker-skimage:1.0'

# DEBUG 
# print "Create Client"
import pdb
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
pdb.set_trace()
start = c.start(container, binds=None, port_bindings=None, lxc_conf=None,
        publish_all_ports=False, links=None, privileged=False,)

# Generate Handle for accessing the child's streams
handle = subprocess.Popen(['docker', 'attach', container_id], stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE,)

# Separate STDOUT and STDERR
out, err = handle.communicate(sample_code);

print out

## Travel the docker filesystem default directory for files of our interest
start = c.restart(container)

# Generate Handle for accessing the child's streams
handle = subprocess.Popen(['docker', 'attach', container_id], stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE,)

# Separate STDOUT and STDERR
out, err = handle.communicate(list_files_code);

# Get list of files, last value is an empty string
filelist = out.split('\n')[:-1];

import tarfile
import StringIO

import pdb

for f in filelist:
  copy = c.copy(container, f)

  # TARFILE tryouts
  filo = StringIO.StringIO()
  while 1:
    try:
      filo.write(next(copy))

    except StopIteration:  
      # DEBUG print "no more to read, reached", copy.tell()
      # DEBUG print "Passing to tarfile"
      filo.seek(0)
      tarf = tarfile.TarFile(fileobj=filo)
      fcontent = tarf.extractfile(f).read()
      fcencode = fcontent.encode("uu")
      fcbase64 = base64.b64encode(fcontent)
      # 15351
      # 14832
      break

    finally:
      pass
  # pdb.set_trace()


print out,

# print "Listing Containers"
# containers = c.containers(quiet=False, all=True, trunc=True, latest=False, since=None,
#              before=None, limit=-1)
