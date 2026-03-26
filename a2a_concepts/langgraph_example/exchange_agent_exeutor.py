from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message, new_task
from a2a.server.tasks import TaskUpdater
from a2a.types import Part, TaskState, TextPart, UnsupportedOperationError
from langgraph_agent import CurrencyAgent
from a2a.utils.errors import ServerError


class CurrencyAgentExecutor(AgentExecutor):
    """
    An executor that runs the CurrencyAgent.
    """

    def __init__(self):
        self.agent = CurrencyAgent()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        query = context.get_user_input()
        task = context.current_task
        if not task:
            task = new_task(context.message)
            await event_queue.enqueue_event(task)
        task_updater = TaskUpdater(event_queue, task.id, task.context_id)
        try:
            async for item in self.agent.stream(query, context_id=task.context_id):
                is_task_completed = item.get("is_task_completed")
                required_user_input = item.get("required_user_input")

                if not is_task_completed and not required_user_input:
                    await task_updater.update_status(
                        TaskState.working,
                        new_agent_text_message(
                            item["content"], task.context_id, task.id
                        ),
                    )
                elif required_user_input:
                    await task_updater.update_status(
                        TaskState.input_required,
                        new_agent_text_message(
                            item["content"], task.context_id, task.id
                        ),
                        final=True,
                    )
                else:
                    await task_updater.add_artifact(
                        [Part(root=TextPart(text=item["content"]))],
                        name="CurrencyAgent Result",
                    )
                    await task_updater.complete()
                    break
        except Exception as e:
            await task_updater.update_status(TaskState.failed)
            raise ServerError(
                f"An error occurred while executing the CurrencyAgent: {str(e)}"
            ) from e

    async def cancel(
        self, request_context: RequestContext, event_queue: EventQueue
    ) -> None:
        raise UnsupportedOperationError("CurrencyAgent does not support cancellation.")
