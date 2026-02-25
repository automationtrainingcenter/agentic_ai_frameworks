from fastmcp import FastMCP

app = FastMCP("First MCP Server")


@app.tool
def greet(name: str) -> str:
    """Greet a person by name."""
    return f"Hello, {name}!"


if __name__ == "__main__":
    app.run(transport="http", port=8181)
