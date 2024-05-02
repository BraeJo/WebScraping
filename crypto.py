from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

def scrape_coinmarketcap():
    url = "https://coinmarketcap.com/"
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"})
    response = urlopen(req)
    soup = BeautifulSoup(response.read(), 'html.parser')
    table = soup.find('tbody')

    cryptocurrencies = []
    for row in table.find_all('tr')[:5]:
        data = row.find_all('td')
        name = data[1].find('p').text.strip()
        symbol = data[2].text.strip()
        price = data[3].text.strip()
        change_24h = data[4].text.strip()

        cryptocurrencies.append({
            "name": name,
            "symbol": symbol,
            "price": price,
            "change_24h": change_24h
        })

    return cryptocurrencies

def calculate_price_change(price, percentage_change):
    price_change = float(price) * (1 + percentage_change / 100)
    return price_change

def display_formatted_output(cryptocurrency):
    print("Crypto:", cryptocurrency["name"])
    if cryptocurrency["symbol"]:
        print("Symbol:", cryptocurrency["symbol"])
    print("Price:", cryptocurrency["price"])
    print("% Change in last 24 hrs:", cryptocurrency["change_24h"])
    print("Corresponding price (based on % change):", round(calculate_price_change(float(cryptocurrency["price"].replace('$', '').replace(',', '')), float(cryptocurrency["change_24h"].replace('%', ''))), 2))
    print()

if __name__ == "__main__":
    top_5_cryptos = scrape_coinmarketcap()
    for crypto in top_5_cryptos:
        display_formatted_output(crypto)
