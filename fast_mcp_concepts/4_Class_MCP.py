from fastmcp import FastMCP, Context
from pydantic import Field
from typing import Annotated, Any

class MyMCP(FastMCP):

    def __init__(self, 
                 name: str = "My MCP Server", 
                 instructions: str| None = None,
                 **settings: Any
    ):
        
        super().__init__(name=name, instructions=instructions, **settings)
        self.setup_tools()

    def setup_tools(self):

        async def greet(ctx: Context,
            message: Annotated[str, Field(description="message to display")],
            # The `metadata` parameter is defined as non-optional, but it can be None.
            # If we set it to be optional, some of the MCP clients, like Cursor, cannot
            # handle the optional parameter correctly.
            metadata: Annotated[
                dict | None,
                Field(
                    description="Extra metadata stored along with memorised information. Any json is accepted."
                ),
            ] = None,
        ) -> str:
            """
            Store some information in Qdrant.
            :param ctx: The context for the request.
            :param message: The message to store.
            :param metadata: JSON metadata to store with the information, optional.
            :return: A message indicating that the information was stored.
            """
            await ctx.debug(f"Displaying Message {message}")
            return f"Remembered: {message}"
        
        greet_foo = greet

        self.tool(
            greet_foo,
            name="server_message",
            description="Send a message to server to display in debug logs.",
        )

server = MyMCP()
if __name__ == "__main__":
    server.run(transport="stdio")
