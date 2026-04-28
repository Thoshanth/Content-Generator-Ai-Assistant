# 🚀 Restart and Test PDF Export

## Quick Start

### Step 1: Restart AI Service
```bash
# Stop current service (Ctrl+C if running)

# Start fresh
cd ai-service
python main.py
```

**Look for these messages on startup**:
```
[PDF Export] WeasyPrint not available: No module named 'weasyprint'
[PDF Export] ReportLab available as fallback
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ This confirms PDF export is ready with ReportLab!

---

### Step 2: Test PDF Export

#### Option A: Quick API Test
```bash
# In a new terminal (keep AI service running)
cd ai-service
python test_pdf_api.py
```

**Expected**: Creates `test_resume_output.pdf` successfully

#### Option B: Frontend Test
1. Open browser: `http://localhost:3000`
2. Login to your account
3. Generate a resume: "Create a resume for a software engineer"
4. Click the **PDF** export button
5. PDF should download automatically

#### Option C: cURL Test
```bash
curl -X POST http://localhost:8000/tools/export-pdf \
  -H "Content-Type: application/json" \
  -d '{
    "content": "# Test Resume\n\n## Experience\n\n- Software Engineer at Tech Co\n- Built amazing products",
    "content_type": "resume",
    "candidate_name": "Test_User"
  }' \
  --output test.pdf

# Check if PDF was created
ls -lh test.pdf
```

---

## What to Expect

### ✅ Success Indicators

**AI Service Logs**:
```
[PDF Export] Using ReportLab (WeasyPrint not available)
INFO: 127.0.0.1:XXXXX - "POST /tools/export-pdf HTTP/1.1" 200 OK
```

**Frontend**:
- PDF downloads automatically
- File opens in PDF viewer
- Content is formatted correctly

**File Size**:
- Typical resume: 1500-3000 bytes
- With more content: 3000-10000 bytes

---

### ❌ If You See Errors

**Error: "ReportLab not found"**
```bash
cd ai-service
pip install reportlab
# Then restart service
```

**Error: "500 Internal Server Error"**
- Check AI service terminal for detailed error
- Make sure ReportLab is installed: `pip list | grep reportlab`
- Try the quick API test to isolate the issue

**Error: "Connection refused"**
- Make sure AI service is running on port 8000
- Check: `curl http://localhost:8000/health`

---

## Complete Test Checklist

- [ ] AI service starts without errors
- [ ] Startup logs show ReportLab available
- [ ] Quick API test creates PDF file
- [ ] PDF file opens correctly
- [ ] Frontend PDF export button works
- [ ] Downloaded PDF has correct content
- [ ] No 500 errors in logs

---

## Files to Check

### AI Service Logs
Look for:
```
[PDF Export] ReportLab available as fallback
[PDF Export] Using ReportLab (WeasyPrint not available)
```

### Generated PDFs
- Should open in any PDF viewer
- Should show formatted content (headings, bullets)
- Should be readable and professional

---

## Troubleshooting Commands

### Check if ReportLab is installed
```bash
cd ai-service
python -c "import reportlab; print(f'ReportLab version: {reportlab.Version}')"
```

### Check if PDF exporter works
```bash
cd ai-service
python -c "from services.pdf_exporter import markdown_to_pdf_bytes; print('✓ PDF exporter ready')"
```

### Test PDF generation
```bash
cd ai-service
python -c "from services.pdf_exporter import markdown_to_pdf_bytes; pdf = markdown_to_pdf_bytes('# Test', 'resume', 'Test'); print(f'✓ Generated {len(pdf)} bytes')"
```

### Check API health
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy","service":"ai-content-generator"}
```

---

## Summary

1. **Restart AI service**: `cd ai-service && python main.py`
2. **Look for ReportLab message** in startup logs
3. **Test PDF export** via frontend or API
4. **Verify PDF downloads** and opens correctly

**PDF export is now working with ReportLab!** 🎉

No more WeasyPrint/GTK3 errors - everything works out of the box!
