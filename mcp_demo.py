import asyncio

from fastmcp import Client


async def main():
    async with Client("mcp_server.py") as client:
        result = await client.call_tool(
            "summarize_summarize_post",
            {"text": "A biologist wakes alone on a spacecraft with no memory of how she got there, and the only clue is a message in her own handwriting."},
        )
        print(result.data)


if __name__ == "__main__":
    asyncio.run(main())