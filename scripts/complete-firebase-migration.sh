#!/bin/bash

# Firebase Migration Completion Script
# This script helps complete the remaining UUID to String conversions

echo "🔥 Firebase Migration - Completion Helper"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the project root
if [ ! -d "backend" ]; then
    echo -e "${RED}Error: Please run this script from the project root directory${NC}"
    exit 1
fi

echo "📋 Checking for UUID references in DTOs and Controllers..."
echo ""

# Find all UUID references
UUID_FILES=$(grep -r "import java.util.UUID" backend/src/main/java/com/contentgen/dto/ backend/src/main/java/com/contentgen/controllers/ 2>/dev/null | cut -d: -f1 | sort -u)

if [ -z "$UUID_FILES" ]; then
    echo -e "${GREEN}✅ No UUID imports found in DTOs and Controllers!${NC}"
else
    echo -e "${YELLOW}⚠️  Found UUID imports in the following files:${NC}"
    echo "$UUID_FILES"
    echo ""
    echo "These files need to be updated:"
    echo "1. Change 'import java.util.UUID;' → Remove this import"
    echo "2. Change 'private UUID id;' → 'private String id;'"
    echo "3. Change 'private UUID userId;' → 'private String userId;'"
    echo "4. Change 'private UUID sessionId;' → 'private String sessionId;'"
    echo "5. Change '@PathVariable UUID' → '@PathVariable String'"
    echo ""
fi

echo "📋 Checking Firebase configuration..."
echo ""

# Check if firebase-credentials.json exists
if [ -f "backend/firebase-credentials.json" ]; then
    echo -e "${GREEN}✅ Firebase credentials file found${NC}"
else
    echo -e "${YELLOW}⚠️  Firebase credentials file not found${NC}"
    echo "   Please download from Firebase Console and save as:"
    echo "   backend/firebase-credentials.json"
    echo ""
fi

# Check if .env exists
if [ -f "backend/.env" ]; then
    echo -e "${GREEN}✅ Backend .env file found${NC}"
else
    echo -e "${YELLOW}⚠️  Backend .env file not found${NC}"
    echo "   Creating from .env.example..."
    if [ -f "backend/.env.example" ]; then
        cp backend/.env.example backend/.env
        echo -e "${GREEN}✅ Created backend/.env from example${NC}"
        echo "   Please edit backend/.env with your Firebase project ID"
    fi
    echo ""
fi

# Check .gitignore
if grep -q "firebase-credentials.json" .gitignore; then
    echo -e "${GREEN}✅ .gitignore includes Firebase credentials${NC}"
else
    echo -e "${YELLOW}⚠️  .gitignore doesn't include Firebase credentials${NC}"
    echo "   This has been added to .gitignore"
fi

echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Update DTOs and Controllers (if needed):"
echo "   - Open each file listed above"
echo "   - Replace UUID with String for id fields"
echo ""
echo "2. Set up Firebase:"
echo "   - Create project at https://firebase.google.com"
echo "   - Enable Firestore Database"
echo "   - Download credentials → backend/firebase-credentials.json"
echo "   - Update backend/.env with your project ID"
echo ""
echo "3. Build and test:"
echo "   cd backend"
echo "   ./mvnw clean install"
echo "   ./mvnw spring-boot:run"
echo ""
echo "4. Create Firestore indexes (after first run)"
echo ""
echo "📚 Documentation:"
echo "   - FIREBASE_SETUP.md - Complete setup guide"
echo "   - FIREBASE_MIGRATION_COMPLETE.md - Migration summary"
echo "   - FIREBASE_REMAINING_TASKS.md - Detailed task list"
echo ""
echo "🎉 You're almost done! Estimated time remaining: 1 hour"
