# Windows OS is not supporting running the server from notebook files

from agents.mcp import MCPServerStdio


async def fetch_server():
    fetch_params = {"command": "uvx", "args": ["mcp-server-fetch"]}


    async with MCPServerStdio(
        params=fetch_params,
        client_session_timeout_seconds=30,
    ) as mcp_server:
        tools = await mcp_server.list_tools()

    for tool in tools:
        print(tool.name)
        print(tool.description)
        print(tool.model_dump())
        print("-" * 20)

async def basic_server_client():
    fetch_params = {"command": "fastmcp", "args": ["run", "fast_mcp_concepts\\1_basic_server.py"]}  # Use double backslashes for Windows paths
    

    async with MCPServerStdio(
        params=fetch_params,
        client_session_timeout_seconds=30,
    ) as mcp_server:
        tools = await mcp_server.list_tools()

        for tool in tools:
            print(tool.name)
            print(tool.description)
            print("-" * 20)
        print(await mcp_server.call_tool('greet', {"name": "Surya"}))


async def class_server_client():
    fetch_params = {"command": "fastmcp", "args": ["run", "fast_mcp_concepts\\4_Class_MCP.py"]}  # Use double backslashes for Windows paths
    

    async with MCPServerStdio(
        params=fetch_params,
        client_session_timeout_seconds=30,
    ) as mcp_server:
        tools = await mcp_server.list_tools()

        for tool in tools:
            print(tool.name)
            print(tool.description)
            print("-" * 20)
        print(await mcp_server.call_tool('server_message', {"message": "Hello from the client!"}))

async def main():
    await class_server_client()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())