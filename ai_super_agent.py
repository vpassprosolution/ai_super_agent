from fastapi import FastAPI
import requests
import yfinance as yf
import pandas as pd

app = FastAPI()

# Root endpoint to confirm API is running
@app.get("/")
def home():
    return {"message": "AI Super Agent is running!"}

# Function to fetch real-time gold price
def get_gold_price():
    try:
        gold = yf.Ticker("GC=F")  # Gold Futures symbol
        gold_data = gold.history(period="1d", interval="5m")  # Get last 5-minute data
        if gold_data.empty:
            return None  # No data available
        latest_price = gold_data["Close"].iloc[-1]  # Get latest closing price
        return latest_price
    except Exception as e:
        return None  # Return None if there's an error fetching data

# Function to analyze market and give Buy/Sell recommendation
def analyze_market():
    gold_price = get_gold_price()
    if gold_price is None:
        return {"error": "Failed to retrieve gold price"}

    try:
        # Fetch historical data for analysis
        gold = yf.Ticker("GC=F")
        history = gold.history(period="1d", interval="5m")  # Get last 5-min intervals
        if history.empty or len(history) < 3:
            return {"error": "Not enough data for analysis"}

        # Get last three closing prices
        last_prices = history["Close"].iloc[-3:].tolist()

        # Determine market trend
        trend = "Neutral"
        if last_prices[-1] > last_prices[-2] > last_prices[-3]:  
            trend = "Bullish"
        elif last_prices[-1] < last_prices[-2] < last_prices[-3]:  
            trend = "Bearish"

        # AI Suggestion based on trend
        if trend == "Bullish":
            decision = "BUY"
            stop_loss = round(gold_price - 2, 2)  # Example SL
            take_profit = round(gold_price + 4, 2)  # Example TP
        elif trend == "Bearish":
            decision = "SELL"
            stop_loss = round(gold_price + 2, 2)
            take_profit = round(gold_price - 4, 2)
        else:
            decision = "HOLD"
            stop_loss = None
            take_profit = None

        return {
            "gold_price": gold_price,
            "trend": trend,
            "decision": decision,
            "stop_loss": stop_loss,
            "take_profit": take_profit
        }

    except Exception as e:
        return {"error": "Market analysis failed"}

# FastAPI endpoint to get AI trading signal
@app.get("/ai-signal")
def ai_signal():
    result = analyze_market()
    return result
