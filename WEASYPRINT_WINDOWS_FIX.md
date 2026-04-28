# WeasyPrint PDF Export Fix for Windows

## Problem
WeasyPrint requires external libraries (GTK3, Pango, Cairo, GDK-PixBuf) that are not automatically installed on Windows.

Error message:
```
WeasyPrint could not import some external libraries.
```

## Solution Options

### Option 1: Install GTK3 Runtime (Recommended for Windows)

#### Step 1: Download GTK3 Runtime
Download the GTK3 runtime installer from:
https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases

**Direct link** (latest stable):
https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases/download/2022-01-04/gtk3-runtime-3.24.31-2022-01-04-ts-win64.exe

#### Step 2: Install GTK3
1. Run the downloaded `.exe` file
2. Follow the installation wizard
3. **Important**: Check "Add to PATH" during installation
4. Complete the installation

#### Step 3: Restart Terminal
Close and reopen your terminal/command prompt to load the new PATH.

#### Step 4: Verify Installation
```bash
# Check if GTK libraries are accessible
where libcairo-2.dll
where libpango-1.0-0.dll
```

Should show paths like:
```
C:\Program Files\GTK3-Runtime Win64\bin\libcairo-2.dll
C:\Program Files\GTK3-Runtime Win64\bin\libpango-1.0-0.dll
```

#### Step 5: Test WeasyPrint
```bash
cd ai-service
python -c "from weasyprint import HTML; print('WeasyPrint OK')"
```

Should output: `WeasyPrint OK`

---

### Option 2: Use Alternative PDF Library (Fallback)

If GTK3 installation fails, we can switch to an alternative PDF library that works better on Windows.

#### Install ReportLab (Pure Python, No External Dependencies)
```bash
cd ai-service
pip install reportlab
```

I'll create a fallback PDF exporter that uses ReportLab when WeasyPrint is unavailable.

---

### Option 3: Use Docker (Cross-Platform)

Run the AI service in Docker where all dependencies are pre-installed:

```dockerfile
FROM python:3.11-slim

# Install WeasyPrint dependencies
RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python", "main.py"]
```

---

## Quick Fix: Disable PDF Export Temporarily

If you need the service running immediately, you can disable PDF export:

### Modify `ai-service/routers/tools.py`

Find the PDF export endpoint and add a check:

```python
@router.post("/export/pdf")
async def export_pdf(request: PdfExportRequest):
    if not WEASYPRINT_AVAILABLE:
        raise HTTPException(
            status_code=501,
            detail="PDF export is not available. Please install GTK3 runtime."
        )
    # ... rest of the code
```

---

## Automated Fix Script

I'll create a script to detect and guide you through the installation.

---

## Testing After Fix

### Test 1: Import WeasyPrint
```bash
cd ai-service
python -c "from weasyprint import HTML; print('✓ WeasyPrint working')"
```

### Test 2: Generate Test PDF
```bash
cd ai-service
python -c "
from weasyprint import HTML
HTML(string='<h1>Test PDF</h1>').write_pdf('test.pdf')
print('✓ PDF generated: test.pdf')
"
```

### Test 3: Test via API
```bash
curl -X POST http://localhost:8000/export/pdf \
  -H "Content-Type: application/json" \
  -d '{
    "content": "# Test Resume\n\nThis is a test.",
    "content_type": "resume",
    "candidate_name": "Test User"
  }' \
  --output test_resume.pdf
```

---

## Troubleshooting

### Issue: "DLL load failed"
**Solution**: Make sure GTK3 bin directory is in PATH
```bash
# Add to PATH (PowerShell)
$env:Path += ";C:\Program Files\GTK3-Runtime Win64\bin"

# Or permanently via System Properties > Environment Variables
```

### Issue: "libcairo-2.dll not found"
**Solution**: Reinstall GTK3 runtime and ensure "Add to PATH" is checked

### Issue: Still not working after GTK3 install
**Solution**: 
1. Restart computer (not just terminal)
2. Verify PATH includes GTK3 bin directory
3. Try running Python as administrator

### Issue: GTK3 installer not available
**Solution**: Use Option 2 (ReportLab) or Option 3 (Docker)

---

## Alternative: Client-Side PDF Generation

Instead of server-side PDF generation, you can generate PDFs in the browser:

### Frontend Solution (No Server Dependencies)
```javascript
// Use jsPDF or html2pdf.js
import html2pdf from 'html2pdf.js';

const exportToPDF = (content) => {
  const element = document.createElement('div');
  element.innerHTML = content;
  
  html2pdf()
    .from(element)
    .save('document.pdf');
};
```

This approach:
- ✅ No server dependencies
- ✅ Works on all platforms
- ✅ Faster (no network round-trip)
- ❌ Less control over styling
- ❌ Requires JavaScript enabled

---

## Recommended Approach

**For Development (Windows)**:
1. Try Option 1 (GTK3 Runtime) first
2. If fails, use Option 2 (ReportLab fallback)

**For Production**:
1. Use Option 3 (Docker) for consistent environment
2. Or use client-side PDF generation

**For Quick Fix**:
1. Disable PDF export temporarily
2. Use HTML/Markdown export instead
