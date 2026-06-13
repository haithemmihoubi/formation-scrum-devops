# ATELIER DevOps (Module 2) — image multi-stage : build Maven puis runtime léger.

# ---------- Étape 1 : build ----------
FROM maven:3.9-eclipse-temurin-21 AS build
WORKDIR /app
COPY pom.xml .
RUN mvn -B dependency:go-offline        # cache des dépendances (couche stable)
COPY src ./src
RUN mvn -B clean package -DskipTests

# ---------- Étape 2 : runtime ----------
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
ENV SPRING_PROFILES_ACTIVE=dev
COPY --from=build /app/target/quickbite-api-*.jar app.jar
EXPOSE 8080
# Ne pas tourner en root
RUN addgroup -S app && adduser -S app -G app
USER app
ENTRYPOINT ["java", "-jar", "app.jar"]
