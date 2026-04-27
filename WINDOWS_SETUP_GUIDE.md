# Windows Setup Guide for Firebase Migration

## Issue: Maven Not Found

You're seeing this error because Maven is not installed on your Windows system.

## Solution: Install Maven

### Option 1: Install Maven with Chocolatey (Recommended - Easiest)

1. **Install Chocolatey** (if not already installed):
   - Open PowerShell as Administrator
   - Run:
   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```

2. **Install Maven**:
   ```powershell
   choco install maven -y
   ```

3. **Verify installation**:
   ```powershell
   mvn --version
   ```

4. **Close and reopen PowerShell**, then try again:
   ```powershell
   cd backend
   mvn clean install
   mvn spring-boot:run
   ```

### Option 2: Manual Installation

1. **Download Maven**:
   - Go to https://maven.apache.org/download.cgi
   - Download "Binary zip archive" (e.g., `apache-maven-3.9.6-bin.zip`)

2. **Extract Maven**:
   - Extract to `C:\Program Files\Apache\maven`
   - You should have: `C:\Program Files\Apache\maven\bin\mvn.cmd`

3. **Add to PATH**:
   - Press `Win + X` → System → Advanced system settings
   - Click "Environment Variables"
   - Under "System variables", find "Path"
   - Click "Edit" → "New"
   - Add: `C:\Program Files\Apache\maven\bin`
   - Click "OK" on all dialogs

4. **Verify installation**:
   - Close and reopen PowerShell
   - Run:
   ```powershell
   mvn --version
   ```

5. **Build the project**:
   ```powershell
   cd backend
   mvn clean install
   mvn spring-boot:run
   ```

### Option 3: Use IntelliJ IDEA or Eclipse (If you have an IDE)

If you have IntelliJ IDEA or Eclipse installed:

#### IntelliJ IDEA:
1. Open the `backend` folder as a project
2. IntelliJ will detect it's a Maven project
3. Wait for dependencies to download
4. Right-click `pom.xml` → Maven → Reload Project
5. Run → Edit Configurations → Add New → Spring Boot
6. Main class: `com.contentgen.ContentGeneratorApplication`
7. Click Run

#### Eclipse:
1. File → Import → Maven → Existing Maven Projects
2. Select the `backend` folder
3. Wait for dependencies to download
4. Right-click project → Run As → Spring Boot App

## Quick Commands After Maven Installation

```powershell
# Navigate to backend
cd "C:\Users\mthos\OneDrive\Desktop\Content Generator\backend"

# Clean and build
mvn clean install

# Run the application
mvn spring-boot:run

# Or run both in one command
mvn clean install spring-boot:run
```

## Before Running - Complete These Steps

### 1. Update Remaining Files (Required)

You still need to update these files to change `UUID` to `String`:

**DTOs** (in `backend/src/main/java/com/contentgen/dto/`):
- `UserProfileDTO.java`
- `ChatSessionDTO.java`
- `ChatMessageDTO.java`

**Controllers** (in `backend/src/main/java/com/contentgen/controllers/`):
- `UserController.java`
- `ChatController.java`

**Security** (in `backend/src/main/java/com/contentgen/config/`):
- `CustomUserDetailsService.java`

See `FIREBASE_REMAINING_TASKS.md` for detailed instructions.

### 2. Set Up Firebase (Required)

1. Create Firebase project at https://firebase.google.com
2. Enable Firestore Database
3. Download credentials → save as `backend/firebase-credentials.json`
4. Update `backend/.env` with your Firebase project ID

See `database/FIREBASE_SETUP.md` for detailed instructions.

## Troubleshooting

### "mvn: command not found" after installation
- Close and reopen PowerShell
- Verify PATH: `$env:Path -split ';' | Select-String maven`
- Try: `& "C:\Program Files\Apache\maven\bin\mvn.cmd" --version`

### "JAVA_HOME not set"
1. Install Java 17 or higher:
   ```powershell
   choco install openjdk17 -y
   ```
2. Or download from: https://adoptium.net/
3. Set JAVA_HOME:
   - Environment Variables → System variables → New
   - Variable name: `JAVA_HOME`
   - Variable value: `C:\Program Files\Eclipse Adoptium\jdk-17.0.x`

### "Could not find firebase-credentials.json"
- Make sure the file is in the `backend` folder
- Check the path in `backend/.env`

### Build errors about UUID
- You need to complete the remaining file updates
- See `FIREBASE_REMAINING_TASKS.md`

## Alternative: Use Docker (Advanced)

If you have Docker installed, you can run without installing Maven:

```powershell
# In the backend directory
docker run -it --rm -v ${PWD}:/app -w /app maven:3.9-eclipse-temurin-17 mvn clean install
```

## Next Steps After Maven Installation

1. ✅ Install Maven (this guide)
2. ⚠️ Update remaining files (see `FIREBASE_REMAINING_TASKS.md`)
3. ⚠️ Set up Firebase (see `database/FIREBASE_SETUP.md`)
4. ✅ Build and run: `mvn clean install spring-boot:run`
5. ✅ Test the application

## Quick Reference

| Command | Purpose |
|---------|---------|
| `mvn clean` | Clean build artifacts |
| `mvn install` | Build and install dependencies |
| `mvn spring-boot:run` | Run the application |
| `mvn clean install` | Clean and build |
| `mvn test` | Run tests |
| `mvn --version` | Check Maven version |

## Windows-Specific Commands

```powershell
# Check if Maven is in PATH
where.exe mvn

# Check Java version
java -version

# Check environment variables
$env:JAVA_HOME
$env:Path

# Navigate with spaces in path
cd "C:\Users\mthos\OneDrive\Desktop\Content Generator\backend"

# Run Maven (if not in PATH)
& "C:\Program Files\Apache\maven\bin\mvn.cmd" clean install
```

---

**Recommended**: Install Maven with Chocolatey (Option 1) - it's the fastest and easiest method!

**Need help?** Check the troubleshooting section above or the main documentation files.
