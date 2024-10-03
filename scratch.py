import random
import matplotlib.pyplot as plt
import yfinance as yf

# Define file for tracking processed currencies
CURRENCY_FILE = 'processed_currencies.txt'

# Load processed currencies from a text file
def load_processed_currencies(file_name):
    try:
        with open(file_name, 'r') as f:
            return set(line.strip() for line in f.readlines())
    except FileNotFoundError:
        return set()  # If the file doesn't exist, start with an empty set

# Save processed currencies to the text file
def save_processed_currency(file_name, currency):
    with open(file_name, 'a') as f:
        f.write(f"{currency}\n")

# Get a random currency that hasn't been processed yet
def get_random_currency(all_currencies, processed_currencies):
    available_currencies = list(set(all_currencies) - processed_currencies)
    if available_currencies:
        return random.choice(available_currencies)
    else:
        return None  # Return None if no new currencies are left

# Function to fetch the latest exchange rate from Yahoo Finance
def fetch_exchange_rate(base_currency, quote_currency='USD'):
    try:
        pair = f"{base_currency}{quote_currency}=X"
        ticker = yf.Ticker(pair)
        hist = ticker.history(period='1d')
        if not hist.empty:
            latest_rate = hist['Close'].iloc[-1]
            return latest_rate
        else:
            print(f"Error fetching exchange rate for {base_currency}. No data available.")
            return None
    except Exception as e:
        print(f"Error fetching exchange rate for {base_currency}: {e}")
        return None

# Main script
def main():
    all_currencies = ['USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'CHF', 'NZD', 'CNY', 'MXN']  # Add more as needed
    processed_currencies = load_processed_currencies(CURRENCY_FILE)

    # Generate a list of 10 random currencies that haven't been processed yet
    selected_currencies = []
    for _ in range(10):
        currency = get_random_currency(all_currencies, processed_currencies)
        if currency:
            selected_currencies.append(currency)
            processed_currencies.add(currency)  # Mark it as processed
            save_processed_currency(CURRENCY_FILE, currency)  # Save to file
        else:
            print("No more available currencies to select.")
            break

    # Fetch and store exchange rates for selected currencies
    exchange_rates = {}
    for currency in selected_currencies:
        rate = fetch_exchange_rate(currency)
        if rate is not None:
            exchange_rates[currency] = rate

    # Print the selected currencies and their exchange rates
    print("Selected currencies and their rates (against USD):")
    for currency, rate in exchange_rates.items():
        print(f"{currency}: {rate:.4f}")

    # Plotting the data
    plt.figure(figsize=(10, 6))
    currency_names = list(exchange_rates.keys())
    currency_values = list(exchange_rates.values())

    plt.bar(currency_names, currency_values, color='skyblue')
    plt.xlabel('Currencies')
    plt.ylabel('Exchange Rate against USD')
    plt.title('Selected Currency Exchange Rates against USD')

    # Calculate and display the average exchange rate
    average_rate = sum(currency_values) / len(currency_values) if currency_values else 0
    plt.figtext(0.5, -0.1, f"Average Exchange Rate: {average_rate:.4f} USD", wrap=True, horizontalalignment='center', fontsize=12, color='blue')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
