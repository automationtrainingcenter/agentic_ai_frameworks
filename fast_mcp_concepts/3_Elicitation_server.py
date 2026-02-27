import os
from dataclasses import dataclass

from fastmcp import FastMCP, Context

app = FastMCP(name="Elicitation_Server")


@dataclass
class UserInfo:
    name: str
    age: int


@app.tool()
def simple_greet(name: str) -> str:
    """A simple greeting tool."""
    return f"Hello, {name}! Welcome to the Elicitation Server."


# The below tool is a simple example of elicitation.
@app.tool()
async def get_user_preferences(ctx: Context) -> str:
    """Collect user information through interactive prompts."""
    result = await ctx.elicit(
        message="Please provide your name and age.", response_type=UserInfo
    )

    if result.action == "accept":
        user_info: UserInfo = result.data
        return f"Thank you, {user_info.name}! You are {user_info.age} years old."
    elif result.action == "decline":
        return "Sorry to hear that. If you change your mind, feel free to provide your information!"
    else:
        return "I didn't understand your response. Please try again."


# The below tool is a simple example of multi turn elicitation. In a real application, you would likely want to maintain state across turns to have a more meaningful conversation.
@app.tool()
async def plan_meeting(ctx: Context) -> str:
    """Plan a meeting through multi-turn elicitation."""
    # Step 1: Ask for the meeting title
    title_result = await ctx.elicit(
        message="What's the meeting title?", response_type=str
    )

    if title_result.action != "accept":
        return "Meeting planning cancelled."

    meeting_title = title_result.data

    # Step 2: Ask for the meeting date
    date_result = await ctx.elicit(
        message="When would you like to schedule the meeting? (Please provide a date in YYYY-MM-DD format)",
        response_type=str,
    )

    if date_result.action != "accept":
        return "Meeting planning cancelled."

    meeting_date = date_result.data

    # Step 3: Ask for meeting urgent or not
    urgent_result = await ctx.elicit(
        message="Is this meeting urgent? (Please answer 'yes' or 'no')",
        response_type=["yes", "no"],
    )

    if urgent_result.action != "accept":
        return "Meeting planning cancelled."

    meeting_urgent = urgent_result.data == "yes"
    return f"Meeting {meeting_title} scheduled for {meeting_date}. Urgent: {meeting_urgent}."


if __name__ == "__main__":
    transport = os.getenv("MCP_TRANSPORT", "stdio")
    if transport == "http":
        port = int(os.getenv("MCP_PORT", "8181"))
        app.run(transport="http", port=port)
    else:
        app.run(transport="stdio")
