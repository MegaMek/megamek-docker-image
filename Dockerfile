FROM openjdk:8-jdk

# prepare home, user for jenkins
ENV MEGAMEK_HOME /megamek

ARG user=megamek
ARG group=megamek
ARG uid=1000
ARG gid=1000

RUN groupadd -g ${gid} ${group} \
    && useradd -d "$MEGAMEK_HOME" -u ${uid} -g ${gid} -m -s /bin/bash ${user}

ADD ./megamek-0.46.1.tar.gz  /megamek

WORKDIR /megamek

# expose ssh port
EXPOSE 2346

# make sure host keys are regenerated before sshd starts
COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
