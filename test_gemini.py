"""
Test script to verify Gemini integration with Parlant
"""
import asyncio
import os
import sys
from gemini_service import GeminiNLPService, GeminiTokenizer
import parlant.sdk as p

async def test_tokenizer():
    """Test the tokenizer functionality."""
    print("Testing Gemini Tokenizer...")
    
    tokenizer = GeminiTokenizer()
    test_text = "Hello, this is a test message for token counting."
    
    token_count = await tokenizer.estimate_token_count(test_text)
    print(f"Text: {test_text}")
    print(f"Estimated tokens: {token_count}")
    print("✅ Tokenizer test passed\n")

async def test_nlp_service():
    """Test the NLP service components."""
    print("Testing Gemini NLP Service...")
    
    # Create a mock logger
    class MockLogger:
        def info(self, msg): print(f"INFO: {msg}")
        def error(self, msg): print(f"ERROR: {msg}")
        def warning(self, msg): print(f"WARNING: {msg}")
    
    # Create a mock container
    class MockContainer:
        def __getitem__(self, key):
            if key == p.Logger:
                return MockLogger()
            return None
    
    try:
        # Test service creation
        service = GeminiNLPService(logger=MockLogger())
        print("✅ NLP Service created successfully")
        
        # Test embedder
        embedder = await service.get_embedder()
        print(f"✅ Embedder created: {embedder.id}")
        print(f"   Max tokens: {embedder.max_tokens}")
        print(f"   Dimensions: {embedder.dimensions}")
        
        # Test moderation service
        moderation = await service.get_moderation_service()
        print("✅ Moderation service created")
        
        # Test a simple moderation check
        test_content = "This is a normal, safe message."
        mod_result = await moderation.check(test_content)
        print(f"   Moderation test - Flagged: {mod_result.flagged}, Tags: {mod_result.tags}")
        
        print("✅ All NLP service tests passed\n")
        
    except Exception as e:
        print(f"❌ NLP service test failed: {e}")
        return False
    
    return True

async def test_simple_generation():
    """Test a simple schema generation."""
    print("Testing Simple Schema Generation...")
    
    try:
        from pydantic import BaseModel
        
        class SimpleResponse(BaseModel):
            message: str
            confidence: float
        
        # Create service
        service = GeminiNLPService(logger=None)
        generator = await service.get_schematic_generator(SimpleResponse)
        
        # Test generation
        prompt = "Generate a friendly greeting message with a confidence score between 0 and 1."
        result = await generator.generate(prompt)
        
        print(f"✅ Generation successful!")
        print(f"   Generated: {result.content}")
        print(f"   Model: {result.info.model}")
        print(f"   Duration: {result.info.duration:.2f}s")
        print(f"   Tokens: {result.info.usage.input_tokens} in, {result.info.usage.output_tokens} out")
        
    except Exception as e:
        print(f"❌ Generation test failed: {e}")
        return False
    
    return True

async def main():
    """Run all tests."""
    print("🧪 Gemini Integration Test Suite")
    print("=" * 50)
    
    # Check API key
    if not os.environ.get("GEMINI_API_KEY"):
        print("❌ GEMINI_API_KEY not found. Please run setup_env.py first.")
        return
    
    print(f"🔑 Using Gemini model: {os.environ.get('GEMINI_MODEL', 'gemini-1.5-flash')}\n")
    
    # Run tests
    tests = [
        test_tokenizer,
        test_nlp_service,
        test_simple_generation
    ]
    
    passed = 0
    for test in tests:
        try:
            result = await test()
            if result is not False:
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
    
    print(f"\n📊 Test Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed! Your Gemini integration is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check your configuration.")

if __name__ == "__main__":
    asyncio.run(main())
