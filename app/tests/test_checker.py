"""
Test cases for SecurePrompt checker functionality.
"""
import pytest
from app.core.checker import PromptChecker
from app.core.aho_corasick import AhoCorasick


class TestAhoCorasick:
    """Test cases for Aho-Corasick algorithm implementation."""
    
    def test_single_pattern_match(self):
        """Test matching a single pattern."""
        ac = AhoCorasick(["password"])
        matches = ac.search("Enter your password here")
        assert len(matches) == 1
        assert matches[0] == ("password", 11)
    
    def test_multiple_pattern_matches(self):
        """Test matching multiple patterns."""
        ac = AhoCorasick(["email", "phone"])
        matches = ac.search("Send email to my phone")
        assert len(matches) == 2
        # Sort matches by position for consistent testing
        matches.sort(key=lambda x: x[1])
        assert matches[0] == ("email", 5)
        assert matches[1] == ("phone", 17)
    
    def test_overlapping_patterns(self):
        """Test overlapping pattern matches."""
        ac = AhoCorasick(["he", "she", "his", "hers"])
        matches = ac.search("she is his")
        matches.sort(key=lambda x: x[1])  # Sort by position
        assert len(matches) >= 2  # Should find "she" and "his" at minimum
    
    def test_case_insensitive_search(self):
        """Test case insensitive pattern matching."""
        ac = AhoCorasick(["PASSWORD"])
        matches = ac.search("Enter your password here")
        assert len(matches) == 1
        assert matches[0] == ("password", 11)
    
    def test_no_matches(self):
        """Test when no patterns are found."""
        ac = AhoCorasick(["secret"])
        matches = ac.search("This is a normal text")
        assert len(matches) == 0
    
    def test_empty_text(self):
        """Test with empty text."""
        ac = AhoCorasick(["password"])
        matches = ac.search("")
        assert len(matches) == 0
    
    def test_has_matches_method(self):
        """Test the has_matches convenience method."""
        ac = AhoCorasick(["password", "email"])
        assert ac.has_matches("Enter your password") == True
        assert ac.has_matches("This is normal text") == False


class TestPromptChecker:
    """Test cases for PromptChecker class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.checker = PromptChecker(["password", "email", "phone", "nik", "credit card"])
    
    def test_safe_prompt(self):
        """Test a safe prompt."""
        result = self.checker.check_prompt("What is the weather today?")
        assert result["status"] == "SAFE"
        assert result["matches"] == []
        assert "response" in result
        assert result["response"].startswith("LLM response:")
    
    def test_sensitive_prompt_single_match(self):
        """Test a prompt with single sensitive keyword."""
        result = self.checker.check_prompt("What is my password?")
        assert result["status"] == "SENSITIVE"
        assert len(result["matches"]) == 1
        assert result["matches"][0]["keyword"] == "password"
        assert result["matches"][0]["position"] == 11
        assert "response" not in result
    
    def test_sensitive_prompt_multiple_matches(self):
        """Test a prompt with multiple sensitive keywords."""
        result = self.checker.check_prompt("Send my email and phone number")
        assert result["status"] == "SENSITIVE"
        assert len(result["matches"]) == 2
        
        # Check that both keywords are found
        keywords = [match["keyword"] for match in result["matches"]]
        assert "email" in keywords
        assert "phone" in keywords
    
    def test_case_insensitive_detection(self):
        """Test case insensitive detection."""
        result = self.checker.check_prompt("What is my PASSWORD?")
        assert result["status"] == "SENSITIVE"
        assert len(result["matches"]) == 1
        assert result["matches"][0]["keyword"] == "password"
    
    def test_empty_prompt(self):
        """Test empty prompt."""
        result = self.checker.check_prompt("")
        assert result["status"] == "SAFE"
        assert result["matches"] == []
    
    def test_whitespace_only_prompt(self):
        """Test prompt with only whitespace."""
        result = self.checker.check_prompt("   ")
        assert result["status"] == "SAFE"
        assert result["matches"] == []
    
    def test_indonesian_nik_detection(self):
        """Test detection of Indonesian NIK."""
        result = self.checker.check_prompt("My NIK is 1234567890123456")
        assert result["status"] == "SENSITIVE"
        assert len(result["matches"]) == 1
        assert result["matches"][0]["keyword"] == "nik"
    
    def test_credit_card_detection(self):
        """Test detection of credit card keyword."""
        result = self.checker.check_prompt("I lost my credit card")
        assert result["status"] == "SENSITIVE"
        assert len(result["matches"]) == 1
        assert result["matches"][0]["keyword"] == "credit card"


class TestIntegration:
    """Integration tests combining multiple components."""
    
    def test_full_workflow_safe(self):
        """Test complete workflow with safe prompt."""
        checker = PromptChecker()
        prompt = "How do I cook pasta?"
        result = checker.check_prompt(prompt)
        
        assert result["status"] == "SAFE"
        assert result["matches"] == []
        assert result["response"] == f"LLM response: {prompt}"
    
    def test_full_workflow_sensitive(self):
        """Test complete workflow with sensitive prompt."""
        checker = PromptChecker()
        prompt = "Please store my password: mysecret123"
        result = checker.check_prompt(prompt)
        
        assert result["status"] == "SENSITIVE"
        assert len(result["matches"]) >= 1
        assert any(match["keyword"] == "password" for match in result["matches"])
        assert "response" not in result
    
    def test_custom_keywords(self):
        """Test with custom sensitive keywords."""
        custom_keywords = ["confidential", "classified", "internal"]
        checker = PromptChecker(custom_keywords)
        
        result = checker.check_prompt("This is confidential information")
        assert result["status"] == "SENSITIVE"
        assert result["matches"][0]["keyword"] == "confidential"
    
    def test_performance_with_long_text(self):
        """Test performance with longer text."""
        checker = PromptChecker()
        long_text = "This is a very long text without sensitive content. " * 100
        result = checker.check_prompt(long_text)
        
        assert result["status"] == "SAFE"
        assert result["matches"] == []


if __name__ == "__main__":
    pytest.main([__file__])