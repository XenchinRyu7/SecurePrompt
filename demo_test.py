"""
Demo script untuk testing SecurePrompt API
"""
import requests
import json

# Base URL untuk API
BASE_URL = "http://localhost:8000/api/v1"

def test_api():
    """Test SecurePrompt API dengan berbagai contoh prompt"""
    
    print("🔐 SecurePrompt API Testing Demo")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        {
            "name": "Safe Prompt",
            "prompt": "What is the weather today?",
            "expected": "SAFE"
        },
        {
            "name": "Password Prompt", 
            "prompt": "What is my password?",
            "expected": "SENSITIVE"
        },
        {
            "name": "Email Prompt",
            "prompt": "Send this to my email address",
            "expected": "SENSITIVE"
        },
        {
            "name": "NIK Prompt",
            "prompt": "My NIK is 1234567890123456",
            "expected": "SENSITIVE"
        },
        {
            "name": "Credit Card Prompt",
            "prompt": "I lost my credit card yesterday",
            "expected": "SENSITIVE"
        },
        {
            "name": "Multiple Sensitive",
            "prompt": "Send my email and phone number via password protected file",
            "expected": "SENSITIVE"
        },
        {
            "name": "Case Insensitive",
            "prompt": "What is my PASSWORD?",
            "expected": "SENSITIVE"
        }
    ]
    
    # Test health endpoint
    print("🏥 Testing Health Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check: OK")
        else:
            print("❌ Health check failed")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure server is running at http://localhost:8000")
        return
    
    print()
    
    # Test keywords endpoint
    print("📝 Getting Monitored Keywords")
    try:
        response = requests.get(f"{BASE_URL}/keywords")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Monitoring {data['count']} sensitive keywords")
            print(f"Keywords: {', '.join(data['keywords'][:10])}...")  # Show first 10
        else:
            print("❌ Failed to get keywords")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error getting keywords: {e}")
    
    print()
    
    # Test prompt checking
    print("🔍 Testing Prompt Checking")
    print("-" * 30)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print(f"   Prompt: \"{test_case['prompt']}\"")
        
        try:
            # Send request to API
            response = requests.post(
                f"{BASE_URL}/check",
                json={"prompt": test_case["prompt"]},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                status = data["status"]
                
                # Check if result matches expected
                if status == test_case["expected"]:
                    print(f"   ✅ Status: {status}")
                else:
                    print(f"   ❌ Status: {status} (expected {test_case['expected']})")
                
                # Show matches if sensitive
                if status == "SENSITIVE" and data.get("matches"):
                    matches = data["matches"]
                    print(f"   🚨 Found {len(matches)} sensitive keyword(s):")
                    for match in matches:
                        print(f"      - '{match['keyword']}' at position {match['position']}")
                
                # Show LLM response if safe
                elif status == "SAFE" and data.get("response"):
                    response_text = data["response"][:50] + "..." if len(data["response"]) > 50 else data["response"]
                    print(f"   💬 LLM Response: {response_text}")
                    
            else:
                print(f"   ❌ API Error: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Request failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Testing Complete!")

if __name__ == "__main__":
    test_api()