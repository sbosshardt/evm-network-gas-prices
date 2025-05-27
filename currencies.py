"""Currency-related utilities for the EVM gas price monitor."""

from typing import Dict, TypedDict, List
import locale
from locale import getlocale

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

# Map locale currency codes to our supported currencies
LOCALE_CURRENCY_MAP = {
    "USD": "USD",  # United States
    "EUR": "EUR",  # European Union
    "GBP": "GBP",  # United Kingdom
    "JPY": "JPY",  # Japan
    "CNY": "CNY",  # China
    "INR": "INR",  # India
    "KRW": "KRW",  # South Korea
    # Add more mappings as needed
}

def get_locale_currency() -> str:
    """Get the user's locale currency code, falling back to 'all' if not supported."""
    try:
        # Get the locale's currency code
        locale.setlocale(locale.LC_ALL, '')
        currency_code = locale.localeconv()['int_curr_symbol'].strip()
        
        # Map to our supported currency or return 'all'
        return LOCALE_CURRENCY_MAP.get(currency_code, "all")
    except (locale.Error, KeyError):
        return "all"

def get_locale_format() -> Dict[str, str]:
    """Get the locale's number formatting preferences."""
    try:
        locale.setlocale(locale.LC_ALL, '')
        conv = locale.localeconv()
        return {
            "decimal_point": conv['decimal_point'],
            "thousands_sep": conv['thousands_sep'],
            "grouping": conv['grouping']
        }
    except locale.Error:
        # Fall back to US formatting
        return {
            "decimal_point": ".",
            "thousands_sep": ",",
            "grouping": [3, 0]  # Group by 3 digits
        }

def format_number(number: float, precision: int = 5) -> str:
    """Format a number according to the locale's preferences.
    
    For values less than 1, uses significant figures instead of fixed precision
    to avoid showing all zeros.
    For integers, shows no decimal places.
    For numbers greater than 1, uses 2 decimal places.
    """
    fmt = get_locale_format()
    
    # Check if number is effectively an integer
    is_integer = abs(number - round(number)) < 1e-10
    
    if is_integer:
        # For integers, use no decimal places
        num_str = f"{int(round(number))}"
    else:
        # For values less than 1, use significant figures
        if abs(number) < 1 and number != 0:
            # Count leading zeros after decimal point
            str_num = f"{number:.10f}"  # Use high precision for calculation
            if fmt["decimal_point"] in str_num:
                int_part, dec_part = str_num.split(fmt["decimal_point"])
                leading_zeros = len(dec_part) - len(dec_part.lstrip('0'))
                # Use 5 significant figures, adjusting for leading zeros
                precision = max(5, leading_zeros + 5)
        else:
            # For numbers greater than or equal to 1, use 2 decimal places
            precision = 2
        
        # Convert to string with calculated precision
        num_str = f"{number:.{precision}f}"
    
    # Split into integer and decimal parts
    if fmt["decimal_point"] in num_str:
        int_part, dec_part = num_str.split(fmt["decimal_point"])
    else:
        int_part, dec_part = num_str, ""
    
    # Add thousands separators
    if fmt["grouping"]:
        # Reverse the integer part for easier grouping
        int_part_rev = int_part[::-1]
        groups = []
        for i in range(0, len(int_part_rev), fmt["grouping"][0]):
            groups.append(int_part_rev[i:i + fmt["grouping"][0]])
        # Join groups and reverse back
        int_part = fmt["thousands_sep"].join(groups)[::-1]
    
    # Combine parts
    if dec_part:
        return f"{int_part}{fmt['decimal_point']}{dec_part}"
    return int_part

def normalize_currency(currency: str) -> str:
    """Normalize a currency code to uppercase for display and lowercase for API calls."""
    if currency.lower() == "all":
        return "all"
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