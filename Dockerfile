FROM alpine AS builder

ARG MM_VERSION
ENV MM_VERSION=${MM_VERSION}
ARG SENTRY_ENABLED
ENV SENTRY_ENABLED=${SENTRY_ENABLED}

WORKDIR /app

ADD  "https://github.com/MegaMek/megamek/releases/download/v${MM_VERSION}/megamek-${MM_VERSION}.tar.gz" /tmp/megamek.tar.gz
RUN tar -zxf /tmp/megamek.tar.gz -C /app/megamek
RUN mv megamek/docs/mm-revision.txt /app/mm-revision.txt
RUN rm -rf megamek/data/fonts
RUN rm -rf megamek/data/forcegenerator
RUN rm -rf megamek/data/images
RUN rm -rf megamek/data/names
RUN rm -rf megamek/data/rat
RUN rm -rf megamek/data/scenarios
RUN rm -rf megamek/data/sounds
RUN rm -rf megamek/docs
RUN mkdir megamek/docs
RUN mv /app/mm-revision.txt megamek/docs/mm-revision.txt
RUN rm -rf megamek/*.exe
RUN rm -rf megamek/*.sh
RUN rm megamek/sentry.properties
RUN echo "enabled=${SENTRY_ENABLED}" > megamek/sentry.properties

FROM eclipse-temurin:21-noble

WORKDIR /app
EXPOSE 2346

RUN export DEBIAN_FRONTEND=noninteractive DEBCONF_NONINTERACTIVE_SEEN=true \
  && apt-get -q update \
  && apt-get -q full-upgrade -y \
  && apt-get clean && \
  useradd --user-group --create-home --system --skel /dev/null --home-dir /app megamek

USER megamek

COPY --from=builder --chown=megamek:megamek /app/megamek/ /app/

ENTRYPOINT ["java", "-jar", "MegaMek.jar"]
CMD ["-dedicated", "-port", "2346"]
