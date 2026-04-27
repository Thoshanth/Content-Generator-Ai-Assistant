# Firebase Setup Guide

Complete guide to set up your **FREE** Firebase Firestore database for the AI Content Generator.

## Step 1: Create Firebase Account

1. Go to [https://firebase.google.com](https://firebase.google.com)
2. Click "Get started"
3. Sign in with your Google account (100% FREE, no credit card required)

## Step 2: Create New Firebase Project

1. Click "Add project" or "Create a project"
2. Enter project details:
   - **Project name**: `ai-content-generator` (or your choice)
   - Click "Continue"
3. **Google Analytics**: You can disable it for now (optional)
4. Click "Create project"
5. Wait 30-60 seconds for project creation

## Step 3: Set Up Firestore Database

1. In the Firebase Console, click "Firestore Database" in the left sidebar
2. Click "Create database"
3. Choose **"Start in production mode"** (we'll add security rules later)
4. Select a Firestore location (choose closest to your users):
   - `us-central` (Iowa) - Default
   - `us-east1` (South Carolina)
   - `europe-west` (Belgium)
   - `asia-southeast1` (Singapore)
5. Click "Enable"
6. Wait for database provisioning (30-60 seconds)

## Step 4: Create Firestore Collections

Firebase Firestore is a NoSQL database, so we don't need to run SQL scripts. Collections will be created automatically when you first add data. However, you can create them manually to understand the structure:

**📋 Quick Reference**: See `FIRESTORE_FIELD_REFERENCE.md` for a printable field guide with all document templates and step-by-step instructions.

### Option A: Let the Application Create Collections (Recommended)

Collections will be created automatically when you first register a user and create a chat session. Skip to Step 5.

### Option B: Create Collections Manually (Optional)

If you want to create sample data manually:

#### 1. Create Users Collection

1. In Firebase Console, go to "Firestore Database"
2. Click "Start collection"
3. Collection ID: `users`
4. Click "Next"
5. Document ID: Click "Auto-ID" (e.g., `cBRkOSJRLiVs4fDunwe2`)
6. Add fields:

| Field | Type | Value (Example) |
|-------|------|-----------------|
| email | string | demo@example.com |
| username | string | demouser |
| passwordHash | string | $2a$10$... (BCrypt hash) |
| fullName | string | Demo User |
| avatarUrl | string | (leave empty or add URL) |
| plan | string | free |
| dailyMessageCount | number | 0 |
| lastMessageDate | timestamp | (leave empty) |
| createdAt | timestamp | (click "Set to current time") |
| updatedAt | timestamp | (click "Set to current time") |

7. Click "Save"

**Note**: For passwordHash, use a BCrypt hash. Example hash for "password123":
```
$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy
```

#### 2. Create Chat Sessions Collection

1. Click "Start collection"
2. Collection ID: `chat_sessions`
3. Document ID: Click "Auto-ID"
4. Add fields:

| Field | Type | Value (Example) |
|-------|------|-----------------|
| userId | string | (copy the user document ID from step 1) |
| title | string | My First Chat |
| contentType | string | general |
| createdAt | timestamp | (click "Set to current time") |
| updatedAt | timestamp | (click "Set to current time") |

5. Click "Save"

#### 3. Create Chat Messages Collection

1. Click "Start collection"
2. Collection ID: `chat_messages`
3. Document ID: Click "Auto-ID"
4. Add fields for user message:

| Field | Type | Value (Example) |
|-------|------|-----------------|
| sessionId | string | (copy the session document ID from step 2) |
| userId | string | (copy the user document ID from step 1) |
| role | string | user |
| content | string | Hello! Can you help me write a blog post? |
| modelUsed | string | (leave empty) |
| tokensUsed | number | (leave empty) |
| createdAt | timestamp | (click "Set to current time") |

5. Click "Save"
6. Add another document for assistant message:

| Field | Type | Value (Example) |
|-------|------|-----------------|
| sessionId | string | (same session ID) |
| userId | string | (same user ID) |
| role | string | assistant |
| content | string | Of course! I'd be happy to help you write a blog post. What topic would you like to write about? |
| modelUsed | string | nvidia/llama-3.1-nemotron-70b-instruct:free |
| tokensUsed | number | 45 |
| createdAt | timestamp | (click "Set to current time") |

7. Click "Save"

### Collections Structure Summary:

1. **users** collection
   - Document ID: auto-generated string (e.g., `cBRkOSJRLiVs4fDunwe2`)
   - Fields: email (string), username (string), passwordHash (string), fullName (string), avatarUrl (string), plan (string), dailyMessageCount (number), lastMessageDate (timestamp), createdAt (timestamp), updatedAt (timestamp)

2. **chat_sessions** collection
   - Document ID: auto-generated string
   - Fields: userId (string), title (string), contentType (string), createdAt (timestamp), updatedAt (timestamp)

3. **chat_messages** collection
   - Document ID: auto-generated string
   - Fields: sessionId (string), userId (string), role (string), content (string), modelUsed (string), tokensUsed (number), createdAt (timestamp)

### Important Notes:

- **Document IDs**: Use Auto-ID to generate random strings (not UUIDs with dashes)
- **Timestamps**: Use Firestore's timestamp type, not strings
- **Numbers**: Use number type for integers (dailyMessageCount, tokensUsed)
- **Strings**: All IDs are strings (userId, sessionId, etc.)
- **Password Hash**: Use BCrypt to hash passwords (the application does this automatically)

### Visual Guide for Creating a Document:

When you see the Firebase Console interface:

```
Document ID: [Auto-ID button] or [Custom ID field]
                ↓
Click "Auto-ID" to generate: cBRkOSJRLiVs4fDunwe2

Field Name    |  Type Dropdown  |  Value
─────────────────────────────────────────
email         |  string ▼       |  demo@example.com
username      |  string ▼       |  demouser
passwordHash  |  string ▼       |  $2a$10$N9qo8u...
plan          |  string ▼       |  free
dailyMessage  |  number ▼       |  0
createdAt     |  timestamp ▼    |  [Set to current time]
```

**Type Options in Dropdown:**
- string - For text (email, username, etc.)
- number - For integers (dailyMessageCount, tokensUsed)
- boolean - For true/false values
- timestamp - For dates/times (createdAt, updatedAt)
- map - For nested objects
- array - For lists
- null - For empty values
- geopoint - For location data
- reference - For document references

### Create Indexes (Important for Performance):

1. Go to "Firestore Database" → "Indexes" tab
2. Click "Create Index"

**Index 1: chat_sessions by userId and updatedAt**
- Collection ID: `chat_sessions`
- Fields to index:
  - `userId` - Ascending
  - `updatedAt` - Descending
- Query scope: Collection
- Click "Create"

**Index 2: chat_messages by sessionId and createdAt**
- Collection ID: `chat_messages`
- Fields to index:
  - `sessionId` - Ascending
  - `createdAt` - Ascending
- Query scope: Collection
- Click "Create"

**Index 3: chat_messages by userId**
- Collection ID: `chat_messages`
- Fields to index:
  - `userId` - Ascending
  - `role` - Ascending
- Query scope: Collection
- Click "Create"

## Quick Reference: Firestore Field Types

When creating documents manually in Firebase Console, use these field types:

| Java Type | Firestore Type | Example Value | Notes |
|-----------|----------------|---------------|-------|
| String | string | "demo@example.com" | Text values |
| Integer/Long | number | 42 | All numbers use "number" type |
| Boolean | boolean | true | true or false |
| LocalDateTime | timestamp | (click "Set to current time") | Date/time values |
| List | array | ["item1", "item2"] | Lists of values |
| Map | map | {key: "value"} | Nested objects |
| null | null | null | Empty/missing values |

### Complete Field Mappings for Each Collection:

#### Users Collection Document:
```
Document ID: (Auto-generated, e.g., cBRkOSJRLiVs4fDunwe2)

Fields:
├─ email: string → "demo@example.com"
├─ username: string → "demouser"
├─ passwordHash: string → "$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy"
├─ fullName: string → "Demo User"
├─ avatarUrl: string → "" (can be empty)
├─ plan: string → "free"
├─ dailyMessageCount: number → 0
├─ lastMessageDate: timestamp → (null or current time)
├─ createdAt: timestamp → (Set to current time)
└─ updatedAt: timestamp → (Set to current time)
```

#### Chat Sessions Collection Document:
```
Document ID: (Auto-generated)

Fields:
├─ userId: string → "cBRkOSJRLiVs4fDunwe2" (user's document ID)
├─ title: string → "My First Chat"
├─ contentType: string → "general"
├─ createdAt: timestamp → (Set to current time)
└─ updatedAt: timestamp → (Set to current time)
```

#### Chat Messages Collection Document:
```
Document ID: (Auto-generated)

Fields:
├─ sessionId: string → (session's document ID)
├─ userId: string → (user's document ID)
├─ role: string → "user" or "assistant"
├─ content: string → "Hello! Can you help me?"
├─ modelUsed: string → "nvidia/llama-3.1-nemotron-70b-instruct:free" (or empty)
├─ tokensUsed: number → 45 (or null)
└─ createdAt: timestamp → (Set to current time)
```

### Password Hash for Testing:

If you want to create a test user manually, use this BCrypt hash for password "password123":
```
$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy
```

You can then login with:
- Email: demo@example.com
- Password: password123

## Step 5: Get Firebase Admin SDK Credentials

1. In Firebase Console, click the **gear icon** ⚙️ next to "Project Overview"
2. Click "Project settings"
3. Go to the "Service accounts" tab
4. Click "Generate new private key"
5. Click "Generate key" in the confirmation dialog
6. A JSON file will be downloaded (e.g., `ai-content-generator-firebase-adminsdk-xxxxx.json`)
7. **IMPORTANT**: Keep this file secure! It contains sensitive credentials.

## Step 6: Configure Spring Boot Application

### 6.1 Place Firebase Credentials

1. Rename the downloaded JSON file to `firebase-credentials.json`
2. Place it in the `backend` directory (same level as `pom.xml`)
3. **IMPORTANT**: Add to `.gitignore` to prevent committing credentials:

```bash
# Add to .gitignore
backend/firebase-credentials.json
```

### 6.2 Update application.properties

The `application.properties` file has already been updated. Verify it contains:

```properties
# Firebase Configuration
firebase.credentials.path=${FIREBASE_CREDENTIALS_PATH:./firebase-credentials.json}
firebase.database.url=${FIREBASE_DATABASE_URL:https://your-project-id.firebaseio.com}
```

### 6.3 Set Environment Variables (Recommended)

Create a `.env` file in the `backend` directory:

```bash
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
FIREBASE_DATABASE_URL=https://your-project-id.firebaseio.com
JWT_SECRET=your-256-bit-secret-key-change-this-in-production
AI_SERVICE_URL=http://localhost:8000
```

Replace `your-project-id` with your actual Firebase project ID (found in Project Settings).

## Step 7: Set Up Firestore Security Rules

1. In Firebase Console, go to "Firestore Database"
2. Click the "Rules" tab
3. Replace the default rules with:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users collection
    match /users/{userId} {
      allow read, write: if request.auth != null;
    }
    
    // Chat sessions collection
    match /chat_sessions/{sessionId} {
      allow read, write: if request.auth != null;
    }
    
    // Chat messages collection
    match /chat_messages/{messageId} {
      allow read, write: if request.auth != null;
    }
  }
}
```

4. Click "Publish"

**Note**: Since we're using JWT authentication in Spring Boot (not Firebase Auth), these rules are permissive. For production, you may want to implement custom claims or use Firebase Authentication.

### Common Document Creation Issues:

**Issue**: "Invalid field type"
- **Solution**: Make sure you select the correct type from the dropdown:
  - Text → string
  - Numbers → number  
  - Dates → timestamp
  - True/False → boolean

**Issue**: "Document ID format"
- **Solution**: Click "Auto-ID" button to generate IDs like `cBRkOSJRLiVs4fDunwe2`
- Don't use UUIDs with dashes (e.g., ~~123e4567-e89b-12d3-a456-426614174000~~)

**Issue**: "Timestamp not saving"
- **Solution**: Click the "Set to current time" button in the timestamp field
- Don't type dates manually

**Issue**: "Can't find user/session ID to reference"
- **Solution**: Copy the Document ID from the document list
- Example: When viewing a user document, the ID is shown as `Document ID: cBRkOSJRLiVs4fDunwe2`
- Use this ID when creating related documents (sessions, messages)

**Issue**: "Password hash not working for login"
- **Solution**: Use the BCrypt hash provided in the Quick Reference section for testing
- The application will generate proper hashes during registration

## Step 8: Test Firebase Connection

### Option 1: Run Spring Boot Application

```bash
cd backend
./mvnw clean install
./mvnw spring-boot:run
```

If connection is successful, you'll see:
```
Successfully initialized Firebase App
Firestore client initialized
```

### Option 2: Test with Firebase Console

1. Go to "Firestore Database" in Firebase Console
2. Click "Start collection"
3. Collection ID: `test`
4. Add a document with any field
5. If successful, Firebase is working!
6. Delete the test collection

## Firebase Free Tier Limits (Spark Plan)

✅ **Included in Free Tier:**
- **Firestore Database**:
  - 1 GB storage
  - 50,000 reads/day
  - 20,000 writes/day
  - 20,000 deletes/day
  - 10 GB/month network egress
- **Firebase Hosting**: 10 GB storage, 360 MB/day transfer
- **Cloud Functions**: 125K invocations/month, 40K GB-seconds, 40K CPU-seconds
- **Authentication**: Unlimited users
- **Realtime Database**: 1 GB storage, 10 GB/month transfer

### Monitoring Usage

1. Go to Firebase Console → "Usage and billing"
2. View current usage for all services
3. Set up budget alerts (optional)

## Troubleshooting

### Error: "Could not find credentials file"
- Verify `firebase-credentials.json` is in the `backend` directory
- Check the path in `application.properties`
- Ensure the file is not corrupted

### Error: "Permission denied"
- Check Firestore Security Rules
- Verify the service account has proper permissions
- Go to Google Cloud Console → IAM & Admin → Service Accounts

### Error: "Index required"
- Firebase will show which index is needed in the error message
- Go to Firestore → Indexes
- Click the link in the error message to auto-create the index
- Wait 2-5 minutes for index to build

### Connection Timeout
- Check your internet connection
- Verify Firebase project is active
- Check if firewall is blocking Firebase domains

## Advantages of Firebase over Supabase

✅ **Better Free Tier**: More generous limits for small projects  
✅ **No Database Sleep**: Always available, no cold starts  
✅ **Real-time Updates**: Built-in real-time listeners  
✅ **Automatic Scaling**: Scales automatically with usage  
✅ **Google Infrastructure**: Reliable and fast globally  
✅ **No Connection Pooling Issues**: NoSQL, no connection limits  
✅ **Integrated Services**: Auth, Storage, Functions, Hosting all in one  

## Data Migration from Supabase (Optional)

If you have existing data in Supabase, you can export it and import to Firebase:

### Export from Supabase:
```sql
-- Export users
COPY (SELECT * FROM users) TO '/tmp/users.csv' WITH CSV HEADER;

-- Export chat_sessions
COPY (SELECT * FROM chat_sessions) TO '/tmp/chat_sessions.csv' WITH CSV HEADER;

-- Export chat_messages
COPY (SELECT * FROM chat_messages) TO '/tmp/chat_messages.csv' WITH CSV HEADER;
```

### Import to Firebase:
Use the Firebase Admin SDK or create a migration script (we can provide this if needed).

## Next Steps

After successful setup:

1. ✅ Firebase project created
2. ✅ Firestore database enabled
3. ✅ Credentials downloaded and configured
4. ✅ Spring Boot can connect
5. 🚀 Start building your application!

## Useful Firebase Features

### 1. Firestore Console
- View and edit data in real-time
- Add/remove documents manually
- Test queries

### 2. Firebase Authentication (Optional)
- Add email/password authentication
- Social login (Google, Facebook, etc.)
- Phone authentication

### 3. Firebase Storage (Optional)
- Store user avatars
- Store generated content files
- 5 GB free storage

### 4. Firebase Hosting (Optional)
- Deploy your React frontend
- Free SSL certificate
- Global CDN

### 5. Cloud Functions (Optional)
- Serverless backend functions
- Triggered by Firestore changes
- Scheduled functions

## Support

- **Firebase Docs**: https://firebase.google.com/docs
- **Firestore Docs**: https://firebase.google.com/docs/firestore
- **Community**: https://firebase.google.com/community
- **Stack Overflow**: Tag `firebase` or `google-cloud-firestore`

---

**Your Firebase database is now ready! 🎉**

Proceed to run the Spring Boot backend and Python AI service.
