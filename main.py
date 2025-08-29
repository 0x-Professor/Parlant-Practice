import parlant.sdk as p
import asyncio
import os
from dotenv import load_dotenv
from gemini_service import load_gemini_nlp_service
from datetime import datetime

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
@p.tool
async def get_upcoming_slots(context: p.ToolContext) -> p.ToolResult:
    """Get upcoming appointment slots."""
    return p.ToolResult(data=["Monday 10 AM", "Tuesday 2 PM", "Wednesday 1 PM"])
@p.tool
async def get_later_slots(context: p.ToolContext) -> p.ToolResult:
    """Get later appointment slots."""
    return p.ToolResult(data=["Thursday 3 PM", "Friday 11 AM"])
@p.tool
async def schedule_appointment(context: p.ToolContext) -> p.ToolResult:
    """Schedule an appointment."""
    return p.ToolResult(data=["Appointment scheduled for Monday 10 AM"])

async def create_scheduling_journey(server: p.Server, agent: p.Agent) -> p.Journey:
    journey = await agent.create_journey(
        title = "Schedule an Appointment",
        description = "Help the patients to schedule an appointment.",
        conditions = ["The patient wants to schedule an appointment"],
    )
# First, determine the reason for the appointment
    t0 = await journey.initial_state.transition_to(chat_state="Determine the reason for the visit")
    t1 = await t0.target.transition_to(tool_state = get_upcoming_slots)
    t2 = await t1.target.transition_to(chat_state= "List available times and ask which ones works for them")
    t3 = await t2.target.transition_to(
    chat_state="Confirm the details with the patient before scheduling",
    condition="The patient picks a time",
  )
    t4 = await t3.target.transition_to(
    tool_state=schedule_appointment,
    condition="The patient confirms the details",
  )
    t5 = await t4.target.transition_to(chat_state="Confirm the appointment has been scheduled")
    await t5.target.transition_to(state=p.END_JOURNEY)

  # Otherwise, if they say none of the times work, ask for later slots
    t6 = await t2.target.transition_to(
    tool_state=get_later_slots,
    condition="None of those times work for the patient",
  )
    t7 = await t6.target.transition_to(chat_state="List later times and ask if any of them works")

  # Transition back to our happy-path if they pick a time
    await t7.target.transition_to(state=t3.target, condition="The patient picks a time")

  # Otherwise, ask them to call the office
    t8 = await t7.target.transition_to(
    chat_state="Ask the patient to call the office to schedule an appointment",
    condition="None of those times work for the patient either",
  )
    await t8.target.transition_to(state=p.END_JOURNEY)
    await journey.create_guideline(
    condition="The patient says their visit is urgent",
    action="Tell them to call the office immediately",
  )

    return journey
    
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
            await create_scheduling_journey(server, agent)



            await asyncio.sleep(5)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())