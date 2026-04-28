"""
Test script for bot-asks-user follow-up questions
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_bot_followup_flow():
    """Test the complete bot-asks-user follow-up flow"""
    
    print("=" * 70)
    print("Testing Bot-Asks-User Follow-Up Questions Flow")
    print("=" * 70)
    
    # Test scenarios
    test_scenarios = [
        {
            "name": "Resume - Brief Request",
            "content_type": "resume",
            "user_message": "I need a resume",
            "should_ask_followup": True
        },
        {
            "name": "Resume - Detailed Request", 
            "content_type": "resume",
            "user_message": "I need a resume for a software engineer position at Google. I have 5 years of experience in Python and React, graduated from MIT with a CS degree, and worked at Microsoft and Amazon.",
            "should_ask_followup": False
        },
        {
            "name": "Cover Letter - Brief Request",
            "content_type": "cover_letter", 
            "user_message": "Help me write a cover letter",
            "should_ask_followup": True
        },
        {
            "name": "General Chat",
            "content_type": "general",
            "user_message": "Hello, how are you?",
            "should_ask_followup": False
        },
        {
            "name": "Blog Post - Brief Request",
            "content_type": "blog_post",
            "user_message": "I want to write a blog post",
            "should_ask_followup": True
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n{'─' * 70}")
        print(f"Scenario: {scenario['name']}")
        print(f"Content Type: {scenario['content_type']}")
        print(f"User Message: {scenario['user_message']}")
        print(f"Expected Follow-up: {scenario['should_ask_followup']}")
        print(f"{'─' * 70}")
        
        # Step 1: Check if bot should ask follow-up questions
        print("\n1. Checking if bot should ask follow-up questions...")
        try:
            check_response = requests.post(
                f"{BASE_URL}/followup/check",
                json={
                    "content_type": scenario["content_type"],
                    "user_message": scenario["user_message"],
                    "conversation_history": [],
                    "user_id": "test123"
                },
                timeout=10
            )
            
            if check_response.status_code == 200:
                check_data = check_response.json()
                should_ask = check_data["should_ask"]
                reason = check_data.get("reason", "")
                
                print(f"   ✅ Should ask follow-up: {should_ask}")
                print(f"   📝 Reason: {reason}")
                
                # Verify expectation
                if should_ask == scenario["should_ask_followup"]:
                    print(f"   ✅ Matches expectation!")
                else:
                    print(f"   ❌ Expected {scenario['should_ask_followup']}, got {should_ask}")
                
                # Step 2: If should ask, generate the follow-up message
                if should_ask:
                    print("\n2. Generating bot follow-up message...")
                    
                    generate_response = requests.post(
                        f"{BASE_URL}/followup/generate",
                        json={
                            "content_type": scenario["content_type"],
                            "user_message": scenario["user_message"],
                            "conversation_history": [],
                            "user_id": "test123"
                        },
                        timeout=30
                    )
                    
                    if generate_response.status_code == 200:
                        generate_data = generate_response.json()
                        message = generate_data["message"]
                        has_questions = generate_data["has_questions"]
                        
                        print(f"   ✅ Generated message successfully!")
                        print(f"   📝 Has questions: {has_questions}")
                        print(f"   💬 Bot message:")
                        print("   " + "─" * 50)
                        for line in message.split('\n'):
                            print(f"   {line}")
                        print("   " + "─" * 50)
                    else:
                        print(f"   ❌ Failed to generate message: {generate_response.status_code}")
                        print(f"   📝 Error: {generate_response.text}")
                else:
                    print("\n2. No follow-up needed - bot would generate regular content")
                
            else:
                print(f"   ❌ Check failed: {check_response.status_code}")
                print(f"   📝 Error: {check_response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection Error: Make sure the AI service is running on port 8000")
            print("   Run: cd ai-service && python main.py")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print(f"\n{'=' * 70}")
    print("Testing Complete!")
    print(f"{'=' * 70}")


def test_chat_integration():
    """Test the integrated chat endpoint with follow-up questions"""
    
    print("\n" + "=" * 70)
    print("Testing Chat Integration with Follow-Up Questions")
    print("=" * 70)
    
    # Test chat scenarios
    chat_scenarios = [
        {
            "name": "Resume Request - Should Get Follow-up",
            "request": {
                "prompt": "I need help creating a resume",
                "content_type": "resume",
                "tone": "professional",
                "length": "auto",
                "language": "English",
                "conversation_history": [],
                "user_id": "test123"
            }
        },
        {
            "name": "General Chat - Should Get Regular Response",
            "request": {
                "prompt": "Hello, how are you today?",
                "content_type": "general", 
                "tone": "friendly",
                "length": "auto",
                "language": "English",
                "conversation_history": [],
                "user_id": "test123"
            }
        }
    ]
    
    for scenario in chat_scenarios:
        print(f"\n{'─' * 70}")
        print(f"Chat Scenario: {scenario['name']}")
        print(f"{'─' * 70}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/chat/",
                json=scenario["request"],
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                content = data["content"]
                provider = data["provider"]
                model = data["model"]
                
                print(f"✅ Chat response received!")
                print(f"📝 Provider: {provider}")
                print(f"🤖 Model: {model}")
                print(f"💬 Response:")
                print("─" * 50)
                for line in content.split('\n')[:10]:  # Show first 10 lines
                    print(line)
                if len(content.split('\n')) > 10:
                    print("... (truncated)")
                print("─" * 50)
                
                # Check if it's a follow-up response
                if provider == "followup_service":
                    print("🎯 This is a follow-up question response!")
                else:
                    print("💭 This is a regular AI response")
                    
            else:
                print(f"❌ Chat failed: {response.status_code}")
                print(f"📝 Error: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection Error: Make sure the AI service is running on port 8000")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print(f"\n{'=' * 70}")
    print("Chat Integration Testing Complete!")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    print("\n🤖 Starting Bot-Asks-User Follow-Up Tests\n")
    
    # Test the follow-up flow
    test_bot_followup_flow()
    
    # Test chat integration
    test_chat_integration()
    
    print("\n✨ All tests completed!\n")
    print("📋 Summary:")
    print("   - Bot now asks users follow-up questions automatically")
    print("   - Questions appear as regular AI responses in chat")
    print("   - No more clickable question cards needed")
    print("   - Natural conversation flow like Claude AI")