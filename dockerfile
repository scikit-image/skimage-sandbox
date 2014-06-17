## DO NOT BUILD, INCONSISTENT CURRENTLY

# A basic apache server. To use either add or bind mount content under /var/www
FROM fedora

MAINTAINER scikit-image/teamdocker version:1.0

RUN yum install numpy scipy python-matplotlib gcc
RUN easy_install -U scikit-image

CMD ["/bin/bash", "-D", "FOREGROUND"]