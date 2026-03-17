import asyncio
from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.session import ClientSession


async def main():

    server_params = StdioServerParameters(
        command="python",
        args=["math_mcp_server.py"]
    )

    async with stdio_client(server_params) as (read_stream, write_stream):

        async with ClientSession(read_stream, write_stream) as session:

            # IMPORTANT STEP
            await session.initialize()

            tools = await session.list_tools()
            print("Available tools:", tools)

            for t in tools.tools:
                print("-", t.name)

            result = await session.call_tool("multiply", {"a": 10, "b": 15})
            print("Result:", result.structuredContent["result"])


asyncio.run(main())