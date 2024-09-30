# ideal currency color palette
# 1 = cream / white
# 5 = green
# 10 = orange
# 25 = blue
# 50 = redblack
# 100 = royal purple

import random
import time
import webbrowser

import matplotlib.pyplot as plt
import yfinance as yf

# List of active currency pairs on Yahoo Finance (currency pairs)
currency_pairs = [
    "EURUSD=X", "JPYUSD=X", "GBPUSD=X", "AUDUSD=X", "CADUSD=X",
    "CHFUSD=X", "CNYUSD=X", "SEKUSD=X", "NZDUSD=X", "MXNUSD=X",
    "THBUSD=X", "ARSUSD=X", "HUFUSD=X", "EGPUSD=X",
    "KRWUSD=X", "KWDUSD=X", "OMRUSD=X", "ZARUSD=X", "AEDUSD=X",
    "BHDUSD=X", "JODUSD=X", "KYDUSD=X"
]

# Randomly select 10 currency pairs
selected_currencies = random.sample(currency_pairs, 10)

print(selected_currencies)


def open_image_search(currency_code, search_engine="google"):
    currency_code = currency_code[:3]
    if search_engine == "google":
        url = f"https://www.google.com/search?tbm=isch&q={currency_code}+currency+latest+series+bills"
    elif search_engine == "bing":
        url = f"https://www.bing.com/images/search?q={currency_code}+currency+latest+series+bills"
    else:
        print(f"Unknown search engine: {search_engine}")
        return

    print(f"Opening {search_engine.capitalize()} Image Search for {currency_code} currency bill...")
    webbrowser.open(url)


# Open image searches for each selected currency with user input to proceed
for currency in selected_currencies:
    open_image_search(currency, search_engine="google")  # or use "bing" for Bing search
    input("Press Enter to proceed to the next currency search...")  # Wait for user input

# input("Press Enter to continue...")

# Initial value in dollars to compare
usd_amount = 10

# Create a dictionary to store the comparison results
currency_values = {}


# Function to fetch exchange rate with retry logic
def fetch_exchange_rate(pair, retries=3):
    for attempt in range(retries):
        try:
            ticker = yf.Ticker(pair)
            data = ticker.history(period='1d')  # Fetch the latest exchange rate
            if not data.empty:  # Ensure the data isn't empty
                return data['Close'][0]  # Get the closing price (exchange rate)
            else:
                raise ValueError("No data returned")
        except Exception as e:
            print(f"Error fetching data for {pair}: {e}. Retrying... ({attempt + 1}/{retries})")
            time.sleep(1)  # Pause for a second before retrying
    return None  # Return None if all attempts fail


# Fetch today's exchange rate for each currency pair and calculate value in USD
for pair in selected_currencies:
    exchange_rate = fetch_exchange_rate(pair)
    if exchange_rate:
        # Split the pair name to get the base currency (e.g., EURUSD -> EUR)
        base_currency = pair[:3]
        currency_value = usd_amount * exchange_rate  # Convert 10 units of base currency to USD equivalent
        currency_values[base_currency] = currency_value
        print(f"{base_currency}: 10 units = {currency_value:.4f} USD (Exchange Rate: {exchange_rate:.4f})")
    else:
        print(f"Failed to fetch exchange rate for {pair} after multiple attempts.")

# Calculate the average of the 10 currencies in USD
if currency_values:
    average_value = sum(currency_values.values()) / len(currency_values)
    print(f"\nAverage value of 10 currencies in USD: {average_value:.4f}")

# Visualize the comparison using a bar chart
if currency_values:
    fig, ax = plt.subplots()

    # Create the bar chart
    bars = ax.bar(currency_values.keys(), currency_values.values(), color='green', width=0.5)

    # Add labels on top of the bars, formatted to 4 decimal places
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval:.4f}', ha='center', va='bottom')

    # Rotate the x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')

    # Add gridlines for better granularity
    ax.yaxis.grid(True, linestyle='--', which='major', color='gray', alpha=0.7)

    # Display the average value on the graph
    ax.text(0.5, 1.10, f'Average Value: ${average_value:.4f} USD', transform=ax.transAxes, fontsize=12, color='blue',
            ha='center')

    # Labels and title
    plt.xlabel('Currency')
    plt.ylabel('Value in USD')
    plt.title('Value of 10 Units of Random Currencies in USD')

    # Adjust layout to prevent label overlap
    plt.tight_layout()

    # Show the plot
    plt.show()
