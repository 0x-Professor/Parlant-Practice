import parlant.sdk as p
import asyncio

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
    async with p.Server() as server:
        agent = await server.create_agent(
            name="Healthcare Agent",
            description="Is empathetic and calming to the patient.",
        )

        await add_domain_glossary(agent)

if __name__ == "__main__":
    asyncio.run(main())