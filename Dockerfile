FROM alpine:latest AS builder

ARG MM_VERSION
ENV MM_VERSION=${MM_VERSION}
ARG SENTRY_ENABLED
ENV SENTRY_ENABLED=${SENTRY_ENABLED}

WORKDIR /app

ADD "https://github.com/MegaMek/megamek/releases/download/v${MM_VERSION}/megamek-${MM_VERSION}.tar.gz" /tmp/megamek.tar.gz
RUN tar -zxvf /tmp/megamek.tar.gz && mv MegaMek-${MM_VERSION} megamek && \
  mv megamek/docs/mm-revision.txt /app/mm-revision.txt && \
  rm -rf megamek/data/fonts && \
  rm -rf megamek/data/forcegenerator && \
  rm -rf megamek/data/images && \
  rm -rf megamek/data/names && \
  rm -rf megamek/data/rat && \
  rm -rf megamek/data/scenarios && \
  rm -rf megamek/data/sounds && \
  rm -rf megamek/docs && \
  mkdir megamek/docs && \
  mv /app/mm-revision.txt megamek/docs/mm-revision.txt && \
  rm -rf megamek/*.exe && \
  rm -rf megamek/*.sh && \
  rm megamek/sentry.properties && \
  echo "enabled=${SENTRY_ENABLED}" > megamek/sentry.properties

FROM gcr.io/distroless/java25-debian13:nonroot

WORKDIR /app
EXPOSE 2346

COPY --from=builder --chown=nonroot:0 /app/megamek/ /app/

ENTRYPOINT ["java", "-jar", "MegaMek.jar"]
CMD ["-dedicated", "-port", "2346"]
