# Firestore Field Reference - Quick Guide

## Document ID Format

✅ **Correct**: `cBRkOSJRLiVs4fDunwe2` (Click "Auto-ID" button)  
❌ **Wrong**: `123e4567-e89b-12d3-a456-426614174000` (UUID with dashes)

## Field Type Mapping

| Java Type | Firestore Type | Example | How to Set |
|-----------|----------------|---------|------------|
| String | string | "demo@example.com" | Type text directly |
| Integer | number | 42 | Type number directly |
| Long | number | 1000000 | Type number directly |
| Boolean | boolean | true | Select true/false |
| LocalDateTime | timestamp | Dec 15, 2024 10:30 AM | Click "Set to current time" |
| null | null | null | Select "null" from dropdown |

## Users Collection Template

```
Collection: users
Document ID: [Auto-ID] → cBRkOSJRLiVs4fDunwe2

┌─────────────────────┬───────────┬──────────────────────────────────┐
│ Field               │ Type      │ Example Value                    │
├─────────────────────┼───────────┼──────────────────────────────────┤
│ email               │ string    │ demo@example.com                 │
│ username            │ string    │ demouser                         │
│ passwordHash        │ string    │ $2a$10$N9qo8uLOickgx2ZMRZo...    │
│ fullName            │ string    │ Demo User                        │
│ avatarUrl           │ string    │ (empty or URL)                   │
│ plan                │ string    │ free                             │
│ dailyMessageCount   │ number    │ 0                                │
│ lastMessageDate     │ timestamp │ (null or current time)           │
│ createdAt           │ timestamp │ [Set to current time]            │
│ updatedAt           │ timestamp │ [Set to current time]            │
└─────────────────────┴───────────┴──────────────────────────────────┘
```

**Test Password**: "password123"  
**BCrypt Hash**: `$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy`

## Chat Sessions Collection Template

```
Collection: chat_sessions
Document ID: [Auto-ID] → xYz9AbC123dEf456

┌─────────────────────┬───────────┬──────────────────────────────────┐
│ Field               │ Type      │ Example Value                    │
├─────────────────────┼───────────┼──────────────────────────────────┤
│ userId              │ string    │ cBRkOSJRLiVs4fDunwe2            │
│ title               │ string    │ My First Chat                    │
│ contentType         │ string    │ general                          │
│ createdAt           │ timestamp │ [Set to current time]            │
│ updatedAt           │ timestamp │ [Set to current time]            │
└─────────────────────┴───────────┴──────────────────────────────────┘
```

**userId**: Copy from the user document ID you created

## Chat Messages Collection Template

```
Collection: chat_messages
Document ID: [Auto-ID] → pQr7StU890vWx123

┌─────────────────────┬───────────┬──────────────────────────────────┐
│ Field               │ Type      │ Example Value                    │
├─────────────────────┼───────────┼──────────────────────────────────┤
│ sessionId           │ string    │ xYz9AbC123dEf456                │
│ userId              │ string    │ cBRkOSJRLiVs4fDunwe2            │
│ role                │ string    │ user (or assistant)              │
│ content             │ string    │ Hello! Can you help me?          │
│ modelUsed           │ string    │ nvidia/llama-3.1-nemotron-70b... │
│ tokensUsed          │ number    │ 45 (or null)                     │
│ createdAt           │ timestamp │ [Set to current time]            │
└─────────────────────┴───────────┴──────────────────────────────────┘
```

**sessionId**: Copy from the chat session document ID  
**userId**: Copy from the user document ID  
**role**: Must be exactly "user" or "assistant"

## Content Type Options

For `chat_sessions.contentType` field:

- `general` - General conversation
- `blog` - Blog post generation
- `social` - Social media content
- `email` - Email writing
- `code` - Code generation
- `creative` - Creative writing

## Role Options

For `chat_messages.role` field:

- `user` - Message from the user
- `assistant` - Response from AI

## Common Mistakes to Avoid

❌ **Don't use UUID format with dashes**
```
Wrong: 123e4567-e89b-12d3-a456-426614174000
Right: cBRkOSJRLiVs4fDunwe2
```

❌ **Don't type timestamps as strings**
```
Wrong: "2024-12-15 10:30:00"
Right: Click "Set to current time" button
```

❌ **Don't use wrong field types**
```
Wrong: dailyMessageCount as string "0"
Right: dailyMessageCount as number 0
```

❌ **Don't forget to copy IDs correctly**
```
Wrong: Typing IDs manually
Right: Copy-paste from Document ID field
```

## Step-by-Step: Creating Your First User

1. **Go to Firestore Database** in Firebase Console
2. **Click "Start collection"**
3. **Collection ID**: Type `users`
4. **Click "Next"**
5. **Document ID**: Click "Auto-ID" button
6. **Add fields** one by one:
   - Click "Add field"
   - Enter field name (e.g., "email")
   - Select type from dropdown (e.g., "string")
   - Enter value (e.g., "demo@example.com")
   - Repeat for all fields
7. **Click "Save"**
8. **Copy the Document ID** (you'll need it for sessions and messages)

## Step-by-Step: Creating a Chat Session

1. **Click "Start collection"** (or add to existing `chat_sessions`)
2. **Collection ID**: Type `chat_sessions`
3. **Click "Next"**
4. **Document ID**: Click "Auto-ID"
5. **Add field**: `userId`
   - Type: string
   - Value: Paste the user document ID from step 8 above
6. **Add field**: `title`
   - Type: string
   - Value: "My First Chat"
7. **Add field**: `contentType`
   - Type: string
   - Value: "general"
8. **Add field**: `createdAt`
   - Type: timestamp
   - Click "Set to current time"
9. **Add field**: `updatedAt`
   - Type: timestamp
   - Click "Set to current time"
10. **Click "Save"**
11. **Copy the Document ID** (you'll need it for messages)

## Step-by-Step: Creating a Message

1. **Click "Start collection"** (or add to existing `chat_messages`)
2. **Collection ID**: Type `chat_messages`
3. **Click "Next"**
4. **Document ID**: Click "Auto-ID"
5. **Add field**: `sessionId`
   - Type: string
   - Value: Paste the session document ID
6. **Add field**: `userId`
   - Type: string
   - Value: Paste the user document ID
7. **Add field**: `role`
   - Type: string
   - Value: "user"
8. **Add field**: `content`
   - Type: string
   - Value: "Hello! Can you help me write a blog post?"
9. **Add field**: `createdAt`
   - Type: timestamp
   - Click "Set to current time"
10. **Click "Save"**

## Indexes Required

After creating documents, create these indexes:

### Index 1: chat_sessions
- Collection: `chat_sessions`
- Fields:
  - `userId` - Ascending
  - `updatedAt` - Descending

### Index 2: chat_messages (by session)
- Collection: `chat_messages`
- Fields:
  - `sessionId` - Ascending
  - `createdAt` - Ascending

### Index 3: chat_messages (by user)
- Collection: `chat_messages`
- Fields:
  - `userId` - Ascending
  - `role` - Ascending

## Testing Your Setup

After creating sample data, test with these queries in Firestore Console:

**Find user by email:**
```
Collection: users
Filter: email == "demo@example.com"
```

**Find sessions for user:**
```
Collection: chat_sessions
Filter: userId == "cBRkOSJRLiVs4fDunwe2"
Order by: updatedAt descending
```

**Find messages in session:**
```
Collection: chat_messages
Filter: sessionId == "xYz9AbC123dEf456"
Order by: createdAt ascending
```

## Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Can't find "Auto-ID" button | Look for it next to "Document ID" field at the top |
| Timestamp shows error | Don't type - click "Set to current time" button |
| Can't save document | Check all required fields have values |
| Index error when querying | Create the index (Firebase will show a link) |
| Login fails with test user | Verify passwordHash is exactly the BCrypt hash provided |

---

**Print this page** and keep it handy while setting up Firebase! 📄

**Need more help?** Check `FIREBASE_SETUP.md` for detailed instructions.
