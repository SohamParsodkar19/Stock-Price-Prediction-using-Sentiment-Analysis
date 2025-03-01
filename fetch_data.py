# fetch_data.py

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import pymysql

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',       # Replace with your MySQL username
    'password': 'Astrophile@31',   # Replace with your MySQL password
    'database': 'StockSentimentDB' # Your database name
}

# Fetch stock data
def fetch_stock_data(ticker='AAPL', days=1):
    try:
        end_date = datetime.today().strftime('%Y-%m-%d')
        start_date = (datetime.today() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        # Attempt to download stock data
        data = yf.download(ticker, start=start_date, end=end_date, progress=False)
        
        # Check if data is empty
        if data.empty:
            print(f"No data found for {ticker}. It may be delisted or the market was closed.")
            return None
        
        data.reset_index(inplace=True)
        
        # Rename 'Date' column to lowercase 'date' and format it without timezone
        data.rename(columns={'Date': 'date', 'Open': 'open', 'High': 'high', 
                             'Low': 'low', 'Close': 'close', 'Volume': 'volume'}, inplace=True)
        
        # Convert date column to remove timezone information and format as 'YYYY-MM-DD'
        data['date'] = data['date'].dt.date
        
        return data[['date', 'open', 'high', 'low', 'close', 'volume']]
    
    except ValueError as e:
        print(f"Failed to download data for {ticker}: {e}")
        return None

# Fetch sentiment data (dummy data for example)
def fetch_sentiment_data():
    data = {
        'date': [datetime.today().date()],  # Use lowercase 'date' to match SQL schema
        'daily_sentiment': [0.1]  # Placeholder for sentiment analysis result
    }
    return pd.DataFrame(data)

# Store data in SQL
def store_data(stock_data, sentiment_data):
    if stock_data is None:
        print("No stock data to store.")
        return
    
    try:
        # Connect to MySQL
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
        
        # Store stock data
        for index, row in stock_data.iterrows():
            cursor.execute("""
                INSERT INTO stock_data (date, open, high, low, close, volume)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (row['date'], row['open'], row['high'], row['low'], row['close'], row['volume'])
            )
        
        # Store sentiment data
        for index, row in sentiment_data.iterrows():
            cursor.execute("""
                INSERT INTO sentiment_data (date, daily_sentiment)
                VALUES (%s, %s)
                """,
                (row['date'], row['daily_sentiment'])
            )

        connection.commit()
        print("Data successfully stored in SQL.")
        
    except Exception as e:
        print("Error storing data:", e)
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    stock_data = fetch_stock_data()
    sentiment_data = fetch_sentiment_data()
    store_data(stock_data, sentiment_data)
    print("Data fetching and storage completed.")
