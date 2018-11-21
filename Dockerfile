FROM ubuntu:18.04
MAINTAINER Stephen Ramsey (stephen.ramsey@oregonstate.edu)
COPY setup-kg2.sh /usr/local/bin/
COPY setup-kg2-as-rtx.sh /usr/local/bin/
RUN /usr/local/bin/setup-kg2.sh
