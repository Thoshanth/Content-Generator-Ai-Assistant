"""
Test script for follow-up questions endpoint
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_followup_questions():
    """Test the follow-up questions endpoint"""
    
    print("=" * 60)
    print("Testing Follow-Up Questions Endpoint")
    print("=" * 60)
    
    # Test cases
    test_cases = [
        {
            "name": "Resume - No initial prompt",
            "data": {
                "content_type": "resume",
                "initial_prompt": "",
                "user_id": "test123"
            }
        },
        {
            "name": "Resume - With initial prompt",
            "data": {
                "content_type": "resume",
                "initial_prompt": "I need help creating a resume for a software engineer position at Google",
                "user_id": "test123"
            }
        },
        {
            "name": "Cover Letter",
            "data": {
                "content_type": "cover_letter",
                "initial_prompt": "I'm applying for a data scientist role",
                "user_id": "test123"
            }
        },
        {
            "name": "Blog Post",
            "data": {
                "content_type": "blog_post",
                "initial_prompt": "I want to write about AI and machine learning",
                "user_id": "test123"
            }
        },
        {
            "name": "Email",
            "data": {
                "content_type": "email",
                "initial_prompt": "I need to write a professional email to my manager",
                "user_id": "test123"
            }
        },
        {
            "name": "General",
            "data": {
                "content_type": "general",
                "initial_prompt": "",
                "user_id": "test123"
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n{'─' * 60}")
        print(f"Test: {test_case['name']}")
        print(f"{'─' * 60}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/followup/questions",
                json=test_case['data'],
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Success!")
                print(f"Content Type: {data['content_type']}")
                print(f"Number of Questions: {len(data['questions'])}")
                print("\nQuestions:")
                for i, question in enumerate(data['questions'], 1):
                    print(f"  {i}. {question}")
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection Error: Make sure the AI service is running on port 8000")
            print("   Run: cd ai-service && python main.py")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print(f"\n{'=' * 60}")
    print("Testing Complete!")
    print(f"{'=' * 60}")


def test_templates_endpoint():
    """Test the templates endpoint"""
    
    print("\n" + "=" * 60)
    print("Testing Templates Endpoint")
    print("=" * 60)
    
    content_types = ["resume", "cover_letter", "blog_post", "email", "social_media", "general"]
    
    for content_type in content_types:
        print(f"\n{'─' * 60}")
        print(f"Content Type: {content_type}")
        print(f"{'─' * 60}")
        
        try:
            response = requests.get(
                f"{BASE_URL}/followup/templates/{content_type}",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Success!")
                print(f"Number of Templates: {len(data['questions'])}")
                print("\nTemplate Questions:")
                for i, question in enumerate(data['questions'], 1):
                    print(f"  {i}. {question}")
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection Error: Make sure the AI service is running on port 8000")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print(f"\n{'=' * 60}")
    print("Testing Complete!")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    print("\n🚀 Starting Follow-Up Questions Tests\n")
    
    # Test both endpoints
    test_followup_questions()
    test_templates_endpoint()
    
    print("\n✨ All tests completed!\n")
