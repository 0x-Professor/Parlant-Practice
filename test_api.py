"""
Quick test to verify Gemini API key works
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

def test_gemini_api():
    """Test the Gemini API with your key."""
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment")
        return False
    
    print(f"🔑 Using API Key: {api_key[:10]}...")
    
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Test with the model you mentioned - gemini-2.0-flash
        model_name = "gemini-2.0-flash-exp"  # Using experimental version
        print(f"🤖 Testing model: {model_name}")
        
        model = genai.GenerativeModel(model_name)
        
        # Simple test
        response = model.generate_content("Explain how AI works in a few words")
        
        print("✅ API test successful!")
        print(f"Response: {response.text}")
        
        return True
        
    except Exception as e:
        print(f"❌ API test failed: {e}")
        
        # Try fallback to older model
        try:
            print("🔄 Trying fallback model: gemini-1.5-flash")
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content("Explain how AI works in a few words")
            
            print("✅ Fallback model works!")
            print(f"Response: {response.text}")
            print("💡 Updating .env to use gemini-1.5-flash")
            
            # Update .env file
            with open('.env', 'r') as f:
                content = f.read()
            
            content = content.replace('gemini-2.0-flash-exp', 'gemini-1.5-flash')
            
            with open('.env', 'w') as f:
                f.write(content)
            
            return True
            
        except Exception as e2:
            print(f"❌ Fallback also failed: {e2}")
            return False

if __name__ == "__main__":
    test_gemini_api()
