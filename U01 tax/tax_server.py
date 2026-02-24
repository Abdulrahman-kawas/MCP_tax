
# calling server mcp
from mcp.server.fastmcp import FastMCP
import pandas as pd
import os
# Create an MCP server
mcp = FastMCP("TaxAssistant", json_response=True)


# Add a dynamic greeting resource
@mcp.resource("resource://tax_config")
def tax_config():
    """hello this is some of tax config info"""
    df = pd.read_excel("tax_global.xlsx")
    df.columns = df.columns.str.strip()
    TAX_INFO = dict(zip(df["Country"].str.lower(),
                        df["VAT_Rate (%)"]))

    return TAX_INFO


@mcp.tool(name="calculate_tax", description="Calculate tax based on base amount and tax rate")
def calculate_tax(price: float, country: str) :
    config = tax_config()
    config_lower = {name.lower(): rate for name, rate in config.items()}
    country_key = country.strip().lower()
    if country_key not in config_lower:
        raise ValueError(f"Tax rate not found for country: {country}")
    tax_rate = config_lower[country_key]
    tax_amount = price * (tax_rate / 100)
    return round(tax_amount, 2)


@mcp.prompt(name="tax_greeting", description="Generate a greeting prompt for tax-related queries")
def tax_greeting(name: str, country: str) -> str:
    """Generate a greeting prompt for tax-related queries based on the user's name and country."""
    config = tax_config()
    config_lower = {name.lower(): rate for name, rate in config.items()}
    country_key = country.strip().lower()

    if country_key not in config_lower:
        raise ValueError(f"Hello {name}, tax rate not found for country: {country}")
    
    tax_rate = config_lower[country_key]
    return f"Hello {name}! The current tax rate in {country} is {tax_rate}%."


if __name__ == "__main__":
    mcp.run(transport="stdio")