from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

import docker

import subprocess
import tarfile
import StringIO


# CONSTANTS
socket='unix://var/run/docker.sock'
version='1.11'
timeout=10
image='docker-skimage'

# code to fetch files written as png
list_files_code = """import os

for file in os.listdir("."):
    if file.endswith(".png"):
        print file;
"""

fig_manager = """
dpi = 80

from matplotlib import _pylab_helpers

fig_managers = _pylab_helpers.Gcf.get_all_fig_managers()
for idx, figman in enumerate(fig_managers):
  figman.canvas.figure.savefig('image{0}.png'.format(idx), dpi=80)
"""

matplotlib_backend = """
import matplotlib
matplotlib.use('Agg')
"""


app = Flask(__name__)

def dock(code):
    c = docker.Client(base_url=socket, version=version, timeout=timeout)

    # open STDIN
    container = c.create_container(image, command='python', hostname=None, user=None,
                                detach=False, stdin_open=True, tty=False, mem_limit=0,
                                ports=None, environment=None, dns=None, volumes=None,
                                volumes_from=None, network_disabled=False, name=None,
                                entrypoint=None, cpu_shares=None, working_dir=None,)

    container_id = container.get('Id');

    if container_id is None:
        print "Failed to create container!" 
        return -1

    # DEBUG
    # print container_id

    start = c.start(container, binds=None, port_bindings=None, lxc_conf=None,
        publish_all_ports=False, links=None, privileged=False,)

    # Attach handles for accessing the child's streams
    handle = subprocess.Popen(['docker', 'attach', container_id], stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE,)

    # Separate STDOUT and STDERR
    # Done with code execution
    out, err = handle.communicate(code);
    # DEBUG
    # print "STDOUT after exec ", out
    # print "STDERR after exec ", err

    ####################################################################################

    # Fetch files generated
    ## Travel the docker filesystem default directory for files of our interest
    start = c.restart(container)

    # Generate Handle for accessing the child's streams
    handle = subprocess.Popen(['docker', 'attach', container_id], stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,)

    # Separate STDOUT and STDERR
    out, err = handle.communicate(list_files_code);
    # DEBUG
    # print "STDOUT after exec ", out
    # print "STDERR after exec ", err


    # Get list of files, last value is an empty string
    filelist = out.split('\n')[:-1];

    # dict of UUencoded filecontent to be returned
    # fcencode = {}

    # dict of base64 converted filecontent to be returned
    fcbase64 = {}

    # Iterate for all files in the list
    import base64

    for f in filelist:
      copy = c.copy(container, f)

      ofile = StringIO.StringIO()

      while 1:
        try:
          ofile.write(next(copy))

        except StopIteration:  
          ofile.seek(0)
          tarf = tarfile.TarFile(fileobj=ofile)
          fcontent = tarf.extractfile(f).read()
          # DEBUG to check if output is correct before encoding
          # print fcontent
          # UUDECODE is difficult client side, so we go the base64 route
          # fcencode[f] = fcontent.encode("uu")
          fcbase64[f] = base64.b64encode(fcontent)
          break

        finally:
          pass

    return fcbase64

@app.route('/')
def home():
    return 'The server is up!'

@app.route('/code')
def write_code():
    return render_template('runcode.html')

@app.route('/runcode', methods=['POST'])
def run_code():
    content = request.json['data']
    # DEBUG 
    # print content

    # fire up docker
    # force matplotlib to agg and add the figure manager code
    content = matplotlib_backend + content + fig_manager
    result = dock(content)

    return jsonify(result=result);

if __name__ == '__main__':
    app.run()