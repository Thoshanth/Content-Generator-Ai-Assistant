# Java Module System Fix for Firebase

## Issue

When running with Java 17+, you may see this error:
```
Unable to make private java.time.chrono.IsoChronology() accessible: 
module java.base does not "opens java.time.chrono" to unnamed module
```

This happens because Firebase Admin SDK needs access to Java's internal classes, but Java 17+ has stricter module encapsulation.

## Solution Applied

I've added the necessary JVM arguments to allow Firebase to access required modules.

## How to Run

### Option 1: Use the Run Script (Recommended)

**Windows:**
```powershell
cd backend
.\run.bat
```

**Linux/Mac:**
```bash
cd backend
chmod +x run.sh
./run.sh
```

### Option 2: Maven with JVM Arguments

```bash
cd backend
mvn spring-boot:run -Dspring-boot.run.jvmArguments="--add-opens java.base/java.lang=ALL-UNNAMED --add-opens java.base/java.time=ALL-UNNAMED --add-opens java.base/java.time.chrono=ALL-UNNAMED --add-opens java.base/java.util=ALL-UNNAMED"
```

### Option 3: Run JAR with Arguments

```bash
# Build first
mvn clean package

# Run with arguments
java --add-opens java.base/java.lang=ALL-UNNAMED \
     --add-opens java.base/java.time=ALL-UNNAMED \
     --add-opens java.base/java.time.chrono=ALL-UNNAMED \
     --add-opens java.base/java.util=ALL-UNNAMED \
     -jar target/ai-content-generator-1.0.0.jar
```

### Option 4: IDE Configuration

#### IntelliJ IDEA:
1. Run → Edit Configurations
2. Select your Spring Boot configuration
3. Add to "VM options":
   ```
   --add-opens java.base/java.lang=ALL-UNNAMED
   --add-opens java.base/java.time=ALL-UNNAMED
   --add-opens java.base/java.time.chrono=ALL-UNNAMED
   --add-opens java.base/java.util=ALL-UNNAMED
   ```

#### Eclipse:
1. Run → Run Configurations
2. Select your Spring Boot App
3. Arguments tab → VM arguments:
   ```
   --add-opens java.base/java.lang=ALL-UNNAMED
   --add-opens java.base/java.time=ALL-UNNAMED
   --add-opens java.base/java.time.chrono=ALL-UNNAMED
   --add-opens java.base/java.util=ALL-UNNAMED
   ```

#### VS Code:
Add to `.vscode/launch.json`:
```json
{
  "configurations": [
    {
      "type": "java",
      "name": "Spring Boot",
      "request": "launch",
      "mainClass": "com.contentgen.ContentGeneratorApplication",
      "vmArgs": "--add-opens java.base/java.lang=ALL-UNNAMED --add-opens java.base/java.time=ALL-UNNAMED --add-opens java.base/java.time.chrono=ALL-UNNAMED --add-opens java.base/java.util=ALL-UNNAMED"
    }
  ]
}
```

## What Was Changed

1. **pom.xml** - Added JVM arguments to Spring Boot Maven plugin
2. **backend/.mvn/jvm.config** - Created JVM config file (auto-loaded by Maven)
3. **backend/run.bat** - Windows run script with arguments
4. **backend/run.sh** - Linux/Mac run script with arguments

## Why This Happens

Java 9+ introduced the module system (JPMS) which restricts access to internal JDK classes. Firebase Admin SDK uses reflection to access some of these internal classes for serialization/deserialization of Firestore data.

The `--add-opens` flag tells the JVM to allow reflective access to these packages.

## Alternative: Downgrade to Java 11

If you prefer not to use these flags, you can downgrade to Java 11:

1. Install Java 11
2. Update `JAVA_HOME` environment variable
3. Verify: `java -version` should show Java 11
4. Run normally: `mvn spring-boot:run`

However, **Java 17+ is recommended** for better performance and security.

## Verification

After applying the fix, you should see:
```
Started ContentGeneratorApplication in X.XXX seconds
```

Without errors about module access.

## Troubleshooting

### Still seeing module errors?

Add more opens if needed:
```
--add-opens java.base/java.lang.reflect=ALL-UNNAMED
--add-opens java.base/java.text=ALL-UNNAMED
--add-opens java.base/java.io=ALL-UNNAMED
```

### Maven not picking up jvm.config?

Make sure the file is at: `backend/.mvn/jvm.config`

### IDE not using the arguments?

Manually add VM options in your IDE's run configuration (see Option 4 above).

---

**Quick Start:** Just run `.\run.bat` (Windows) or `./run.sh` (Linux/Mac) from the backend directory!
