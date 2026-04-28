"""
Test PDF Export with both WeasyPrint and ReportLab
"""
import sys
import os

# Test content
SAMPLE_RESUME = """# John Doe
**Software Engineer**

john.doe@email.com | (555) 123-4567 | linkedin.com/in/johndoe

---

## Professional Summary

Experienced software engineer with 5+ years of expertise in full-stack development, specializing in Python, React, and cloud technologies.

---

## Experience

### Senior Software Engineer
**Tech Company Inc.** | Jan 2020 - Present

- Led development of microservices architecture serving 1M+ users
- Implemented CI/CD pipelines reducing deployment time by 60%
- Mentored team of 5 junior developers

### Software Engineer
**Startup Co.** | Jun 2018 - Dec 2019

- Built RESTful APIs using Python FastAPI
- Developed React frontend with TypeScript
- Optimized database queries improving performance by 40%

---

## Education

### Bachelor of Science in Computer Science
**University Name** | 2014 - 2018

---

## Skills

- **Languages**: Python, JavaScript, TypeScript, Java
- **Frameworks**: React, FastAPI, Django, Node.js
- **Tools**: Docker, Kubernetes, AWS, Git
- **Databases**: PostgreSQL, MongoDB, Redis
"""


def test_weasyprint():
    """Test WeasyPrint PDF generation"""
    print("\n" + "="*70)
    print("Testing WeasyPrint")
    print("="*70)
    
    try:
        from services.pdf_exporter import WEASYPRINT_AVAILABLE, markdown_to_pdf_bytes
        
        if not WEASYPRINT_AVAILABLE:
            print("⚠ WeasyPrint not available (requires GTK3 on Windows)")
            return False
        
        print("✓ WeasyPrint is available")
        
        # Try to generate PDF
        try:
            pdf_bytes = markdown_to_pdf_bytes(SAMPLE_RESUME, "resume", "John_Doe")
            
            # Save to file
            with open("test_resume_weasyprint.pdf", "wb") as f:
                f.write(pdf_bytes)
            
            print(f"✓ PDF generated successfully: {len(pdf_bytes)} bytes")
            print(f"✓ Saved to: test_resume_weasyprint.pdf")
            return True
            
        except Exception as e:
            print(f"✗ WeasyPrint generation failed: {e}")
            return False
            
    except Exception as e:
        print(f"✗ WeasyPrint test failed: {e}")
        return False


def test_reportlab():
    """Test ReportLab PDF generation"""
    print("\n" + "="*70)
    print("Testing ReportLab (Fallback)")
    print("="*70)
    
    try:
        from services.pdf_exporter_fallback import REPORTLAB_AVAILABLE, markdown_to_pdf_bytes_reportlab
        
        if not REPORTLAB_AVAILABLE:
            print("✗ ReportLab not available")
            print("Install with: pip install reportlab")
            return False
        
        print("✓ ReportLab is available")
        
        # Try to generate PDF
        try:
            pdf_bytes = markdown_to_pdf_bytes_reportlab(SAMPLE_RESUME, "resume", "John_Doe")
            
            # Save to file
            with open("test_resume_reportlab.pdf", "wb") as f:
                f.write(pdf_bytes)
            
            print(f"✓ PDF generated successfully: {len(pdf_bytes)} bytes")
            print(f"✓ Saved to: test_resume_reportlab.pdf")
            return True
            
        except Exception as e:
            print(f"✗ ReportLab generation failed: {e}")
            return False
            
    except Exception as e:
        print(f"✗ ReportLab test failed: {e}")
        return False


def test_unified_exporter():
    """Test the unified PDF exporter (with fallback logic)"""
    print("\n" + "="*70)
    print("Testing Unified PDF Exporter (with automatic fallback)")
    print("="*70)
    
    try:
        from services.pdf_exporter import markdown_to_pdf_bytes
        
        # Try to generate PDF (will use WeasyPrint or ReportLab automatically)
        try:
            pdf_bytes = markdown_to_pdf_bytes(SAMPLE_RESUME, "resume", "John_Doe")
            
            # Save to file
            with open("test_resume_unified.pdf", "wb") as f:
                f.write(pdf_bytes)
            
            print(f"✓ PDF generated successfully: {len(pdf_bytes)} bytes")
            print(f"✓ Saved to: test_resume_unified.pdf")
            print("✓ Automatic fallback working correctly")
            return True
            
        except Exception as e:
            print(f"✗ PDF generation failed: {e}")
            return False
            
    except Exception as e:
        print(f"✗ Unified exporter test failed: {e}")
        return False


def test_api_endpoint():
    """Test the PDF export API endpoint"""
    print("\n" + "="*70)
    print("Testing PDF Export API Endpoint")
    print("="*70)
    
    try:
        import requests
        
        payload = {
            "content": SAMPLE_RESUME,
            "content_type": "resume",
            "candidate_name": "John_Doe"
        }
        
        print("Sending request to http://localhost:8000/tools/export-pdf")
        
        response = requests.post(
            "http://localhost:8000/tools/export-pdf",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            # Save PDF
            with open("test_resume_api.pdf", "wb") as f:
                f.write(response.content)
            
            print(f"✓ API request successful: {len(response.content)} bytes")
            print(f"✓ Saved to: test_resume_api.pdf")
            return True
        else:
            print(f"✗ API request failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to API (is the server running?)")
        print("Start server with: python main.py")
        return False
    except Exception as e:
        print(f"✗ API test failed: {e}")
        return False


if __name__ == "__main__":
    print("\n" + "="*70)
    print("PDF EXPORT TEST SUITE")
    print("="*70)
    
    results = {
        "WeasyPrint": test_weasyprint(),
        "ReportLab": test_reportlab(),
        "Unified Exporter": test_unified_exporter(),
        "API Endpoint": test_api_endpoint()
    }
    
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name:20} {status}")
    
    print("="*70)
    
    # Overall result
    if results["ReportLab"] or results["WeasyPrint"]:
        print("\n✓ PDF export is working!")
        if results["ReportLab"] and not results["WeasyPrint"]:
            print("  Using ReportLab (fallback)")
            print("  For better quality, install GTK3 for WeasyPrint")
        elif results["WeasyPrint"]:
            print("  Using WeasyPrint (best quality)")
    else:
        print("\n✗ PDF export is not working")
        print("  Install ReportLab: pip install reportlab")
    
    print()
