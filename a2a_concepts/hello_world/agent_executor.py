from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message

class HelloWorldAgent:
    """
    A simple agent that returns a greeting message.
    """

    async def invoke(self) -> str:
        return f"Hello, World!"
    

class HelloWorldAgentExecutor(AgentExecutor):
    """
    An executor that runs the HelloWorldAgent.
    """

    def __init__(self):
        self.agent = HelloWorldAgent()

    async def execute(self, request_context: RequestContext, event_queue: EventQueue) -> None:
        result = await self.agent.invoke()
        await event_queue.enqueue_event(new_agent_text_message(result))
    
    async def cancel(self, request_context: RequestContext, event_queue: EventQueue) -> None:
        raise Exception("HelloWorldAgent does not support cancellation.")