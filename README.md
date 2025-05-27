# EVM Network Gas Price Monitor

A command-line tool for monitoring gas prices across multiple EVM networks. The tool provides real-time gas price data, native token costs, and USD (or other currency) costs for transactions.

## Features

- Monitor gas prices across multiple EVM networks:
  - Ethereum
  - Polygon
  - Arbitrum
  - Avalanche
  - Base
  - BSC (Binance Smart Chain)
  - Fantom
  - Linea
  - Optimism
- View gas prices in multiple currencies (USD, EUR, GBP, JPY, CNY, INR, KRW, BTC, ETH, BNB)
- Locale-aware number formatting
- Multiple RPC endpoints per network with automatic fallback
- JSON output support
- Asynchronous data fetching for better performance

## Installation

1. Clone the repository:
```bash
git clone https://github.com/sbosshardt/evm-network-gas-prices.git
cd evm-network-gas-prices
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Make the script executable:
```bash
chmod +x evm-gas
```

## Usage

The tool provides several ways to view gas price information:

### Basic Usage

Show gas costs in your locale's currency (or all currencies if not supported):
```bash
./evm-gas
```

### Command Options

- `--gas-prices`: Show only gas prices for all networks
- `--currency-prices`: Show only cryptocurrency prices
- `--units <number>`: Specify number of million gas units to calculate for (default: 1.0)
- `--currencies <list>`: Specify currencies to show prices in
- `--json`: Output in JSON format

### Examples

Show gas prices in USD:
```bash
./evm-gas --currencies USD
```

Show gas prices in multiple currencies:
```bash
./evm-gas --currencies USD EUR GBP
```

Show gas prices in all supported currencies:
```bash
./evm-gas --currencies all
```

Show only gas prices (no USD costs):
```bash
./evm-gas --gas-prices
```

Show only cryptocurrency prices:
```bash
./evm-gas --currency-prices
```

Calculate costs for 2 million gas units:
```bash
./evm-gas --units 2.0
```

Get output in JSON format:
```bash
./evm-gas --json
```

### Output Format

The tool provides detailed output including:
- Gas price in gwei
- Native token cost
- Costs in specified currencies
- Token prices in specified currencies
- Block number
- RPC URL used
- Timestamp and datetime

Example output:
```
Gas Costs (for 1M gas units):
--------------------------------------------------------------------------------
Ethereum:
  Gas Price: 20.12345 gwei
  Native Token: Ethereum (ETH)
  Native Token Cost: 0.00040247 ETH
  USD Cost: $2,592.34
  Token Price (USD): $2,592.34
  Block Number: 19,123,456
  RPC URL: https://eth-mainnet.g.alchemy.com/v2/...
  Timestamp: 1710864000
  As of: 2024-03-19 12:00:00 UTC
```

### Number Formatting

The tool uses locale-aware number formatting:
- Integers show no decimal places
- Numbers greater than 1 show 2 decimal places
- Numbers less than 1 show 5 significant figures
- Thousands separators are added according to locale

### Supported Networks

The tool supports the following networks:
- Ethereum
- Polygon
- Arbitrum
- Avalanche
- Base
- BSC (Binance Smart Chain)
- Fantom
- Linea
- Optimism

### Supported Currencies

The tool supports the following currencies:
- USD (US Dollar, $)
- EUR (Euro, €)
- GBP (British Pound, £)
- JPY (Japanese Yen, ¥)
- CNY (Chinese Yuan, ¥)
- INR (Indian Rupee, ₹)
- KRW (South Korean Won, ₩)
- BTC (Bitcoin, ₿)
- ETH (Ethereum, Ξ)
- BNB (Binance Coin, BNB)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 