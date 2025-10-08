# SecurePrompt Testing Examples

## 1. GENERATE Feature Examples

### Example 1: Student Registration Form
```
Prompt: "Generate a student registration form template with fields like NIM: 12345678, NIK: 3202011234567890, Phone: 081234567890"

Expected Sanitized: "Generate a student registration form template with fields like student ID, ID, phone"

Expected Response: Creates Indonesian university registration form template
```

### Example 2: Student Profile Template  
```
Prompt: "Create student profile example with NIM: 202312345, NIK: 3201012345678901, Email: student@univ.ac.id"

Expected Sanitized: "Create student profile example with student ID, ID, Email: email"

Expected Response: Generates comprehensive student profile structure
```

## 2. SUMMARIZE Feature Examples

### Example 1: Student Data Summary
```
Prompt: "Summarize this student information: Nama: Ahmad Rizki, NIM: 12345678, NIK: 3202011234567890, Email: ahmad@student.univ.ac.id, Phone: 081234567890, Program: Teknik Informatika"

Expected Sanitized: "Summarize this student information: Nama: Ahmad Rizki, student ID, ID, Email: email, phone, Program: Teknik Informatika"

Expected Response: Structured summary focusing on academic program and general profile
```

### Example 2: Multiple Students Summary
```
Prompt: "Summarize these student records:
1. Budi - NIM: 20220001, NIK: 3201012345678901, Phone: 081987654321
2. Sari - NIM: 20220002, NIK: 3201012345678902, Phone: 081987654322"

Expected Sanitized: "Summarize these student records:
1. Budi - student ID, ID, phone
2. Sari - student ID, ID, phone"

Expected Response: Summary of student data structure and components
```

## 3. EXPLAIN Feature Examples

### Example 1: Data Structure Explanation
```
Prompt: "Explain the structure of this Indonesian student data: Name: Budi Santoso, NIM: 20220001, NIK: 3201012345678901, Phone: 081987654321, Email: budi@university.ac.id"

Expected Sanitized: "Explain the structure of this Indonesian student data: Name: Budi Santoso, student ID, ID, phone, Email: email"

Expected Response: Educational explanation about Indonesian student data components
```

### Example 2: ID Number System Explanation
```
Prompt: "Explain Indonesian student identification system using example: NIM: 202312345678, NIK: 3202011234567890"

Expected Sanitized: "Explain Indonesian student identification system using example: student ID, ID"

Expected Response: General explanation of Indonesian education ID systems
```

## 4. Complex Mixed Examples

### Example 1: Academic Report
```
Prompt: "Create academic report for student with NIM: 12345678, NIK: 3202011234567890, containing grades and contact info Phone: 081234567890"

Expected Sanitized: "Create academic report for student with student ID, ID, containing grades and contact info phone"

Expected Response: Academic report template without sensitive data
```

### Example 2: Research Data Analysis
```
Prompt: "Analyze this research dataset:
Student A: NIM 20220001, NIK 3201012345678901, GPA 3.85
Student B: NIM 20220002, NIK 3201012345678902, GPA 3.92
Explain patterns and summarize findings."

Expected Sanitized: "Analyze this research dataset:
Student A: student ID, ID, GPA 3.85
Student B: student ID, ID, GPA 3.92
Explain patterns and summarize findings."

Expected Response: Academic analysis focusing on GPA patterns and trends
```

## 5. Edge Cases

### Example 1: Mixed Languages
```
Prompt: "Buat ringkasan mahasiswa: Nama: Dewi, NIM: 12345678, NIK: 3202011234567890, Telepon: 081234567890"

Expected Sanitized: "Buat ringkasan mahasiswa: Nama: Dewi, student ID, ID, phone"

Expected Response: Indonesian language summary with protected sensitive data
```

### Example 2: Multiple Sensitive Patterns
```
Prompt: "Process enrollment data: NIK: 3202011234567890, NIM: 12345678, NISN: 1234567890, Phone: +6281234567890, Email: student@univ.ac.id"

Expected Sanitized: "Process enrollment data: ID, student ID, student number, phone, Email: email"

Expected Response: Enrollment process explanation without sensitive details
```

## Testing Commands

### Quick Test - Generate
```bash
python -c "
import urllib.request, json
data = json.dumps({
    'model': 'llama3.2:latest', 
    'messages': [{'role': 'user', 'content': 'Generate student form with NIM: 12345678, NIK: 3202011234567890'}]
}).encode()
req = urllib.request.Request('http://127.0.0.1:8001/api/v1/chat/completions', data=data, headers={'Content-Type': 'application/json'})
response = urllib.request.urlopen(req)
result = json.loads(response.read().decode())
print('GENERATE TEST:', result['choices'][0]['message']['content'][:300])
"
```

### Quick Test - Summarize  
```bash
python -c "
import urllib.request, json
data = json.dumps({
    'model': 'llama3.2:latest',
    'messages': [{'role': 'user', 'content': 'Summarize: Nama: Ahmad, NIM: 12345678, NIK: 3202011234567890, Phone: 081234567890'}]
}).encode()
req = urllib.request.Request('http://127.0.0.1:8001/api/v1/chat/completions', data=data, headers={'Content-Type': 'application/json'})
response = urllib.request.urlopen(req)
result = json.loads(response.read().decode())
print('SUMMARIZE TEST:', result['choices'][0]['message']['content'][:300])
"
```

### Quick Test - Explain
```bash
python -c "
import urllib.request, json
data = json.dumps({
    'model': 'llama3.2:latest',
    'messages': [{'role': 'user', 'content': 'Explain data structure: NIM: 20220001, NIK: 3201012345678901, Phone: 081987654321'}]
}).encode()
req = urllib.request.Request('http://127.0.0.1:8001/api/v1/chat/completions', data=data, headers={'Content-Type': 'application/json'})
response = urllib.request.urlopen(req)
result = json.loads(response.read().decode())
print('EXPLAIN TEST:', result['choices'][0]['message']['content'][:300])
"
```

## Validation Checklist

### ✅ For Each Test:
1. **Detection**: Sensitive data terdeteksi ✅
2. **Sanitization**: Data di-replace dengan generic terms ✅  
3. **Functionality**: AI response tetap berguna dan informatif ✅
4. **Security**: Tidak ada sensitive data di output ✅
5. **Moodle Compatibility**: OpenAI format compliance ✅

### 🎯 Success Criteria:
- Generate: Creates useful templates/examples
- Summarize: Provides structured information overview  
- Explain: Gives educational explanations about data structure
- All: Zero sensitive data exposure in any response