"""
Quick test for PDF export API endpoint
"""
import requests
import json

BASE_URL = "http://localhost:8000"

# Sample resume content
SAMPLE_CONTENT = """# John Doe
**Software Engineer**

john.doe@email.com | (555) 123-4567

---

## Professional Summary

Experienced software engineer with 5+ years of expertise in full-stack development.

---

## Experience

### Senior Software Engineer
**Tech Company Inc.** | Jan 2020 - Present

- Led development of microservices architecture
- Implemented CI/CD pipelines
- Mentored team of 5 junior developers

---

## Skills

- **Languages**: Python, JavaScript, TypeScript
- **Frameworks**: React, FastAPI, Django
- **Tools**: Docker, Kubernetes, AWS
"""

def test_pdf_export():
    """Test the PDF export endpoint"""
    
    print("\n" + "="*70)
    print("Testing PDF Export API Endpoint")
    print("="*70)
    
    payload = {
        "content": SAMPLE_CONTENT,
        "content_type": "resume",
        "candidate_name": "John_Doe"
    }
    
    print(f"\nRequest: POST {BASE_URL}/tools/export-pdf")
    print(f"Content Type: resume")
    print(f"Candidate Name: John_Doe")
    
    try:
        response = requests.post(
            f"{BASE_URL}/tools/export-pdf",
            json=payload,
            timeout=30
        )
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            # Save PDF
            filename = "test_resume_output.pdf"
            with open(filename, "wb") as f:
                f.write(response.content)
            
            print(f"✓ PDF Export Successful!")
            print(f"✓ File size: {len(response.content)} bytes")
            print(f"✓ Saved to: {filename}")
            print(f"\nYou can now open {filename} to verify the PDF")
            return True
        else:
            print(f"✗ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to API")
        print("\nMake sure the AI service is running:")
        print("  cd ai-service")
        print("  python main.py")
        return False
    except Exception as e:
        print(f"✗ Exception: {str(e)}")
        return False


if __name__ == "__main__":
    print("\n" + "="*70)
    print("PDF EXPORT API TEST")
    print("="*70)
    print("\nThis test will:")
    print("1. Send a resume to the PDF export endpoint")
    print("2. Save the generated PDF to test_resume_output.pdf")
    print("3. Verify the PDF was created successfully")
    
    input("\nPress Enter to start test (make sure AI service is running)...")
    
    success = test_pdf_export()
    
    print("\n" + "="*70)
    if success:
        print("✓ TEST PASSED - PDF export is working!")
    else:
        print("✗ TEST FAILED - Check error messages above")
    print("="*70 + "\n")
