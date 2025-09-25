---
applyTo: '**'
---
You are an expert AI security engineer.
Your task is to implement a sensitive prompt protection system using the Aho-Corasick algorithm, but you must implement the algorithm from scratch (do not use existing Aho-Corasick libraries).

Requirements

Language: Python

Project structure:

app/
  ├── main.py              # FastAPI entry point
  ├── api.py               # API routes
  ├── core/
  │     ├── aho_corasick.py   # Manual Aho-Corasick implementation
  │     └── checker.py        # check_prompt logic + dummy LLM forward
  └── tests/
        └── test_checker.py   # Example test cases


Algorithm:

Build a trie from a list of sensitive keywords (e.g., ["NIK", "email", "phone", "password", "credit card"]).

Construct failure links for each trie node.

Implement the search function that scans input text character by character.

Return all matches (keyword + position).

check_prompt(prompt: str)

Input: user prompt.

Process: run Aho-Corasick.

Output JSON:

{
  "status": "SAFE" or "SENSITIVE",
  "matches": [ { "keyword": ..., "position": ... } ]
}


If SAFE → forward prompt to dummy LLM (return "LLM response: ..." + prompt).

If SENSITIVE → block and return the matches.

API:

Use FastAPI with endpoint POST /check → input JSON { "prompt": "..." }.

Return the output of check_prompt().

Tests:

Provide several sample prompts (both SAFE and SENSITIVE).

Environment:

Use virtual environment (venv).

Dependencies: fastapi, uvicorn, pytest.

Deliverables

Full source code with the above folder structure.

Example test cases with pytest.

Instructions to run locally:

python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install fastapi uvicorn pytest
uvicorn app.main:app --reload
pytest