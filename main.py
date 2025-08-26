import parlant.sdk as p
import asyncio
import os
from dotenv import load_dotenv
from gemini_working import load_gemini_nlp_service

# Load environment variables from .env file
load_dotenv()

async def add_domain_glossary(agent: p.Agent) -> None:
    """Add domain-specific terms to the agent's knowledge base."""
    print("📚 Adding domain glossary...")
    
    await agent.create_term(
        name="Office Phone Number",
        description="The phone number of our office, at +1-234-567-8900",
    )

    await agent.create_term(
        name="Office Location",
        description="The location of our office, at 123 Business Rd, Business City, BC 12345",
    )
    
    await agent.create_term(
        name="Business Hours",
        description="Our business hours are Monday to Friday, 9am to 5pm",
    )
    
    await agent.create_term(
        name="Charles Xavier",
        synonyms=["Professor X"],
        description="The renowned doctor who specializes in neurology",
    )
    
    print("✅ Domain glossary added successfully!")

async def main() -> None:
    """Main application entry point."""
    print("🚀 Parlant Healthcare Agent Setup")
    print("=" * 40)
    
    # Check if GEMINI_API_KEY is set
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_api_key:
        print("❌ Error: GEMINI_API_KEY environment variable is required")
        print("\n📋 To set up your environment:")
        print("1. Make sure your .env file contains:")
        print("   GEMINI_API_KEY=your-key-here")
        print("   GEMINI_MODEL=gemini-2.0-flash-exp")
        print("2. Or visit: https://makersuite.google.com/app/apikey")
        return
    
    print(f"🔑 API Key configured: {gemini_api_key[:10]}...")
    
    try:
        # Create server with custom Gemini NLP service
        print("\n🔄 Starting Parlant server with Gemini NLP service...")
        
        async with p.Server(nlp_service=load_gemini_nlp_service) as server:
            print("✅ Server started successfully with Gemini!")
            
            # Create healthcare agent
            print("\n👨‍⚕️ Creating healthcare agent...")
            agent = await server.create_agent(
                name="Healthcare Agent",
                description="An empathetic and calming healthcare assistant that helps patients with appointments, information, and basic medical questions.",
            )
            
            print(f"✅ Healthcare agent created successfully!")
            print(f"   Agent ID: {agent.id}")
            print(f"   Agent Name: {agent.name}")
            
            # Add domain knowledge
            await add_domain_glossary(agent)
            
            print(f"\n🎉 Setup completed successfully!")
            print(f"📖 Your healthcare agent is now using Gemini AI!")
            print(f"   - Text generation: {os.environ.get('GEMINI_MODEL', 'gemini-1.5-flash')}")
            print(f"   - Embeddings: Google text-embedding-004")
            print(f"   - Content moderation: Built-in safety")
            
            print(f"\n🔧 Next steps:")
            print(f"   1. Test conversations with your agent")
            print(f"   2. Customize agent knowledge and behavior")
            print(f"   3. Build conversation flows")
            
            # Keep the server running briefly to show it's working
            print(f"\n⏳ Server running for 5 seconds to demonstrate...")
            await asyncio.sleep(5)
            print("✅ Demo complete!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        if "GEMINI_API_KEY" in str(e):
            print("\n💡 This looks like an API key issue. Please check:")
            print("   1. Your API key is correct")
            print("   2. You have enabled the Gemini API")
            print("   3. Your API key has sufficient quota")
        else:
            print("\n💡 For troubleshooting:")
            print("   1. Check your .env file")
            print("   2. Verify your internet connection")
            print("   3. Check the parlant-data/parlant.log file")

if __name__ == "__main__":
    asyncio.run(main())