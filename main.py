import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime

# =========================
# CREATE FOLDERS
# =========================
os.makedirs("data", exist_ok=True)
os.makedirs("images", exist_ok=True)
os.makedirs("reports", exist_ok=True)

# =========================
# USER INPUT
# =========================
ticker = input("Enter stock ticker symbol example AAPL, MSFT, TSLA: ").upper()

start_date = input("Enter start date YYYY-MM-DD: ")
end_date = input("Enter end date YYYY-MM-DD: ")

print("\nFetching stock data...")

# =========================
# FETCH STOCK DATA
# =========================
data = yf.download(ticker, start=start_date, end=end_date)

# =========================
# CHECK DATA
# =========================
if data.empty:
    print("No stock data found.")
    exit()

# =========================
# FIX COLUMN FORMAT
# =========================
close_prices = data["Close"].squeeze()

# =========================
# CLEAN DATA
# =========================
data.dropna(inplace=True)

# =========================
# CALCULATIONS
# =========================
data["Daily_Return"] = close_prices.pct_change()

data["SMA_20"] = close_prices.rolling(window=20).mean()
data["SMA_50"] = close_prices.rolling(window=50).mean()

highest_price = float(close_prices.max())
lowest_price = float(close_prices.min())
average_price = float(close_prices.mean())
latest_close = float(close_prices.iloc[-1])

volatility = float(data["Daily_Return"].std() * np.sqrt(252))

# =========================
# TREND ANALYSIS
# =========================
if data["SMA_20"].iloc[-1] > data["SMA_50"].iloc[-1]:
    trend = "Bullish Uptrend"
else:
    trend = "Bearish Downtrend"

# =========================
# SAVE CSV
# =========================
csv_path = f"data/{ticker}_stock_data.csv"
data.to_csv(csv_path)

# =========================
# CHART 1 - CLOSE PRICE
# =========================
plt.figure(figsize=(10, 5))
plt.plot(data.index, close_prices)

plt.title(f"{ticker} Closing Price")
plt.xlabel("Date")
plt.ylabel("Price")
plt.grid(True)

closing_chart = f"images/{ticker}_closing_price.png"
plt.savefig(closing_chart)
plt.close()

# =========================
# CHART 2 - MOVING AVERAGE
# =========================
plt.figure(figsize=(10, 5))

plt.plot(data.index, close_prices, label="Close Price")
plt.plot(data.index, data["SMA_20"], label="20 Day SMA")
plt.plot(data.index, data["SMA_50"], label="50 Day SMA")

plt.title(f"{ticker} Moving Average")
plt.xlabel("Date")
plt.ylabel("Price")

plt.legend()
plt.grid(True)

ma_chart = f"images/{ticker}_moving_average.png"

plt.savefig(ma_chart)
plt.close()

# =========================
# CHART 3 - DAILY RETURNS
# =========================
plt.figure(figsize=(10, 5))

plt.plot(data.index, data["Daily_Return"])

plt.title(f"{ticker} Daily Returns")
plt.xlabel("Date")
plt.ylabel("Returns")

plt.grid(True)

returns_chart = f"images/{ticker}_daily_returns.png"

plt.savefig(returns_chart)
plt.close()

# =========================
# REPORT GENERATION
# =========================
report = f"""
========================================
STOCK MARKET DATA ANALYZER REPORT
========================================

Ticker Symbol: {ticker}

Start Date: {start_date}
End Date: {end_date}

Generated On:
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

========================================
PRICE ANALYSIS
========================================

Latest Closing Price: {latest_close:.2f}

Highest Closing Price: {highest_price:.2f}

Lowest Closing Price: {lowest_price:.2f}

Average Closing Price: {average_price:.2f}

========================================
RISK ANALYSIS
========================================

Annual Volatility: {volatility:.4f}

========================================
TREND ANALYSIS
========================================

Current Trend:
{trend}

========================================
GENERATED FILES
========================================

CSV Data:
{csv_path}

Closing Price Chart:
{closing_chart}

Moving Average Chart:
{ma_chart}

Daily Returns Chart:
{returns_chart}

========================================
DISCLAIMER
========================================

This project is created only for educational purposes.

This is NOT financial advice.
"""

# =========================
# SAVE REPORT
# =========================
report_path = f"reports/{ticker}_analysis_report.txt"

with open(report_path, "w", encoding="utf-8") as file:
    file.write(report)

# =========================
# FINAL OUTPUT
# =========================
print("\n========================================")
print("PROJECT EXECUTED SUCCESSFULLY")
print("========================================")

print(f"\nCSV Saved: {csv_path}")

print("\nCharts Saved In images Folder")

print(f"\nReport Saved: {report_path}")

print("\n========================================")
print(report)