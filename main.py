import parlant.sdk as p
import asyncio
import os
from gemini_service import load_gemini_nlp_service

async def add_domain_glossary(agent: p.Agent) -> None:
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

async def main() -> None:
    # Check if GEMINI_API_KEY is set
    if not os.environ.get("GEMINI_API_KEY"):
        print("Error: Please set the GEMINI_API_KEY environment variable")
        print("You can get an API key from: https://makersuite.google.com/app/apikey")
        return
    
    # Create server with custom Gemini NLP service
    async with p.Server(nlp_service=load_gemini_nlp_service) as server:
        agent = await server.create_agent(
            name="Healthcare Agent",
            description="Is empathetic and calming to the patient.",
        )

        await add_domain_glossary(agent)
        
        print("Healthcare agent created successfully with Gemini NLP service!")
        print(f"Agent ID: {agent.id}")
        print("You can now interact with your agent using the Parlant client.")

if __name__ == "__main__":
    asyncio.run(main())