"""
Test Resume Generation with Exact Format
Tests that generated resumes match the provided example format.
"""
import requests
import json
import re

BASE_URL = "http://localhost:8000"

# Sample user information (similar to the provided resume)
SAMPLE_USER_INFO = """
Name: S.N. Thoshanth Reddy Mandapati
Email: mthoshanthreddy@gmail.com
Phone: +91-7989192738
Location: Hyderabad, Telangana
LinkedIn: Thoshanth Reddy
GitHub: github.com/thoshhhh

Education: B.Tech in Computer Science and Engineering (2nd Year) at Hyderabad Institute of Technology and Management (HITAM), CGPA: 7.7/10, Aug 2024 - Present
Relevant Coursework: Machine Learning, Data Structures & Algorithms, DBMS, Linear Algebra, Operating Systems

Skills:
- Languages: Python, Java, SQL
- ML Frameworks: TensorFlow, Keras, PyTorch, Scikit-learn, HuggingFace Transformers
- Computer Vision: OpenCV, CNN architectures, ROI segmentation, contour extraction, image augmentation
- NLP: NLTK, TF-IDF, BERT, DistilBERT, tokenization, text classification, LLM fine-tuning
- Data Science: NumPy, Pandas, Matplotlib, Seaborn, feature engineering, cross-validation, ROC-AUC
- Tools: Git, GitHub, Jupyter Notebook, VS Code, Google Colab

Experience:
1. Artificial Intelligence Engineer Intern at Galactix Solutions Pvt Ltd (Jan 2026 - Present, Hyderabad)
   - Deployed 2 computer vision ML pipelines using TensorFlow and Scikit-learn, cutting inspection time by ~30% across 3 production modules
   - Rebuilt CNN classifier with OpenCV preprocessing on 10,000+ images — contour extraction, ROI segmentation, augmentation — raising F1-score by 8%
   - Documented architecture and evaluation metrics for 2 product releases; presented results to 5 engineers

2. Research Intern at National Institute of Technology (NIT) Warangal (May 2026 - Jul 2026, Warangal)
   - Fine-tuned BERT and DistilBERT on 15,000 text samples; matched published F1-score baseline within 2% in 3 iterations
   - Ran ablation studies across 6 model configurations; documented tokenization and attention hyperparameter results
   - Co-authored a 12-page research report; presented to 10+ faculty and peers after 3 revision rounds

Projects:
1. Real-Time Sign-to-Speech Language Converter (Jan 2025 - Apr 2025)
   Technologies: Python, TensorFlow, OpenCV, Tkinter, gTTS
   - Trained a CNN on 87,000 ASL images across 29 classes achieving 98.6% validation accuracy; trained in under 4 hours on CPU-only hardware
   - Engineered OpenCV pipeline — contour extraction, ROI segmentation — delivering sub-100 ms inference per frame without GPU
   - Built Tkinter GUI with live confidence display; tested with 5 non-technical users, all successful without instruction

2. Spam Bot Detection System (May 2025 - Jun 2025)
   Technologies: Python, Scikit-learn, NLTK
   - Trained Logistic Regression on 5,574 SMS messages achieving 97.4% accuracy and 96.8% F1-score via TF-IDF over 50,000 features
   - Reduced false-positive rate to under 1.5% by tuning decision threshold across 15 values via ROC-AUC analysis

3. Diabetes Prediction using Machine Learning (Jul 2025 - Aug 2025)
   Technologies: Python, Scikit-learn, Pandas, Matplotlib
   - Benchmarked Random Forest, SVM, and KNN on 768 records; Random Forest achieved 79.2% accuracy and 0.86 AUC after fixing nulls in 3 columns
   - Reduced features from 8 to 5 via importance ranking; validated with 5-fold cross-validation

Certifications:
- Complete Python Bootcamp: Zero to Hero | Udemy: Mar 2025
- Fundamentals of DevOps on AWS | Simplilearn: Jan 2026
"""


def test_resume_generation():
    """Test resume generation with sample user info"""
    
    print("\n" + "="*80)
    print("TESTING RESUME GENERATION - EXACT FORMAT")
    print("="*80)
    
    payload = {
        "prompt": f"Create a professional resume with this information:\n\n{SAMPLE_USER_INFO}",
        "content_type": "resume",
        "tone": "professional",
        "length": "medium",
        "language": "English",
        "user_id": "test-user-123"
    }
    
    print(f"\nRequest: POST {BASE_URL}/chat/")
    print(f"Content Type: resume")
    print(f"Generating resume...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/chat/",
            json=payload,
            timeout=60
        )
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            content = data.get('content', '')
            provider = data.get('provider', 'Unknown')
            model = data.get('model', 'Unknown')
            word_count = data.get('word_count', 0)
            
            print(f"\n✓ Resume Generated Successfully!")
            print(f"Provider: {provider}")
            print(f"Model: {model}")
            print(f"Word Count: {word_count}")
            
            # Save to file
            with open("generated_resume.md", "w", encoding="utf-8") as f:
                f.write(content)
            print(f"\n✓ Saved to: generated_resume.md")
            
            # Verify format
            print("\n" + "="*80)
            print("FORMAT VERIFICATION")
            print("="*80)
            
            checks = verify_resume_format(content)
            
            print("\nFormat Checks:")
            print("-" * 80)
            for check, passed in checks.items():
                status = "✓" if passed else "✗"
                print(f"{status} {check}")
            print("-" * 80)
            
            # Display resume preview
            print("\n" + "="*80)
            print("GENERATED RESUME PREVIEW")
            print("="*80)
            print(content[:1500] + "..." if len(content) > 1500 else content)
            print("="*80)
            
            # Overall result
            all_passed = all(checks.values())
            if all_passed:
                print("\n✓ ALL FORMAT CHECKS PASSED!")
                print("Resume matches the exact format from the example.")
            else:
                print("\n⚠ SOME FORMAT CHECKS FAILED")
                print("Review the generated resume for formatting issues.")
            
            return all_passed
            
        else:
            print(f"\n✗ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"\n✗ Exception: {str(e)}")
        return False


def verify_resume_format(content: str) -> dict:
    """
    Verify that the resume matches the expected format.
    
    Returns:
        Dictionary of checks and their pass/fail status
    """
    checks = {}
    
    # Check 1: Has H1 header (name)
    checks["Has H1 header (# NAME)"] = bool(re.search(r'^# .+', content, re.MULTILINE))
    
    # Check 2: Has required sections
    required_sections = ["SUMMARY", "SKILLS", "EXPERIENCE", "PROJECTS", "EDUCATION"]
    for section in required_sections:
        checks[f"Has {section} section"] = section.upper() in content.upper()
    
    # Check 3: Uses bullet symbols (• and ◦)
    checks["Uses • bullet symbol"] = "•" in content
    checks["Uses ◦ sub-bullet symbol"] = "◦" in content
    
    # Check 4: Has bold numbers (looking for **number**)
    checks["Has bold numbers (**X**)"] = bool(re.search(r'\*\*\d+', content))
    
    # Check 5: Has italic text (looking for *text*)
    checks["Has italic text (*text*)"] = bool(re.search(r'\*[^*]+\*', content))
    
    # Check 6: Has em dashes (—)
    checks["Uses em dash (—)"] = "—" in content
    
    # Check 7: Has contact information
    checks["Has email"] = bool(re.search(r'[\w\.-]+@[\w\.-]+', content))
    checks["Has phone"] = bool(re.search(r'\+?\d[\d\s\-()]+', content))
    
    # Check 8: Has quantified achievements (numbers with %)
    checks["Has percentage metrics"] = bool(re.search(r'\d+\.?\d*%', content))
    
    # Check 9: Has duration format (Month Year - Month Year)
    checks["Has duration format"] = bool(re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}', content))
    
    return checks


def test_streaming_resume():
    """Test streaming resume generation"""
    
    print("\n" + "="*80)
    print("TESTING STREAMING RESUME GENERATION")
    print("="*80)
    
    payload = {
        "prompt": f"Create a professional resume:\n\n{SAMPLE_USER_INFO}",
        "content_type": "resume",
        "tone": "professional",
        "length": "medium",
        "language": "English",
        "user_id": "test-user-123"
    }
    
    print(f"\nRequest: POST {BASE_URL}/chat/stream")
    print(f"Content Type: resume")
    print(f"Streaming response...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/chat/stream",
            json=payload,
            stream=True,
            timeout=60
        )
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            full_content = ""
            provider_info = {}
            
            print("\nStreaming chunks:")
            print("-" * 80)
            
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith('data: '):
                        data_str = line_str[6:]
                        try:
                            data = json.loads(data_str)
                            
                            if 'provider' in data:
                                provider_info = data
                                print(f"Provider: {data.get('provider')} | Model: {data.get('model')}")
                            
                            if 'delta' in data:
                                full_content += data['delta']
                                # Print first few chunks
                                if len(full_content) < 200:
                                    print(data['delta'], end='', flush=True)
                            
                            if data.get('done'):
                                print(f"\n\n✓ Streaming complete!")
                                print(f"Word Count: {data.get('word_count')}")
                                print(f"Char Count: {data.get('char_count')}")
                                break
                                
                        except json.JSONDecodeError:
                            continue
            
            print("-" * 80)
            
            # Save streamed content
            with open("generated_resume_stream.md", "w", encoding="utf-8") as f:
                f.write(full_content)
            print(f"\n✓ Saved to: generated_resume_stream.md")
            
            return True
            
        else:
            print(f"\n✗ Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"\n✗ Exception: {str(e)}")
        return False


if __name__ == "__main__":
    print("\n" + "="*80)
    print("RESUME GENERATION TEST SUITE")
    print("="*80)
    print("\nThis test will:")
    print("1. Generate a resume using the non-streaming endpoint")
    print("2. Verify the format matches the example (bullets, bold, italic, etc.)")
    print("3. Test streaming resume generation")
    print("4. Save generated resumes to files for manual review")
    
    input("\nPress Enter to start tests (make sure AI service is running)...")
    
    # Test 1: Non-streaming resume generation
    result1 = test_resume_generation()
    
    # Test 2: Streaming resume generation
    result2 = test_streaming_resume()
    
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Non-Streaming Resume: {'✓ PASSED' if result1 else '✗ FAILED'}")
    print(f"Streaming Resume: {'✓ PASSED' if result2 else '✗ FAILED'}")
    print("="*80)
    
    print("\n📄 Generated Files:")
    print("  - generated_resume.md (non-streaming)")
    print("  - generated_resume_stream.md (streaming)")
    print("\nPlease review these files to verify the format matches your example!")
    print("="*80 + "\n")
