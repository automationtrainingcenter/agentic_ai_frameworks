from fastmcp import Client, Context
from pydantic import Field
from typing import Annotated, Any
import asyncio



class MyMCPC(Client):
    """
    A client that connects to the MyMCP server.
    Can call server_message tool to display messages in the server's debug logs.
    """

    def __init__(self, server_instance):
        """
        Initialize the MCP client.
        
        Args:
            server_instance: FastMCP server instance
        """
        super().__init__(server_instance)

    async def greet(self, message: Annotated[str, Field(description="message to display")],
                    metadata: dict | None = None) -> str:
        """
        Call the server_message tool to greet the server.
        
        Args:
            message: The message to display in server debug logs
            metadata: Optional JSON metadata to store with the information
        
        Returns:
            A message indicating that the information was stored
        """
        result = await self.call_tool(
            name="server_message",
            arguments={
                "message": message,
                "metadata": metadata
            }
        )
        print(f"\n--- Received from server ---")
        print(result)
        return result

    async def greet_with_metadata(self, message: str, metadata: dict | None = None) -> str:
        """
        Call the server_message tool with metadata.
        
        Args:
            message: The message to display in server debug logs
            metadata: Optional JSON metadata to store with the information
        
        Returns:
            A message indicating that the information was stored
        """
        return await self.greet(message, metadata)

    def run(self):
        """Run the client with an interactive prompt."""
        print("MyMCP Client - Ready!")
        print("\nAvailable commands:")
        print("  greet 'message'              - Send a simple message to server")
        print("  greet 'message' meta 'json'  - Send message with metadata")
        print("  greet_with_metadata 'message' 'json' - Send message with metadata")
        print("  quit                         - Exit client")
        print()

        while True:
            try:
                command = input(">>> ").strip()
                if command.lower() in ["quit", "exit", "q"]:
                    if hasattr(self, 'process'):
                        self.process.terminate()
                    print("Goodbye!")
                    break
                elif command.startswith("greet "):
                    parts = command.split(None, 2)
                    if len(parts) == 2:
                        message = parts[1]
                        result = asyncio.run(self.greet(message))
                        print(result)
                    elif len(parts) == 3:
                        message = parts[1]
                        metadata_str = parts[2]
                        try:
                            metadata = eval(metadata_str) if metadata_str.startswith("{") else None
                            result = asyncio.run(self.greet(message, metadata))
                            print(result)
                        except:
                            print("Error parsing metadata. Sending without metadata.")
                            result = asyncio.run(self.greet(message))
                            print(result)
            except EOFError:
                print("Goodbye!")
                break
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    from fastmcp.client.transports import StdioTransport
    trasport = StdioTransport(
        command="fastmcp",
        args=["run", "fast_mcp_concepts\\4_Class_MCP.py"]
    )
    client = MyMCPC(trasport)
    client.run()
