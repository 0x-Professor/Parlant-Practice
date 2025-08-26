"""
Environment setup script for Gemini integration
"""
import os

def setup_environment():
    """Interactive script to set up environment variables for Gemini API."""
    
    print("🚀 Parlant + Gemini Setup")
    print("=" * 40)
    
    # Check if API key is already set
    current_key = os.environ.get("GEMINI_API_KEY")
    if current_key:
        print(f"✅ GEMINI_API_KEY is already set: {current_key[:10]}...")
        return True
    
    print("\n🔑 Gemini API Key Setup")
    print("To get your API key:")
    print("1. Visit https://makersuite.google.com/app/apikey")
    print("2. Sign in with your Google account")
    print("3. Click 'Create API Key'")
    print("4. Copy the generated key\n")
    
    api_key = input("Enter your Gemini API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided. Exiting.")
        return False
    
    # Set environment variable for current session
    os.environ["GEMINI_API_KEY"] = api_key
    
    # Optional model selection
    print("\n🤖 Model Selection")
    print("Available models:")
    print("1. gemini-1.5-flash (fast, cost-effective)")
    print("2. gemini-1.5-pro (more capable, higher cost)")
    print("3. gemini-pro (older generation)")
    
    model_choice = input("\nSelect model (1-3) or press Enter for default (1): ").strip()
    
    model_map = {
        "1": "gemini-1.5-flash",
        "2": "gemini-1.5-pro", 
        "3": "gemini-pro",
        "": "gemini-1.5-flash"
    }
    
    selected_model = model_map.get(model_choice, "gemini-1.5-flash")
    os.environ["GEMINI_MODEL"] = selected_model
    
    print(f"\n✅ Environment configured!")
    print(f"   API Key: {api_key[:10]}...")
    print(f"   Model: {selected_model}")
    
    print(f"\n💡 To make this permanent, add to your PowerShell profile or .env file:")
    print(f'   $env:GEMINI_API_KEY = "{api_key}"')
    print(f'   $env:GEMINI_MODEL = "{selected_model}"')
    
    return True

if __name__ == "__main__":
    if setup_environment():
        print(f"\n🎉 Ready to run: python main.py")
    else:
        print(f"\n❌ Setup failed. Please try again.")
