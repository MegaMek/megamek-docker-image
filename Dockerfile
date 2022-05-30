FROM openjdk:11-jdk-slim as builder

WORKDIR /app

RUN apt update && \
  apt install curl -y --no-install-recommends && \
  MM_VERSION=`curl --silent "https://api.github.com/repos/megamek/megamek/releases/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/' | cut -c2-` && \
  echo $MM_VERSION && \
  echo "https://github.com/MegaMek/megamek/releases/download/v${MM_VERSION}/megamek-${MM_VERSION}.tar.gz" && \
  curl -o /tmp/megamek.tar.gz -L "https://github.com/MegaMek/megamek/releases/download/v${MM_VERSION}/megamek-${MM_VERSION}.tar.gz" && \
  tar -zxvf /tmp/megamek.tar.gz && \
  mv megamek-${MM_VERSION} megamek && \
  rm -rf megamek/data/fonts megamek/data/forcegenerator megamek/data/images megamek/data/names megamek/data/rat megamek/data/scenarios megamek/data/sounds megamek/docs megamek/userdata megamek/mm megamek/mm.bat

FROM openjdk:11-jdk-slim

WORKDIR /app
EXPOSE 2346

COPY --from=builder /app/megamek/ /app/

ENTRYPOINT ["java", "-jar", "MegaMek.jar"]
CMD ["-dedicated", "-port", "2346"]
