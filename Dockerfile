FROM ubuntu:jammy as builder

ARG MM_VERSION
ENV MM_VERSION=${MM_VERSION}

WORKDIR /app

RUN apt update && \
  apt install curl ca-certificates -y --no-install-recommends && \
  curl -o /tmp/megamek.tar.gz -L "https://github.com/MegaMek/megamek/releases/download/v${MM_VERSION}/megamek-${MM_VERSION}.tar.gz" && \
  tar -zxvf /tmp/megamek.tar.gz && mv megamek-${MM_VERSION} megamek && \
  rm -rf megamek/data/fonts megamek/data/forcegenerator megamek/data/images megamek/data/names megamek/data/rat megamek/data/scenarios megamek/data/sounds megamek/docs megamek/userdata megamek/mm megamek/mm.bat

FROM eclipse-temurin:17-jammy

WORKDIR /app
EXPOSE 2346

RUN export DEBIAN_FRONTEND=noninteractive DEBCONF_NONINTERACTIVE_SEEN=true \
  && apt-get -q update \
  && apt-get -q dist-upgrade -y \
  && rm -r /var/lib/apt/lists/*

RUN useradd --user-group --create-home --system --skel /dev/null --home-dir /app megamek

COPY --from=builder --chown=megamek:megamek /app/megamek/ /app/

ENTRYPOINT ["java", "-jar", "MegaMek.jar"]
CMD ["-dedicated", "-port", "2346"]
