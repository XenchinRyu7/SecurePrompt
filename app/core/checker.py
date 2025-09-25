"""
Prompt checker using Aho-Corasick algorithm for sensitive content detection.
"""
from typing import Dict, List, Any
from .aho_corasick import AhoCorasick


# Default list of sensitive keywords
DEFAULT_SENSITIVE_KEYWORDS = [
    "NIK",
    "email", 
    "phone",
    "password",
    "credit card",
    "ssn",
    "social security",
    "bank account",
    "pin",
    "cvv",
    "passport",
    "driver license",
    "api key",
    "token",
    "secret",
    "private key",
    "confidential",
    "classified"
]


class PromptChecker:
    """Checker for sensitive content in prompts using Aho-Corasick algorithm."""
    
    def __init__(self, sensitive_keywords: List[str] = None):
        """
        Initialize the prompt checker.
        
        Args:
            sensitive_keywords: List of sensitive keywords to detect
        """
        if sensitive_keywords is None:
            sensitive_keywords = DEFAULT_SENSITIVE_KEYWORDS
        
        self.aho_corasick = AhoCorasick(sensitive_keywords)
    
    def _dummy_llm_response(self, prompt: str) -> str:
        """
        Dummy LLM response for safe prompts.
        
        Args:
            prompt: The input prompt
            
        Returns:
            Dummy LLM response
        """
        return f"LLM response: {prompt}"
    
    def check_prompt(self, prompt: str) -> Dict[str, Any]:
        """
        Check if prompt contains sensitive content.
        
        Args:
            prompt: User input prompt to check
            
        Returns:
            Dictionary with status and matches/response
        """
        if not prompt or not prompt.strip():
            return {
                "status": "SAFE",
                "matches": [],
                "response": self._dummy_llm_response(prompt)
            }
        
        # Search for sensitive patterns
        matches = self.aho_corasick.search(prompt)
        
        if matches:
            # Convert matches to the required format
            formatted_matches = [
                {
                    "keyword": keyword,
                    "position": position
                }
                for keyword, position in matches
            ]
            
            return {
                "status": "SENSITIVE",
                "matches": formatted_matches
            }
        else:
            return {
                "status": "SAFE",
                "matches": [],
                "response": self._dummy_llm_response(prompt)
            }


# Global instance for use in API
prompt_checker = PromptChecker()