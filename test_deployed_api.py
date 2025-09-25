"""
Test script untuk SecurePrompt API yang sudah di-deploy
Usage: python test_deployed_api.py [URL]
"""
import requests
import sys
import json

def test_deployed_api(base_url):
    """Test deployed SecurePrompt API"""
    
    print(f"🌐 Testing SecurePrompt API at: {base_url}")
    print("=" * 60)
    
    # Remove trailing slash
    base_url = base_url.rstrip('/')
    
    # Test 1: Health Check
    print("\n1. 🏥 Health Check")
    try:
        response = requests.get(f"{base_url}/api/health", timeout=30)
        if response.status_code == 200:
            print(f"   ✅ Status: {response.status_code}")
            print(f"   Response: {response.json()}")
        else:
            print(f"   ❌ Status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 2: Root endpoint
    print("\n2. 🏠 Root Endpoint")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print(f"   ✅ Status: {response.status_code}")
            data = response.json()
            print(f"   Title: {data.get('message', 'N/A')}")
        else:
            print(f"   ⚠️  Status: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  Error: {e}")
    
    # Test 3: Keywords endpoint
    print("\n3. 📝 Keywords Endpoint")
    try:
        response = requests.get(f"{base_url}/api/keywords", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Monitoring {data['count']} keywords")
            print(f"   Keywords: {', '.join(data['keywords'][:5])}...")
        else:
            print(f"   ⚠️  Status: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  Error: {e}")
    
    # Test 4: Safe prompt
    print("\n4. ✅ Safe Prompt Test")
    test_safe_prompt = {
        "prompt": "What is the weather today?"
    }
    try:
        response = requests.post(
            f"{base_url}/api/check",
            json=test_safe_prompt,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {data['status']}")
            if data['status'] == 'SAFE':
                print(f"   💬 LLM Response: {data.get('response', 'No response')[:50]}...")
            else:
                print(f"   ⚠️  Expected SAFE, got {data['status']}")
        else:
            print(f"   ❌ HTTP Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 5: Sensitive prompt
    print("\n5. 🚨 Sensitive Prompt Test")
    test_sensitive_prompt = {
        "prompt": "What is my password?"
    }
    try:
        response = requests.post(
            f"{base_url}/api/check",
            json=test_sensitive_prompt,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {data['status']}")
            if data['status'] == 'SENSITIVE':
                matches = data.get('matches', [])
                print(f"   🔍 Found {len(matches)} sensitive keyword(s):")
                for match in matches:
                    print(f"      - '{match['keyword']}' at position {match['position']}")
            else:
                print(f"   ⚠️  Expected SENSITIVE, got {data['status']}")
        else:
            print(f"   ❌ HTTP Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 6: Multiple sensitive keywords
    print("\n6. 🔥 Multiple Keywords Test")
    test_multiple = {
        "prompt": "Send my email and phone via password protected file"
    }
    try:
        response = requests.post(
            f"{base_url}/api/check",
            json=test_multiple,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            print(f"   Status: {data['status']}")
            if data['status'] == 'SENSITIVE':
                matches = data.get('matches', [])
                print(f"   🔍 Found {len(matches)} sensitive keywords:")
                for match in matches:
                    print(f"      - '{match['keyword']}' at position {match['position']}")
            else:
                print(f"   Unexpected status: {data['status']}")
        else:
            print(f"   ❌ HTTP Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 API Testing Complete!")
    print(f"📖 API Documentation: {base_url}/docs")
    print(f"🔗 Base URL: {base_url}")
    
    return True

if __name__ == "__main__":
    # Default to Vercel URL pattern
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        # Default test URL (update setelah deploy)
        url = "https://secure-prompt.vercel.app"
        print(f"🔄 Using default URL: {url}")
        print("   To test your URL: python test_deployed_api.py https://your-project.vercel.app")
    
    test_deployed_api(url)