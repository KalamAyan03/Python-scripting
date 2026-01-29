# 1. IMPORTING LIBRARIES
# We import 'yfinance' (Yahoo Finance) to download live stock market data from the internet.
import yfinance as yf
# We import 'pandas' (as 'pd') to handle the data in table format (rows and columns).
import pandas as pd

# 2. DEFINING THE FUNCTION
# We create a reusable function named 'analyze_stock'. 
# It takes one input: 'ticker_symbol' (the name of the stock, e.g., 'KAYNES.NS').
def analyze_stock(ticker_symbol):
    
    # Just a print statement to show the user which stock is currently being processed.
    print(f"\n--- Analyzing {ticker_symbol} ---")
    
    # We create a 'Ticker' object using yfinance. This connects us to that specific company's data.
    stock = yf.Ticker(ticker_symbol)
    
    # 3. FETCHING HISTORICAL DATA
    # We ask for the price history (Open, High, Low, Close) for the last 1 year ('1y').
    # This stores the data in a variable named 'hist' (which is a pandas DataFrame/Table).
    hist = stock.history(period="1y")
    
    # 4. GETTING CURRENT PRICE
    # We look at the 'Close' column of our table and grab the last row (.iloc[-1]).
    # This gives us the most recent closing price.
    current_price = hist['Close'].iloc[-1]
    
    # 5. FINDING THE RANGE (HIGH vs LOW)
    # We scan the entire 'High' column to find the maximum price in the last year.
    high_52 = hist['High'].max()
    # We scan the entire 'Low' column to find the minimum price in the last year.
    low_52 = hist['Low'].min()
    
    # 6. CALCULATING MOVING AVERAGES (TRENDS)
    # We calculate the average of the last 50 days of closing prices.
    # .rolling(window=50) groups data in 50-day chunks; .mean() calculates the average.
    sma_50 = hist['Close'].rolling(window=50).mean().iloc[-1]
    
    # We calculate the average of the last 200 days (Long-term trend).
    # This is often used as a major support level by big investors.
    sma_200 = hist['Close'].rolling(window=200).mean().iloc[-1]
    
    # 7. CALCULATING FIBONACCI LEVELS (MATH PATTERNS)
    # First, calculate the total movement: Highest Price minus Lowest Price.
    diff = high_52 - low_52
    
    # Calculate the 38.2% Retracement Level: High - (Range * 0.382).
    # This is a minor support level.
    level_38 = high_52 - (diff * 0.382)
    
    # Calculate the 50% Retracement Level: High - (Range * 0.5).
    # The halfway point of the year's rally.
    level_50 = high_52 - (diff * 0.5)
    
    # Calculate the 61.8% Retracement Level: High - (Range * 0.618).
    # Known as the "Golden Pocket." This is statistically the strongest bounce zone.
    level_61 = high_52 - (diff * 0.618) 
    
    # 8. PRINTING THE RESULTS
    # We print the calculated numbers formatted to 2 decimal places (:.2f) for readability.
    print(f"Current Price:  ₹{current_price:.2f}")
    print(f"52-Week High:   ₹{high_52:.2f}")
    print("-" * 30) # Prints a divider line for neatness
    print("SUPPORT LEVELS (Where to Buy):")
    print(f"1. 50-Day Avg (Short Term):   ₹{sma_50:.2f}")
    print(f"2. 50% Retracement (Halfway): ₹{level_50:.2f}")
    print(f"3. 61.8% Golden Pocket (Best):₹{level_61:.2f}")
    print(f"4. 200-Day Avg (Strongest):   ₹{sma_200:.2f}")


    
    # 9. LOGIC FOR ADVICE (ALGORITHM)
    # We compare the Current Price against our calculated Support Levels.
    
    # IF price is below the Golden Pocket OR below the 200-Day Average...
    if current_price < level_61 or current_price < sma_200:
        # ...it implies the stock is very cheap/oversold.
        print("\nVerdict: STRONG BUY ZONE (Oversold)")
        
    # ELSE IF price is below the 50-Day Average (but above the deep supports)...
    elif current_price < sma_50:
        # ...it implies a normal correction is happening.
        print("\nVerdict: GOOD ACCUMULATION ZONE (Dipping)")
        
    # OTHERWISE (if price is high above all averages)...
    else:
        # ...it implies the stock is expensive or in a strong uptrend.
        print("\nVerdict: HOLD / WAIT (Trend is High)")

# 10. EXECUTING THE SCRIPT
# We call the function for 'KAYNES' on the NSE (National Stock Exchange).
analyze_stock("KAYNES.NS")
# We call the function for 'NETWEB' on the NSE.
analyze_stock("NETWEB.NS")