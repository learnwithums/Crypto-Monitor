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
        "per_page": 20,
        "page": 1,
        "sparkline": "false"
    }

    url = "https://api.coingecko.com/api/v3/coins/markets"
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("Error fetching data:", response.status_code)
        return ""

    data = response.json()

    TRADING_FEE_PERCENT = 1.5  # Total buy+sell fee
    INVESTMENT = 100000
    FEE_AMOUNT = (TRADING_FEE_PERCENT / 100) * INVESTMENT

    output = f"# 🪙 Crypto Prices in INR (Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n\n"
    output += "| Logo | Symbol | Name       | Price (INR) | Est. High | Est. Low | Gross Profit | Fees | Net Profit | ROI % |\n"
    output += "|------|--------|------------|-------------|-----------|----------|---------------|------|-------------|--------|\n"

    for coin in data:
        symbol = coin['symbol'].upper()
        name = coin['name']
        price = coin['current_price']
        price_str = f"₹{price:,}"
        logo_url = coin['image']

        range_delta = (coin['high_24h'] - coin['low_24h']) * 0.3
        est_high = price + (range_delta / 2)
        est_low = price - (range_delta / 2)

        try:
            units = INVESTMENT / est_low
            gross_return = units * est_high
            gross_profit = gross_return - INVESTMENT
            net_profit = gross_profit - FEE_AMOUNT
            roi_percent = (net_profit / INVESTMENT) * 100
        except ZeroDivisionError:
            gross_profit = 0
            net_profit = 0
            roi_percent = 0

        output += (
            f"| ![]({logo_url}) | {symbol:<6} | {name:<10} | ₹{price:,.2f} "
            f"| ₹{est_high:,.2f} | ₹{est_low:,.2f} | ₹{gross_profit:,.2f} "
            f"| ₹{FEE_AMOUNT:,.2f} | ₹{net_profit:,.2f} | {roi_percent:.2f}% |\n"
        )

    return output

if __name__ == "__main__":
    readme_content = get_crypto_data()
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
