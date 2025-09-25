"""
Manual implementation of Aho-Corasick algorithm for pattern matching.
"""
from typing import List, Dict, Set, Tuple
from collections import deque


class TrieNode:
    """Node in the trie structure for Aho-Corasick algorithm."""
    
    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        self.failure_link: 'TrieNode' = None
        self.output: Set[str] = set()  # Patterns that end at this node
        self.is_end_of_word: bool = False


class AhoCorasick:
    """Aho-Corasick string matching algorithm implementation."""
    
    def __init__(self, patterns: List[str]):
        """
        Initialize the Aho-Corasick automaton with a list of patterns.
        
        Args:
            patterns: List of strings to search for
        """
        self.root = TrieNode()
        self.patterns = [pattern.lower() for pattern in patterns]  # Case insensitive
        self._build_trie()
        self._build_failure_links()
    
    def _build_trie(self):
        """Build the trie structure from patterns."""
        for pattern in self.patterns:
            current = self.root
            for char in pattern:
                if char not in current.children:
                    current.children[char] = TrieNode()
                current = current.children[char]
            current.is_end_of_word = True
            current.output.add(pattern)
    
    def _build_failure_links(self):
        """Build failure links using BFS."""
        # Initialize failure links for depth 1 nodes
        queue = deque()
        for child in self.root.children.values():
            child.failure_link = self.root
            queue.append(child)
        
        # Build failure links for deeper nodes
        while queue:
            current = queue.popleft()
            
            for char, child in current.children.items():
                queue.append(child)
                
                # Find the failure link for this child
                failure = current.failure_link
                while failure != self.root and char not in failure.children:
                    failure = failure.failure_link
                
                if char in failure.children and failure.children[char] != child:
                    child.failure_link = failure.children[char]
                else:
                    child.failure_link = self.root
                
                # Copy output from failure link
                child.output.update(child.failure_link.output)
    
    def search(self, text: str) -> List[Tuple[str, int]]:
        """
        Search for all pattern occurrences in the text.
        
        Args:
            text: Text to search in
            
        Returns:
            List of tuples (pattern, position) for all matches
        """
        matches = []
        text = text.lower()  # Case insensitive search
        current = self.root
        
        for i, char in enumerate(text):
            # Follow failure links until we find a valid transition or reach root
            while current != self.root and char not in current.children:
                current = current.failure_link
            
            # Move to next state if possible
            if char in current.children:
                current = current.children[char]
            
            # Check for pattern matches at current position
            for pattern in current.output:
                start_pos = i - len(pattern) + 1
                matches.append((pattern, start_pos))
        
        return matches
    
    def has_matches(self, text: str) -> bool:
        """
        Quick check if text contains any patterns.
        
        Args:
            text: Text to check
            
        Returns:
            True if any pattern is found, False otherwise
        """
        text = text.lower()
        current = self.root
        
        for char in text:
            while current != self.root and char not in current.children:
                current = current.failure_link
            
            if char in current.children:
                current = current.children[char]
            
            if current.output:
                return True
        
        return False