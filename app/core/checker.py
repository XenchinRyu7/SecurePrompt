"""
Prompt checker using Aho-Corasick algorithm for sensitive content detection.
"""
from typing import Dict, List, Any
from .aho_corasick import AhoCorasick


# Default list of sensitive keywords
DEFAULT_SENSITIVE_KEYWORDS = [
    # Indonesian specific
    "NIK",
    "NIM", 
    "NISN",
    "KTP",
    "SIM",
    "NPWP",
    "rekening bank",
    "nomor rekening",
    
    # Contact info
    "email", 
    "phone",
    "telepon",
    "handphone",
    "hp",
    "whatsapp",
    "wa",
    
    # Security related
    "password",
    "pin",
    "cvv",
    "otp",
    "kode verifikasi",
    
    # Financial
    "credit card",
    "kartu kredit", 
    "debit card",
    "bank account",
    "saldo",
    "transfer",
    
    # Identity documents
    "passport",
    "paspor", 
    "driver license",
    "birth certificate",
    "akta lahir",
    "ijazah",
    "transkrip",
    
    # System security
    "api key",
    "token",
    "secret",
    "private key",
    "confidential",
    "classified",
    "rahasia"
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


def check_prompt(prompt: str) -> Dict[str, Any]:
    """
    Function wrapper for checking prompts.
    
    Args:
        prompt: User input prompt to check
        
    Returns:
        Dictionary with status and matches/response
    """
    return prompt_checker.check_prompt(prompt)