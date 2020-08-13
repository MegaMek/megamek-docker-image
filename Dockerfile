FROM openjdk:11-jdk

WORKDIR /app

COPY app/ /app

EXPOSE 2346

ENTRYPOINT ["java", "-jar", "MegaMek.jar"]
CMD ["-dedicated", "-port", "2346"]