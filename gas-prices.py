from web3 import Web3

# Define RPC endpoints
RPC_ENDPOINTS = {
    #"Ethereum Mainnet": "https://rpc.ankr.com/eth",
    "Ethereum Mainnet": "https://eth.merkle.io",
    "Arbitrum One": "https://arb1.arbitrum.io/rpc",
    "Gnosis": "https://rpc.gnosis.gateway.fm",
    "Polygon": "https://polygon-rpc.com",
    "Fantom": "https://rpc.fantom.foundation",
}

GAS_UNITS = 1_000_000

def wei_to_eth(wei):
    return wei / 10**18

for name, url in RPC_ENDPOINTS.items():
    try:
        w3 = Web3(Web3.HTTPProvider(url))
        gas_price = w3.eth.gas_price  # in wei
        total_cost_wei = gas_price * GAS_UNITS
        native_token_cost = wei_to_eth(total_cost_wei)

        print(f"--- {name} ---")
        print(f"Gas Price: {Web3.from_wei(gas_price, 'gwei')} gwei")
        print(f"Tx Cost for 1M gas: {total_cost_wei} wei ({native_token_cost:.6f} native token)\n")

    except Exception as e:
        print(f"Failed to fetch data for {name}: {e}")
