Stuff you need to have preinstalled -
** Docker - http://docs.docker.com/installation/
** Flask - http://flask.pocoo.org/docs/installation/

An install of Flask in the virtualenv works fine too.

Use the following command to build the Dockerfile -> `docker build -t docker-skimage:1.0 .`
You need to be in the root directory of the repository. This will build a new image from the official base fedora image.
So it may take a while.

After a successful build - `docker images` should list out 'docker-skimage' in the list. 

To start the server, run `python start.py`, it should print the URL of the server
Default is 'http://127.0.0.1:5000/'.
Opening this URL in the browser should open a page which says "The server is up!".
Point to 'http://127.0.0.1:5000/code' to open the interface.

Some basic logging is enabled.

