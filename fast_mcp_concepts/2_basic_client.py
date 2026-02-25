from fastmcp import Client
import asyncio

client = Client("http://localhost:8181/mcp")


async def greeter():
    async with client:
        greeting = await client.call_tool("greet", {"name": "Alice"})
        print(greeting)


async def calculator():
    async with client:
        # get all tools
        tools = await client.list_tools()
        print("Available tools:")
        for tool in tools:
            print(f"- {tool.name}: {tool.description} (Parameters: {tool.inputSchema['properties']})")

        sum_result = await client.call_tool("add", {"a": 5, "b": 3})
        product_result = await client.call_tool("multiply", {"a": 5, "b": 3})
        print(f"Sum: {sum_result}, Product: {product_result}")


async def product_info():
    async with client:
        tools = await client.list_tools()
        print("Product Info:")
        for tool in tools:
            print(f"- {tool.name}: {tool.description} (Parameters: {tool.inputSchema['properties']})")
        
        # get product info for product_id 1
        product_info = await client.call_tool("get_product_info", {"product_id": 1})
        print(f"Product Info: {product_info.structured_content}")

        # update price for product_id 1
        updated_product = await client.call_tool("update_price", {"product_id": 1, "new_price": 10})
        print(f"Updated Product: {updated_product.structured_content}")

        # apply discount for product_id 1
        discounted_product = await client.call_tool("apply_discount", {"product_id": 1, "discount_percentage": 25})
        print(f"Discounted Product: {discounted_product.structured_content}")

        # get updated product info for product_id 1
        updated_product_info = await client.call_tool("get_product_info", {"product_id": 1})
        print(f"Updated Product Info: {updated_product_info.structured_content}")



asyncio.run(product_info())
