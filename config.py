## This is the config file for the Docker execution service
## Parameters defined here help to customize the results returned

## PS - this file is very simple, flexible and powerful. Since it is imported
## directly, please be careful while modifying this

# CONSTANTS
# socket for scikit server, address where the Docker daemon listens
socket='tcp://192.168.59.103:2375'
version='1.11'
# timeout specifies the timeout for the request for connection to communicate
# with the Docker daemon
timeout=10
# containers launched are instances of this image
image='docker-skimage:1.1'

# DEBUG mode
debug = False

# maximum number of lines of output which the service returns
max_output = 100

# max number of simultaneous containers that can exists and run code
max_queue_size = 5

# port at which the service listens
port = 8000

# ip address at which the service exists
hostip = '198.206.133.45'
