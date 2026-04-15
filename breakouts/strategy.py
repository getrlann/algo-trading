import pandas as pd
import numpy as np
import config

def calculate_indicators(df):
    """Calculates the breakout threshold (rolling high) and ATR."""
    df = df.copy()
    
    # 20-day rolling high (excluding the current day to avoid look-ahead bias)
    df['rolling_high'] = df['high'].shift(1).rolling(window=config.LOOKBACK_WINDOW).max()
    
    # Average True Range (ATR) calculation
    df['tr0'] = abs(df['high'] - df['low'])
    df['tr1'] = abs(df['high'] - df['close'].shift(1))
    df['tr2'] = abs(df['low'] - df['close'].shift(1))
    df['true_range'] = df[['tr0', 'tr1', 'tr2']].max(axis=1)
    df['atr'] = df['true_range'].rolling(window=config.ATR_WINDOW).mean()
    
    return df.dropna()

def run_backtest(df):
    """
    Plain English Explanation for Web Page:
    I define a breakout using a Donchian Channel framework. A long entry signal is triggered 
    when the daily closing price exceeds the highest high of the previous 20 trading days. 
    To manage risk, I set a strict exit protocol: the trade closes for a profit if it reaches 
    a target of 2x the Average True Range (ATR), closes for a loss if it drops below 1x the ATR, 
    or times out and closes at the market price after 10 trading days, whichever occurs first.
    """
    df = calculate_indicators(df)
    
    blotter_data = []
    ledger_data = []
    
    current_cash = config.INITIAL_CASH
    position = 0
    
    entry_price = 0.0
    entry_date = None
    days_in_trade = 0
    target_price = 0.0
    stop_price = 0.0
    
    for date, row in df.iterrows():
        # Check Exits if currently in a trade
        if position > 0:
            days_in_trade += 1
            exit_reason = None
            exit_price = 0.0
            
            # Intraday check: Did high hit target or low hit stop?
            if row['high'] >= target_price:
                exit_reason = 'Target Hit'
                exit_price = target_price
            elif row['low'] <= stop_price:
                exit_reason = 'Stop Loss'
                exit_price = stop_price
            elif days_in_trade >= config.TIMEOUT_DAYS:
                exit_reason = 'Timeout'
                exit_price = row['close']
                
            if exit_reason:
                blotter_data.append({
                    'entry_date': entry_date,
                    'exit_date': date,
                    'direction': 'Long',
                    'size': position,
                    'entry_price': entry_price,
                    'exit_price': exit_price,
                    'outcome': exit_reason
                })
                current_cash += (position * exit_price)
                position = 0
                days_in_trade = 0
                
        # Check Entries if flat
        if position == 0:
            if row['close'] > row['rolling_high']:
                position = config.POSITION_SIZE
                entry_price = row['close']
                entry_date = date
                days_in_trade = 0
                
                # Set static profit target and stop loss based on entry ATR
                target_price = entry_price + (row['atr'] * config.PROFIT_TARGET_ATR)
                stop_price = entry_price - (row['atr'] * config.STOP_LOSS_ATR)
                
                current_cash -= (position * entry_price)
                
        # Record Daily Ledger
        mkt_val = position * row['close']
        ledger_data.append({
            'date': date,
            'position': position,
            'cash': current_cash,
            'mkt_val': mkt_val,
            'NAV': current_cash + mkt_val
        })
        
    blotter = pd.DataFrame(blotter_data)
    ledger = pd.DataFrame(ledger_data).set_index('date')
    
    return blotter, ledger
