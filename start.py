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
image='fedora'

list_files_code = """import os

for file in os.listdir("."):
    if file.endswith(".txt"):
        print file;
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

    ####################################################################################

    # Fetch files generated
    ## Travel the docker filesystem default directory for files of our interest
    start = c.start(container, binds=None, port_bindings=None, lxc_conf=None,
            publish_all_ports=False, links=None, privileged=False,)

    # Generate Handle for accessing the child's streams
    handle = subprocess.Popen(['docker', 'attach', container_id], stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,)

    # Separate STDOUT and STDERR
    out, err = handle.communicate(list_files_code);

    # Get list of files, last value is an empty string
    filelist = out.split('\n')[:-1];

    # dict of UUencoded filecontent to be returned
    fcencode = {}

    # Iterate for all files in the list
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
          fcencode[f] = fcontent.encode("uu")
          break

        finally:
          pass

    return fcencode

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
    result = dock(content)

    return jsonify(result=result);

if __name__ == '__main__':
    app.run()