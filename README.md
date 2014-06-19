Stuff you need to have preinstalled -
** Docker - http://docs.docker.com/installation/
** Flask env - http://flask.pocoo.org/docs/installation/

An install of Flask in the virtualenv works well.

Use the following command to build the Dockerfile -> `docker build -t docker-skimage:1.0 .`
You need to be in the root directory of the repository. This will build a new image from the official base fedora image.
It takes some time, so patience is key here, there will be logs thrown at you, so you can have a look at that or just go do something else.

After a successful build - `docker images` should list out 'docker-skimage' in the list. If not there is something wrong, please verify if you folllowed the steps correctly, look for any obvious mistakes.

To start the server, run `python start.py`, it should print out the URL of the server, default is 'http://127.0.0.1:5000/'.
Opening this URL in the browser should open a page which says "The server is up!".
Point to 'http://127.0.0.1:5000/code' to open the interface to the code execution service.

Some basic logging is enabled, so Flask will print out stuff on the terminal you used to start the server.

