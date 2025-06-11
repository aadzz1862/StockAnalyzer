from mcp.server.fastmcp import FastMCP

# Define a simple decorator to simulate `@tool`
def tool(func):
    func._is_tool = True
    return func
