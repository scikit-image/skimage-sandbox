from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

import docker
import subprocess

# CONSTANTS
socket='unix://var/run/docker.sock'
version='1.11'
timeout=10
image='fedora'


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
    out, err = handle.communicate(code);

    return out

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