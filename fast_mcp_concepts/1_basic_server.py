from fastmcp import FastMCP
import os

app = FastMCP("First MCP Server")


@app.tool
def greet(name: str) -> str:
    """Greet a person by name."""
    return f"Hello, {name}!"


if __name__ == "__main__":
    transport = os.getenv("MCP_TRANSPORT", "stdio")
    if transport == "http":
        port = int(os.getenv("MCP_PORT", "8181"))
        app.run(transport="http", port=port)
    else:
        app.run(transport="stdio")
