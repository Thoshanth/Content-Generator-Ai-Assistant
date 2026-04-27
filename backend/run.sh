#!/bin/bash
# Run Spring Boot application with required JVM arguments for Firebase

echo "Starting AI Content Generator Backend..."
echo ""

JAVA_OPTS="--add-opens java.base/java.lang=ALL-UNNAMED \
--add-opens java.base/java.time=ALL-UNNAMED \
--add-opens java.base/java.time.chrono=ALL-UNNAMED \
--add-opens java.base/java.util=ALL-UNNAMED \
--add-opens java.base/java.lang.reflect=ALL-UNNAMED \
--add-opens java.base/java.text=ALL-UNNAMED \
--add-opens java.base/java.io=ALL-UNNAMED"

mvn spring-boot:run -Dspring-boot.run.jvmArguments="$JAVA_OPTS"
