import parlant.sdk as p
import asyncio
import os
from gemini_service import load_gemini_nlp_service

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

async def create_sample_conversation(agent: p.Agent) -> None:
    """Create a sample conversation to demonstrate the agent."""
    print("💬 Creating sample conversation...")
    
    try:
        # Create a new conversation session
        session = await agent.create_conversation(
            customer_id="demo-customer-001"
        )
        
        # Send a message from the customer
        await session.send_customer_message("Hello, I need help with scheduling an appointment.")
        
        print(f"✅ Sample conversation created with ID: {session.id}")
        print("   Customer message: 'Hello, I need help with scheduling an appointment.'")
        
        # Get agent response
        messages = await session.get_messages()
        if len(messages) > 1:
            print(f"   Agent response: {messages[-1].content}")
        
    except Exception as e:
        print(f"⚠️  Could not create conversation: {e}")

async def main() -> None:
    """Main application entry point."""
    print("🚀 Parlant Healthcare Agent with Gemini AI")
    print("=" * 50)
    
    # Check if GEMINI_API_KEY is set
    if not os.environ.get("GEMINI_API_KEY"):
        print("❌ Error: GEMINI_API_KEY environment variable is required")
        print("\n📋 To set up your environment:")
        print("1. Run: python setup_env.py")
        print("2. Or visit: https://makersuite.google.com/app/apikey")
        print("3. Set your API key: $env:GEMINI_API_KEY = 'your-key-here'")
        return
    
    gemini_model = os.environ.get("GEMINI_MODEL", "gemini-1.5-flash")
    print(f"🤖 Using Gemini model: {gemini_model}")
    print(f"🔑 API Key configured: {os.environ['GEMINI_API_KEY'][:10]}...")
    
    try:
        # Create server with custom Gemini NLP service
        print("\n🔄 Starting Parlant server with Gemini NLP service...")
        
        async with p.Server(nlp_service=load_gemini_nlp_service) as server:
            print("✅ Server started successfully!")
            
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
            
            # Create a sample conversation
            await create_sample_conversation(agent)
            
            print(f"\n🎉 Setup completed successfully!")
            print(f"\n📖 Your healthcare agent is now ready to use with Gemini AI!")
            print(f"   - Agent uses Gemini {gemini_model} for natural language processing")
            print(f"   - Embeddings powered by Google's text-embedding-004")
            print(f"   - Content moderation via Gemini safety filters")
            
            print(f"\n🔧 Next steps:")
            print(f"   1. Test the integration: python test_gemini.py")
            print(f"   2. Build your own conversation flows")
            print(f"   3. Customize the agent's knowledge and behavior")
            
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
            print("   1. Run: python test_gemini.py")
            print("   2. Check the parlant-data/parlant.log file")
            print("   3. Verify your internet connection")

if __name__ == "__main__":
    asyncio.run(main())