# dockerfile

FROM fedora

MAINTAINER scikit-image/teamdocker version:1.0

RUN yum -y install numpy scipy python-matplotlib gcc
RUN easy_install -U cython scikit-image
RUN yum clean all

CMD ["/bin/bash", "-D", "FOREGROUND"]
