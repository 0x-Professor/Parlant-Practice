"""Test if we can import the gemini service"""
try:
    print("Testing gemini_service import...")
    import gemini_service
    print("✅ gemini_service module imported successfully")
    
    # Test if the function exists
    if hasattr(gemini_service, 'load_gemini_nlp_service'):
        print("✅ load_gemini_nlp_service function found")
    else:
        print("❌ load_gemini_nlp_service function not found")
        print("Available attributes:", dir(gemini_service))
        
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Other error: {e}")
    import traceback
    traceback.print_exc()
