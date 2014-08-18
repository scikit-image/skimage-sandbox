## About
In short, this setup listens for code execution requests, processes and returns the output. To do this it spins up Docker containers in the back-end, all execution takes place within it and the output is returned in a legible format to the front-end which requested it in the first place.

It was born as a result of a project to setup an interactive gallery for examples @ [scikit-image](http://scikit-image.org/), the Image Processing library for Python.

This is live here @ [interactive gallery for scikit-image examples](http://sharky93.github.io/docs/gallery/auto_examples/)

## Setting it up

Get the latest copy on your server
`git clone https://github.com/scikit-image/skimage-docker/`

### Prerequisites
* [Docker](http://docs.docker.com/installation/)
* [Flask](http://flask.pocoo.org/docs/installation/) - the webserver using which we expose the service
* [docker-py](https://github.com/dotcloud/docker-py) - Python library for interacting with the Docker daemon

Docker works on the concept of [images](https://docs.docker.com/terms/image/#base-image-def) and [containers](http://docs.docker.com/terms/container/) and a [Dockerfile](http://docs.docker.com/reference/builder/) is what is usually used to build the image

The [Dockerfile](http://docs.docker.com/reference/builder/) provided with the repository helps one build an [image](https://docs.docker.com/terms/image/#base-image-def) which caters to running code which uses the scikit-image library. Basically installs all the dependencies on top of the base image. This started as an attempt to setup an interactive gallery for examples @ [scikit-image](http://scikit-image.org/), remember?

Building the image - `docker build -t docker-skimage:1.0 .`

This has to be run when present in the root directory of the repository, since the [Dockerfile](http://docs.docker.com/reference/builder/) is present there and that is what this command uses

After a successful build, - `docker images` should list 'docker-skimage'

Start the server - `python start.py`

This also prints the current URL at which it is running. All left to do now is set up the front-end which interacts with this setup.

## Sample Demo

Here is a very minimalist demo. 

I'll try to explain some of the interactions taking place here. Obviously a lot more can be achieved as desired. See the [interactive gallery](http://sharky93.github.io/docs/gallery/auto_examples/) ;)

#### Components
There are some major components which interact for the demo to work properly.

**Edit** - Creates an instance of the [Ace](http://ace.c9.io/) editor and loads it with code. There needs to be a source for this code in picking it up directly from the HTML is not possible. It is very often such a case when the code is highlighted, but in our demo it is possible to parse the `<pre>` content, but we instead pick it up by decoding a `base64` encoded string which is embedded in the page, since this is what we used eventually for the main gallery since the method is more robust

Clicking anywhere inside the code snippet region invokes the same function

**Run** - Fetches code from the editor and sends it to the server and registers handlers for a successful as well as an error response. On receiving the response, the appropriate message boxes are displayed. If the response contains images, they are inserted after the editor

Pressing `Shift+Enter` invokes the same function

**Revert** - Replaces the editor with a backup of the code snippet, which is created when the page loads for the first time

Similarly if the code generated something on `STDOUT` or `STDERR`, it is received as part of the response and is inserted appropriately
