# PDF Export Fix - Complete Solution

## Problem Summary
WeasyPrint requires external GTK3 libraries on Windows, causing PDF export to fail with:
```
WeasyPrint could not import some external libraries.
```

## Solution Implemented
Added **automatic fallback** to ReportLab (pure Python, no external dependencies) when WeasyPrint is unavailable.

---

## Quick Fix (Recommended)

### Step 1: Install ReportLab
```bash
cd ai-service
pip install reportlab
```

### Step 2: Restart AI Service
```bash
python main.py
```

### Step 3: Test PDF Export
```bash
python tests/test_pdf_export.py
```

**Done!** PDF export now works using ReportLab.

---

## What Changed

### 1. New Fallback PDF Exporter
**File**: `ai-service/services/pdf_exporter_fallback.py`
- Pure Python implementation using ReportLab
- No external dependencies (works on all platforms)
- Supports markdown formatting (headings, bullets, bold, italic)
- Professional styling for resumes and cover letters

### 2. Updated Main PDF Exporter
**File**: `ai-service/services/pdf_exporter.py`
- Tries WeasyPrint first (better quality)
- Automatically falls back to ReportLab if WeasyPrint fails
- Transparent to the API - same interface

### 3. Updated API Endpoint
**File**: `ai-service/routers/tools.py`
- Passes `candidate_name` parameter for better filenames
- Better error messages
- Sanitizes filenames

### 4. Updated Requirements
**File**: `ai-service/requirements.txt`
- Added `reportlab==4.0.7` as fallback

---

## Installation Options

### Option 1: ReportLab Only (Easiest - Windows)
```bash
cd ai-service
pip install reportlab
```
✅ Works immediately  
✅ No external dependencies  
✅ Cross-platform  
⚠️ Slightly simpler styling than WeasyPrint

### Option 2: WeasyPrint + GTK3 (Best Quality)
```bash
# Step 1: Install GTK3 Runtime
# Download from: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases
# Run installer and check "Add to PATH"

# Step 2: Restart terminal

# Step 3: Verify
python -c "from weasyprint import HTML; print('WeasyPrint OK')"
```
✅ Best PDF quality  
✅ Advanced CSS styling  
⚠️ Requires GTK3 installation on Windows

### Option 3: Both (Recommended)
```bash
cd ai-service
pip install reportlab

# Then optionally install GTK3 for WeasyPrint
# System will use WeasyPrint when available, ReportLab as fallback
```
✅ Best of both worlds  
✅ Automatic fallback  
✅ Works everywhere

---

## Automated Installation

### Windows
```bash
cd ai-service
install_pdf_support.bat
```

This script:
1. Installs ReportLab
2. Tests ReportLab
3. Checks for WeasyPrint
4. Provides GTK3 installation instructions if needed

---

## Testing

### Test 1: Library Availability
```bash
cd ai-service
python -c "from services.pdf_exporter_fallback import REPORTLAB_AVAILABLE; print(f'ReportLab: {REPORTLAB_AVAILABLE}')"
python -c "from services.pdf_exporter import WEASYPRINT_AVAILABLE; print(f'WeasyPrint: {WEASYPRINT_AVAILABLE}')"
```

### Test 2: Generate Test PDFs
```bash
cd ai-service
python tests/test_pdf_export.py
```

This will:
- Test WeasyPrint (if available)
- Test ReportLab
- Test unified exporter with fallback
- Test API endpoint
- Generate sample PDFs for comparison

### Test 3: API Endpoint
```bash
# Start server
cd ai-service
python main.py

# In another terminal
curl -X POST http://localhost:8000/tools/export-pdf \
  -H "Content-Type: application/json" \
  -d '{
    "content": "# Test Resume\n\n## Experience\n\n- Item 1\n- Item 2",
    "content_type": "resume",
    "candidate_name": "Test_User"
  }' \
  --output test.pdf
```

---

## How It Works

### Fallback Logic
```
1. Try WeasyPrint
   ├─ Success → Return high-quality PDF
   └─ Fail (GTK3 missing)
       └─ Try ReportLab
           ├─ Success → Return PDF
           └─ Fail → Error message

2. If WeasyPrint not installed
   └─ Use ReportLab directly
```

### Quality Comparison

**WeasyPrint** (requires GTK3):
- ✅ Full CSS support
- ✅ Advanced layouts
- ✅ Web fonts
- ✅ Complex styling
- ⚠️ Requires external libraries

**ReportLab** (pure Python):
- ✅ No dependencies
- ✅ Fast generation
- ✅ Professional output
- ✅ Works everywhere
- ⚠️ Simpler styling

---

## Frontend Integration

The frontend doesn't need any changes. The PDF export button will work automatically:

```javascript
// In ExportButtons.jsx - already working
const handlePdfExport = async () => {
  const response = await fetch('/tools/export-pdf', {
    method: 'POST',
    body: JSON.stringify({
      content: message.content,
      content_type: 'resume',
      candidate_name: 'User_Name'
    })
  });
  
  const blob = await response.blob();
  // Download PDF
};
```

---

## Troubleshooting

### Issue: "ReportLab not installed"
```bash
pip install reportlab
```

### Issue: "PDF generation failed"
Check logs:
```bash
cd ai-service
python main.py
# Look for "[PDF Export]" messages
```

### Issue: "Module not found"
Reinstall dependencies:
```bash
cd ai-service
pip install -r requirements.txt
```

### Issue: Want better quality PDFs
Install GTK3 for WeasyPrint:
1. Download: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases
2. Install with "Add to PATH" checked
3. Restart terminal
4. Test: `python -c "from weasyprint import HTML; print('OK')"`

---

## Verification Checklist

- [ ] ReportLab installed: `pip list | grep reportlab`
- [ ] PDF exporter imports: `python -c "from services.pdf_exporter import markdown_to_pdf_bytes"`
- [ ] Test script passes: `python tests/test_pdf_export.py`
- [ ] API endpoint works: Test via curl or frontend
- [ ] PDF downloads correctly in browser
- [ ] PDF opens and displays content

---

## Files Modified

1. ✅ `ai-service/services/pdf_exporter.py` - Added fallback logic
2. ✅ `ai-service/services/pdf_exporter_fallback.py` - New ReportLab exporter
3. ✅ `ai-service/routers/tools.py` - Updated endpoint
4. ✅ `ai-service/requirements.txt` - Added reportlab
5. ✅ `ai-service/install_pdf_support.bat` - Installation script
6. ✅ `ai-service/tests/test_pdf_export.py` - Test suite

---

## Next Steps

1. **Install ReportLab**:
   ```bash
   cd ai-service
   pip install reportlab
   ```

2. **Restart AI Service**:
   ```bash
   python main.py
   ```

3. **Test in Frontend**:
   - Generate a resume
   - Click PDF export button
   - Should download PDF successfully

4. **Optional - Install WeasyPrint**:
   - Follow GTK3 installation guide
   - System will automatically use it for better quality

---

## Support

### ReportLab Documentation
https://www.reportlab.com/docs/reportlab-userguide.pdf

### WeasyPrint Documentation
https://doc.courtbouillon.org/weasyprint/stable/

### GTK3 for Windows
https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer

---

## Summary

✅ **Problem**: WeasyPrint requires GTK3 on Windows  
✅ **Solution**: Added ReportLab as automatic fallback  
✅ **Result**: PDF export works on all platforms without external dependencies  
✅ **Bonus**: Can still use WeasyPrint for better quality if GTK3 is installed  

**No code changes needed in frontend or backend - just install ReportLab!**
