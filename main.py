import parlant.sdk as p

@p.tool
async def get_weather(context: p.ToolContext, city: str) -> p.ToolResult:
    # Your weather API logic here
    return p.ToolResult(f"Sunny, 72°F in {city}")

@p.tool
async def get_datetime(context: p.ToolContext) -> p.ToolResult:
    from datetime import datetime
    return p.ToolResult(datetime.now())

async def main():
    async with p.Server() as server:
        agent = await server.create_agent(
            name="WeatherBot",
            description="Helpful weather assistant"
        )

        # Have the agent's context be updated on every response (though
        # update interval is customizable) using a context variable.
        await agent.create_variable(name="current-datetime", tool=get_datetime)

        # Control and guide agent behavior with natural language
        await agent.create_guideline(
            condition="User asks about weather",
            action="Get current weather and provide a friendly response with suggestions",
            tools=[get_weather]
        )

        # Add other (reliably enforced) behavioral modeling elements
        # ...

        # 🎉 Test playground ready at http://localhost:8800
        # Integrate the official React widget into your app,
        # or follow the tutorial to build your own frontend!

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())