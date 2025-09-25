"""
Simple test script untuk SecurePrompt API
"""
import json
from app.core.checker import prompt_checker

def test_prompt_checker():
    """Test langsung ke prompt checker tanpa API"""
    
    print("🔐 SecurePrompt Direct Testing")
    print("=" * 40)
    
    # Test cases
    test_prompts = [
        "What is the weather today?",  # SAFE
        "What is my password?",        # SENSITIVE  
        "Send to my email",            # SENSITIVE
        "My NIK is 123456789",         # SENSITIVE
        "How to cook pasta?",          # SAFE
        "My credit card number",       # SENSITIVE
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n{i}. Testing: \"{prompt}\"")
        
        result = prompt_checker.check_prompt(prompt)
        status = result["status"]
        
        if status == "SAFE":
            print(f"   ✅ {status}")
            print(f"   Response: {result.get('response', 'No response')}")
        else:
            print(f"   🚨 {status}")
            matches = result.get('matches', [])
            for match in matches:
                print(f"   - Found '{match['keyword']}' at position {match['position']}")
    
    print(f"\n{'='*40}")
    print("✅ All tests completed!")

if __name__ == "__main__":
    test_prompt_checker()