import asyncio
import os
import sys
from unittest import result
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.shared.metadata_utils import get_display_name
import json

async def main():
    
    # Spawn the server using the same Python interpreter so the virtualenv is used.
    # Use `-m uv run ...` so the `uv` CLI runs in the current interpreter/venv.
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "tax_server.py"],
)
    
      
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            print ("Client connected to server successfully.")

            while True:
                print("1 - calculate tax")
                print("2 - tax greeting")
                print("3 - tax config")
                print("0 - exit")
                choice = input("Enter your choice: ")

                if choice == "0":
                    print("Exiting...")
                    break
                elif choice == "1":
                    price = float(input("Enter the base amount: "))
                    country = input("Enter the country: ")

                    result = await session.call_tool(
                         "calculate_tax",{"price": price, "country": country})

                    if result.isError:
                         print("Error:", result.content)
                    else:
                         print("Calculated tax amount:", result.content[0].text)
                elif choice == "2":
                    name = input("Enter your name: ")
                    country = input("Enter your country: ")
                    greeting = await session.get_prompt("tax_greeting",{"name": name, "country": country})
                    print(greeting)
                elif choice == "3":
                    result = await session.read_resource("resource://tax_config")

                    tax_info = json.loads(result.contents[0].text)

                    print("Tax configuration:")
                    for country, rate in tax_info.items():
                        print(f"{country}: {rate}%")
                else:
                    print("Invalid choice. Please try again.")

                    



if __name__ == "__main__":
    asyncio.run(main())


    

    