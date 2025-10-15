#!/usr/bin/env python3
"""
Basic tests for AI Terminal Client
Run with: python test_basic.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai_cli_tool import APIKeyDetector

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

if __name__ == '__main__':
    test_api_key_detection()
