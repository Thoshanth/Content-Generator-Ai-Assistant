"""
Test the new non-streaming /chat/ endpoint
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_non_streaming_chat():
    """Test the non-streaming chat endpoint"""
    
    payload = {
        "prompt": "Write a short professional email to schedule a meeting",
        "content_type": "email",
        "tone": "professional",
        "length": "short",
        "language": "English",
        "conversation_history": [],
        "user_id": "test-user-123",
        "regenerate": False
    }
    
    print("\n" + "="*70)
    print("Testing Non-Streaming Chat Endpoint")
    print("="*70)
    print(f"\nRequest: POST {BASE_URL}/chat/")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/chat/",
            json=payload,
            timeout=30
        )
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✓ Success!")
            print(f"Provider: {data.get('provider')}")
            print(f"Model: {data.get('model')}")
            print(f"Word Count: {data.get('word_count')}")
            print(f"Char Count: {data.get('char_count')}")
            print(f"\nContent Preview:")
            print("-" * 70)
            content = data.get('content', '')
            print(content[:300] + "..." if len(content) > 300 else content)
            print("-" * 70)
            return True
        else:
            print(f"\n✗ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"\n✗ Exception: {str(e)}")
        return False


def test_resume_generation():
    """Test resume generation specifically (the failing case)"""
    
    payload = {
        "prompt": "Generate a resume for a software engineer with 5 years of experience in Python and React",
        "content_type": "resume",
        "tone": "professional",
        "length": "medium",
        "language": "English",
        "conversation_history": [],
        "user_id": "test-user-123",
        "regenerate": False
    }
    
    print("\n" + "="*70)
    print("Testing Resume Generation (Non-Streaming)")
    print("="*70)
    print(f"\nRequest: POST {BASE_URL}/chat/")
    print(f"Content Type: resume")
    
    try:
        response = requests.post(
            f"{BASE_URL}/chat/",
            json=payload,
            timeout=30
        )
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✓ Resume Generated Successfully!")
            print(f"Provider: {data.get('provider')}")
            print(f"Model: {data.get('model')}")
            print(f"Word Count: {data.get('word_count')}")
            print(f"Char Count: {data.get('char_count')}")
            print(f"\nResume Preview:")
            print("-" * 70)
            content = data.get('content', '')
            print(content[:500] + "..." if len(content) > 500 else content)
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
    print("NON-STREAMING ENDPOINT TEST")
    print("="*70)
    print("\nMake sure the AI service is running on http://localhost:8000")
    print("Run: cd ai-service && python main.py")
    
    input("\nPress Enter to start tests...")
    
    # Test 1: Basic email generation
    result1 = test_non_streaming_chat()
    
    # Test 2: Resume generation (the failing case)
    result2 = test_resume_generation()
    
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Email Generation: {'✓ PASSED' if result1 else '✗ FAILED'}")
    print(f"Resume Generation: {'✓ PASSED' if result2 else '✗ FAILED'}")
    print("="*70 + "\n")
