from fastmcp import FastMCP
from fastmcp.tools import tool


class Calculator:

    def __init__(self):
        pass

    @tool()
    def add(self, a: int, b: int) -> int:
        """Add two numbers."""
        return a + b

    @tool()
    def multiply(self, a: int, b: int) -> int:
        """Multiply two numbers."""
        return a * b


class Product:

    def __init__(self):
        products = {
            1: {"name": "Product 1", "price": 9.99},
            2: {"name": "Product 2", "price": 19.99},
            3: {"name": "Product 3", "price": 29.99},
        }
        self.products = products

    @tool()
    def get_product_info(self, product_id: int) -> dict:
        """Get product information by ID."""
        # In a real application, this would query a database
        return {
            "id": product_id,
            "name": self.products[product_id]["name"],
            "price": self.products[product_id]["price"],
        }

    @tool()
    def update_price(self, product_id: int, new_price: float) -> dict:
        """Update the price of a product."""
        self.products[product_id]["price"] = new_price
        return {
            "id": product_id,
            "name": self.products[product_id]["name"],
            "price": self.products[product_id]["price"],
        }

    @tool()
    def apply_discount(self, product_id: int, discount_percentage: float) -> dict:
        """Apply a discount to the product price."""
        original_price = self.products[product_id]["price"]
        discounted_price = original_price * (1 - discount_percentage / 100)
        self.products[product_id]["price"] = discounted_price
        return {
            "id": product_id,
            "name": self.products[product_id]["name"],
            "original_price": original_price,
            "discounted_price": discounted_price,
        }


calc = Calculator()
prod = Product()
mcp = FastMCP(
    "Class-Level Tools MCP Server",
    tools=[
        prod.get_product_info,
        prod.update_price,
        prod.apply_discount,
    ],
)

if __name__ == "__main__":
    mcp.run(transport="http", port=8181)
