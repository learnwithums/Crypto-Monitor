import requests
from datetime import datetime

def get_crypto_data():
    coins = [
        "bitcoin", "ethereum", "dogecoin", "solana", "pepe", "floki",
        "polygon", "shiba-inu", "cardano", "tron", "avalanche-2",
        "chainlink", "polkadot", "uniswap", "litecoin", "optimism",
        "arbitrum", "render-token", "the-graph", "aptos", "injective",
        "stellar", "kaspa", "mantle"
    ]

    params = {
        "vs_currency": "inr",
        "ids": ",".join(coins),
        "order": "market_cap_desc",
        "per_page": 20,  # fixed to 20 coins max
        "page": 1,
        "sparkline": "false"
    }

    url = "https://api.coingecko.com/api/v3/coins/markets"
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("Error fetching data:", response.status_code)
        return ""

    data = response.json()

    output = f"# 🪙 Crypto Prices in INR (Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n\n"
    output += "| Logo | Symbol | Name       | Price (INR) | 4-6h High | 4-6h Low | Profit on ₹1L |\n"
    output += "|------|--------|------------|-------------|-----------|----------|----------------|\n"

    for coin in data:
        symbol = coin['symbol'].upper()
        name = coin['name']
        price = coin['current_price']
        price_str = f"₹{price:,}"
        logo_url = coin['image']

        # Estimate 4–6h range using 30% of the 24h range
        range_delta = (coin['high_24h'] - coin['low_24h']) * 0.3
        est_high = price + (range_delta / 2)
        est_low = price - (range_delta / 2)

        # Profit calculation if ₹1L invested at est_low and sold at est_high
        try:
            profit = ((est_high - est_low) / est_low) * 100000
        except ZeroDivisionError:
            profit = 0

        output += (
            f"| ![]({logo_url}) | {symbol:<6} | {name:<10} | {price_str} "
            f"| ₹{est_high:,.2f} | ₹{est_low:,.2f} | ₹{profit:,.2f} |\n"
        )

    return output

if __name__ == "__main__":
    readme_content = get_crypto_data()
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)


