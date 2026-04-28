"""
Test Follow-up Questions API
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_resume_followup_questions():
    """Test follow-up questions for resume"""
    
    print("\n" + "="*70)
    print("Testing Follow-up Questions API - Resume")
    print("="*70)
    
    payload = {
        "content_type": "resume",
        "content": "I want to create a resume for a software engineer position",
        "user_id": "test-user-123"
    }
    
    print(f"\nRequest: POST {BASE_URL}/tools/followup-questions")
    print(f"Content Type: resume")
    
    try:
        response = requests.post(
            f"{BASE_URL}/tools/followup-questions",
            json=payload,
            timeout=30
        )
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✓ Success!")
            print(f"Content Type: {data.get('content_type')}")
            print(f"Number of Questions: {len(data.get('questions', []))}")
            print(f"\nFollow-up Questions:")
            print("-" * 70)
            for i, question in enumerate(data.get('questions', []), 1):
                print(f"{i}. {question}")
            print("-" * 70)
            return True
        else:
            print(f"\n✗ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"\n✗ Exception: {str(e)}")
        return False


def test_cover_letter_followup():
    """Test follow-up questions for cover letter"""
    
    print("\n" + "="*70)
    print("Testing Follow-up Questions API - Cover Letter")
    print("="*70)
    
    payload = {
        "content_type": "cover_letter",
        "content": "",
        "user_id": "test-user-123"
    }
    
    print(f"\nRequest: POST {BASE_URL}/tools/followup-questions")
    print(f"Content Type: cover_letter")
    print(f"Initial Content: (empty)")
    
    try:
        response = requests.post(
            f"{BASE_URL}/tools/followup-questions",
            json=payload,
            timeout=30
        )
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✓ Success!")
            print(f"Number of Questions: {len(data.get('questions', []))}")
            print(f"\nFollow-up Questions:")
            print("-" * 70)
            for i, question in enumerate(data.get('questions', []), 1):
                print(f"{i}. {question}")
            print("-" * 70)
            return True
        else:
            print(f"\n✗ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"\n✗ Exception: {str(e)}")
        return False


if __name__ == "__main__":
    print("\n" + "="*70)
    print("FOLLOW-UP QUESTIONS API TEST")
    print("="*70)
    print("\nThis test will:")
    print("1. Request follow-up questions for resume generation")
    print("2. Request follow-up questions for cover letter generation")
    print("3. Display the questions returned by the API")
    
    input("\nPress Enter to start tests (make sure AI service is running)...")
    
    # Test 1: Resume follow-up questions
    result1 = test_resume_followup_questions()
    
    # Test 2: Cover letter follow-up questions
    result2 = test_cover_letter_followup()
    
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Resume Follow-up Questions: {'✓ PASSED' if result1 else '✗ FAILED'}")
    print(f"Cover Letter Follow-up Questions: {'✓ PASSED' if result2 else '✗ FAILED'}")
    print("="*70 + "\n")
