# EVM Network Gas Prices

A Python tool to monitor gas prices across various EVM-compatible networks and track cryptocurrency prices. This tool helps users make informed decisions about transaction costs across different networks.

## Features

- Real-time gas price monitoring for multiple EVM networks:
  - Ethereum Mainnet
  - Arbitrum One
  - Gnosis
  - Polygon
  - Fantom
- Cryptocurrency price tracking for:
  - ETH/USD
  - FTM/USD
  - xDAI (pegged to USD)
- Calculates transaction costs for 1M gas units
- Displays prices in both native tokens and USD

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/sbosshardt/evm-network-gas-prices.git
cd evm-network-gas-prices
```

2. Create and activate a virtual environment:

### Linux/macOS
```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows
```bash
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running Gas Price Monitor
```bash
python gas-prices.py
```
This will display current gas prices and estimated transaction costs for 1M gas units across all supported networks.

### Running Cryptocurrency Price Tracker
```bash
python cryptocurrency-prices.py
```
This will show current prices for ETH, FTM, and xDAI in USD.

## Output Examples

### Gas Prices Output
```
--- Ethereum Mainnet ---
Gas Price: 25.5 gwei
Tx Cost for 1M gas: 25500000000000 wei (0.025500 native token)

--- Arbitrum One ---
Gas Price: 0.1 gwei
Tx Cost for 1M gas: 100000000000 wei (0.000100 native token)
```

### Cryptocurrency Prices Output
```
Cryptocurrency Prices (2024-03-21 15:30:45):
----------------------------------------
ETH:  $3,500.25 USD
FTM:  $0.45 USD
xDAI: $1.00 USD (pegged)
```

## Configuration

The RPC endpoints are configured in `gas-prices.py`. You can modify the `RPC_ENDPOINTS` dictionary to add or remove networks:

```python
RPC_ENDPOINTS = {
    "Ethereum Mainnet": "https://eth.merkle.io",
    "Arbitrum One": "https://arb1.arbitrum.io/rpc",
    "Gnosis": "https://rpc.gnosis.gateway.fm",
    "Polygon": "https://polygon-rpc.com",
    "Fantom": "https://rpc.fantom.foundation",
}
```

## Troubleshooting

1. If you encounter connection errors:
   - Check your internet connection
   - Verify that the RPC endpoints are accessible
   - Try using alternative RPC endpoints

2. If you get Python package errors:
   - Ensure you're in the virtual environment
   - Try reinstalling dependencies: `pip install -r requirements.txt --upgrade`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 