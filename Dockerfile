FROM openjdk:11-jdk-slim

WORKDIR /app

COPY app/ /app

EXPOSE 2346

ENTRYPOINT ["java", "-jar", "MegaMek.jar"]
CMD ["-dedicated", "-port", "2346"]