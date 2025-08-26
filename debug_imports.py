"""
Simplified test to check what's preventing the import
"""

print("Testing individual imports...")

try:
    import os
    print("✅ os imported")
except Exception as e:
    print(f"❌ os failed: {e}")

try:
    import json
    print("✅ json imported")
except Exception as e:
    print(f"❌ json failed: {e}")

try:
    import time
    print("✅ time imported")
except Exception as e:
    print(f"❌ time failed: {e}")

try:
    from abc import ABC, abstractmethod
    print("✅ abc imported")
except Exception as e:
    print(f"❌ abc failed: {e}")

try:
    from dotenv import load_dotenv
    print("✅ dotenv imported")
except Exception as e:
    print(f"❌ dotenv failed: {e}")

try:
    import google.generativeai as genai
    print("✅ google.generativeai imported")
except Exception as e:
    print(f"❌ google.generativeai failed: {e}")

try:
    import tiktoken
    print("✅ tiktoken imported")
except Exception as e:
    print(f"❌ tiktoken failed: {e}")

try:
    import parlant.sdk as p
    print("✅ parlant.sdk imported")
except Exception as e:
    print(f"❌ parlant.sdk failed: {e}")

try:
    import numpy as np
    print("✅ numpy imported")
except Exception as e:
    print(f"❌ numpy failed: {e}")

print("\nTesting environment variables...")
from dotenv import load_dotenv
load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    print(f"✅ GEMINI_API_KEY found: {api_key[:10]}...")
else:
    print("❌ GEMINI_API_KEY not found")

model = os.environ.get("GEMINI_MODEL")
if model:
    print(f"✅ GEMINI_MODEL found: {model}")
else:
    print("❌ GEMINI_MODEL not found")
