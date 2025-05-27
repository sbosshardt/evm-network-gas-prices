"""Currency-related utilities for the EVM gas price monitor."""

from typing import Dict, TypedDict, List

class CurrencyInfo(TypedDict):
    """Type definition for currency information."""
    name: str
    symbol: str

# Define supported currencies with their symbols and friendly names
SUPPORTED_CURRENCIES: Dict[str, CurrencyInfo] = {
    "USD": {
        "name": "US Dollar",
        "symbol": "$"
    },
    "EUR": {
        "name": "Euro",
        "symbol": "€"
    },
    "GBP": {
        "name": "British Pound",
        "symbol": "£"
    },
    "JPY": {
        "name": "Japanese Yen",
        "symbol": "¥"
    },
    "CNY": {
        "name": "Chinese Yuan",
        "symbol": "¥"
    },
    "INR": {
        "name": "Indian Rupee",
        "symbol": "₹"
    },
    "KRW": {
        "name": "South Korean Won",
        "symbol": "₩"
    },
    "BTC": {
        "name": "Bitcoin",
        "symbol": "₿"
    },
    "ETH": {
        "name": "Ethereum",
        "symbol": "Ξ"
    },
    "BNB": {
        "name": "Binance Coin",
        "symbol": "BNB"
    }
}

# Default currency if none specified
DEFAULT_CURRENCY = "USD"

def normalize_currency(currency: str) -> str:
    """Normalize a currency code to uppercase for display and lowercase for API calls."""
    return currency.upper()

def get_currency_symbol(currency: str) -> str:
    """Get the symbol for a currency."""
    normalized = normalize_currency(currency)
    return SUPPORTED_CURRENCIES.get(normalized, {}).get("symbol", normalized)

def get_currency_name(currency: str) -> str:
    """Get the friendly name for a currency."""
    normalized = normalize_currency(currency)
    return SUPPORTED_CURRENCIES.get(normalized, {}).get("name", normalized)

def get_all_currencies() -> List[str]:
    """Get a list of all supported currency codes."""
    return list(SUPPORTED_CURRENCIES.keys())

def format_currency_help() -> str:
    """Format the currency help text for CLI output."""
    lines = ["  - all    (All of the currencies below.)"]
    for code, info in SUPPORTED_CURRENCIES.items():
        lines.append(f"  - {code:<6} ({info['name']}, {info['symbol']})")
    return "\n".join(lines) 