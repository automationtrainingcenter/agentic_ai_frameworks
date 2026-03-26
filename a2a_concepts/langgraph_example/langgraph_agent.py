from collections.abc import AsyncIterable
import os
from typing import Literal, Any

from pydantic import BaseModel, Field
from langchain.messages import AIMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv

from tools import get_exchange_rate

load_dotenv(override=True)  # Load environment variables from .env file


memore = MemorySaver()


class ResponseFormat(BaseModel):
    """Response to the user in this format"""

    status: Literal["input_required", "completed", "error"] = Field(
        default="input_required"
    )
    message: str


class CurrencyAgent:
    """
    An agent that provides currency exchange rates.
    """

    SYSTEM_INSTRUCTION = (
        "You are a specialized assistant for currency conversions. "
        "Your sole purpose is to use the 'get_exchange_rate' tool to answer questions about currency exchange rates. "
        "If the user asks about anything other than currency conversion or exchange rates, "
        "politely state that you cannot help with that topic and can only assist with currency-related queries. "
        "Do not attempt to answer unrelated questions or use tools for other purposes. "
        "You must not assume the currencies. Instead ask user for clarification. "
        "Remember: You must invoke the tool to convert the currency!"
    )

    FORMAT_INSTRUCTION = (
        "Set response status to input_required if the user needs to provide more information to complete the request."
        "Set response status to error if there is an error while processing the request."
        "Set response status to completed if the request is complete."
    )

    def __init__(self):
        self.model = ChatOpenAI(
            model=os.getenv("OPENROUTER_MODEL"),
            base_url=os.getenv("OPENROUTER_URL"),
            api_key=os.getenv("OPENROUTER_API_KEY"),
            temperature=0.7,
        )

        self.tools = [get_exchange_rate]
        self.graph = create_agent(
            self.model,
            tools=self.tools,
            checkpointer=memore,
            system_prompt=self.SYSTEM_INSTRUCTION,
            response_format=ResponseFormat,
        )

    def get_agent_response(self, config) -> dict[str, Any]:
        try:
            current_state = self.graph.get_state(config)
            print(
                f"Current state values: {current_state.values.get('structured_response')}"
            )
            structured_response = current_state.values.get("structured_response")
            if structured_response and isinstance(structured_response, ResponseFormat):
                if structured_response.status == "completed":
                    return {
                        "is_task_complete": True,
                        "required_user_input": False,
                        "content": structured_response.message,
                    }
                if structured_response.status == "input_required":
                    return {
                        "is_task_complete": False,
                        "required_user_input": True,
                        "content": structured_response.message,
                    }
                if structured_response.status == "error":
                    return {
                        "is_task_complete": False,
                        "required_user_input": False,
                        "content": structured_response.message,
                    }
            return {
                "is_task_complete": False,
                "required_user_input": False,
                "content": "Unable to process the request at this time. Please try again later.",
            }
        except Exception as e:
            return {
                "is_task_complete": False,
                "required_user_input": True,
                "content": f"We are unable to process your request at this time. Error processing the request: {str(e)}",
            }

    async def stream(self, query, context_id) -> AsyncIterable[dict[str, Any]]:
        inputs = {"messages": [{"role": "user", "content": query}]}
        config: RunnableConfig = {"configurable": {"thread_id": context_id}}
        async for item in self.graph.astream(
            inputs, config=config, stream_mode="values"
        ):
            if "messages" not in item or not item["messages"]:
                continue
            message = item["messages"][-1]
            if (
                isinstance(message, AIMessage)
                and message.tool_calls
                and len(message.tool_calls) > 0
            ):
                yield {
                    "is_task_complete": False,
                    "required_user_input": False,
                    "content": "Looking up exchange rates... Please wait while I fetch the latest exchange rates for you.",
                }
            elif isinstance(message, ToolMessage):
                yield {
                    "is_task_complete": False,
                    "required_user_input": False,
                    "content": "Processing the exchange rate information... Please wait while I process the exchange rate information.",
                }
            yield self.get_agent_response(config)

    SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]


# def test():
#     r = model = ChatOpenAI(
#         model=os.getenv("OPENROUTER_MODEL"),
#         base_url=os.getenv("OPENROUTER_URL"),
#         api_key=os.getenv("OPENROUTER_API_KEY"),
#         temperature=0.7,
#     ).invoke("hello")

#     print(r)


# test()
