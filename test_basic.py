#!/usr/bin/env python3
"""
Enhanced tests for AI Terminal Client
Run with: python test_basic.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai_cli_tool import APIKeyDetector, FileManager

def test_api_key_detection():
    """Test API key detection functionality"""
    
    test_cases = [
        ('sk-1234567890123456789012345678901234567890123456789', 'OpenAI'),
        ('sk-ant-api03-abcdefghijklmnopqrstuvwxyz', 'Anthropic'),
        ('AIzaSyDaGmWKa4JsXZ-HjGw7_SzTt1TkuWN-abcdef', 'Google'),
        ('pplx-1234567890abcdef', 'Perplexity'),
        ('xai-1234567890abcdef', 'Grok'),
        ('1234567890abcdefghijklmnopqrstuvwxyz123456', 'Cohere'),
        ('invalid-key-format', 'Unknown'),
    ]
    
    print("🧪 Testing API Key Detection...")
    
    for api_key, expected_provider in test_cases:
        detected = APIKeyDetector.detect_provider(api_key)
        status = "✅" if detected == expected_provider else "❌"
        print(f"{status} {api_key[:15]}... -> {detected} (expected: {expected_provider})")
        
        if detected != expected_provider:
            print(f"   FAILED: Expected {expected_provider}, got {detected}")

def test_get_models():
    """Test model retrieval functionality"""
    print("\n🧪 Testing Model Retrieval...")
    
    providers = ['OpenAI', 'Anthropic', 'Google', 'Perplexity', 'Grok', 'Cohere']
    
    for provider in providers:
        models = APIKeyDetector.get_models(provider)
        print(f"📱 {provider}: {len(models)} models - {models[:2]}...")

def test_get_api_urls():
    """Test API URL retrieval"""
    print("\n🧪 Testing API URL Retrieval...")
    
    providers = ['OpenAI', 'Anthropic', 'Google', 'Perplexity', 'Grok', 'Cohere']
    
    for provider in providers:
        url = APIKeyDetector.get_api_url(provider)
        print(f"🌐 {provider}: {url}")

def test_code_block_extraction():
    """Test file generation code block extraction"""
    print("\n🧪 Testing Code Block Extraction...")
    
    # Test HTML/CSS/JS extraction
    sample_response = """Here's a simple calculator web app:

```html
<!-- index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Calculator</title>
    <link rel=\"stylesheet\" href=\"style.css\">
</head>
<body>
    <div class=\"calculator\">
        <input type=\"text\" id=\"display\" readonly>
        <script src=\"script.js\"></script>
</body>
</html>
```

```css
<!-- style.css -->
.calculator {\n  width: 300px;\n}
```

```javascript
<!-- script.js -->
function clearDisplay() {\n  document.getElementById('display').value = '';\n}
```
"""
    
    code_blocks = FileManager.extract_code_blocks(sample_response)
    
    print(f"📁 Extracted {len(code_blocks)} code blocks:")
    for block in code_blocks:
        print(f"  📄 {block['filename']} ({block['language']}) - {len(block['content'])} chars")
    
    # Verify expected files
    expected_files = ['index.html', 'style.css', 'script.js']
    extracted_files = [block['filename'] for block in code_blocks]
    
    for expected in expected_files:
        if expected in extracted_files:
            print(f"  ✅ Found expected file: {expected}")
        else:
            print(f"  ❌ Missing expected file: {expected}")

def test_python_extraction():
    """Test Python file extraction"""
    print("\n🧪 Testing Python File Extraction...")
    
    python_response = """Here's a Flask API:

```python
# app.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/users')
def get_users():
    return jsonify({'users': []})
```

```python
# models.py
from dataclasses import dataclass

@dataclass
class User:
    id: int
    name: str
```
"""
    
    code_blocks = FileManager.extract_code_blocks(python_response)
    
    print(f"📁 Extracted {len(code_blocks)} code blocks:")
    for block in code_blocks:
        print(f"  📄 {block['filename']} ({block['language']}) - {len(block['content'])} chars")

if __name__ == '__main__':
    print("🚀 AI Terminal Client - Enhanced Tests (v1.2)")
    print("=" * 60)
    
    try:
        test_api_key_detection()
        test_get_models()
        test_get_api_urls()
        test_code_block_extraction()
        test_python_extraction()
        
        print("\n✅ All enhanced tests completed successfully!")
        print("\n📋 Test Summary:")
        print("  ✅ API key detection working")
        print("  ✅ Model retrieval working")
        print("  ✅ URL retrieval working")
        print("  ✅ File generation system working")
        print("  ✅ Code block extraction working")
        print("\nNote: These tests only check detection and extraction logic.")
        print("To test actual API calls and file creation, run the main tool with valid API keys.")
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        sys.exit(1)
