import parlant.sdk as p
import asyncio
import os
from dotenv import load_dotenv
from gemini_service import load_gemini_nlp_service

load_dotenv()

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

async def create_sample_conversation(agent: p.Agent) -> None:
    try:
        session = await agent.create_conversation(
            customer_id="demo-customer-001"
        )
        await session.send_customer_message("Hello, I need help with scheduling an appointment.")
    except Exception:
        pass
    
async def main() -> None:
    if not os.environ.get("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable is required")
        return
    
    try:
        async with p.Server(nlp_service=load_gemini_nlp_service) as server:
            agent = await server.create_agent(
                name="Healthcare Agent",
                description="An empathetic and calming healthcare assistant that helps patients with appointments, information, and basic medical questions.",
            )
            
            await add_domain_glossary(agent)
            await create_sample_conversation(agent)
            await asyncio.sleep(5)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())