import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import config

def generate_reports(blotter, ledger, output_dir='./data'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # 1. Export CSVs (Rounded to 2 decimal places)
    blotter.round(2).to_csv(f'{output_dir}/trades.csv', index=False)
    ledger.round(2).to_csv(f'{output_dir}/ledger.csv')
    
    # 2. Performance Metrics
    ledger['log_ret'] = np.log(ledger['NAV'] / ledger['NAV'].shift(1))
    clean_ret = ledger['log_ret'].dropna()
    
    annualized_return = clean_ret.mean() * 252
    volatility = clean_ret.std() * np.sqrt(252)
    sharpe_ratio = (annualized_return - config.RISK_FREE_RATE) / volatility if volatility != 0 else 0
    
    blotter['return_pct'] = (blotter['exit_price'] - blotter['entry_price']) / blotter['entry_price']
    avg_trade_return = blotter['return_pct'].mean()
    win_rate = len(blotter[blotter['return_pct'] > 0]) / len(blotter) if not blotter.empty else 0
    
    print("\n--- Strategy Performance Metrics ---")
    print(f"Annualized Return: {annualized_return:.2%}")
    print(f"Annualized Volatility: {volatility:.2%}")
    print(f"Sharpe Ratio (RFR {config.RISK_FREE_RATE}): {sharpe_ratio:.4f}")
    print(f"Total Trades: {len(blotter)}")
    print(f"Win Rate: {win_rate:.2%}")
    print(f"Average Return per Trade: {avg_trade_return:.2%}")
    
    # 3. Trade Outcome Analysis (Histogram)
    outcome_counts = blotter['outcome'].value_counts().reset_index()
    outcome_counts.columns = ['Outcome', 'Count']
    
    fig_hist = px.bar(
        outcome_counts, 
        x='Outcome', 
        y='Count', 
        title='Trade Outcomes: Breakout Strategy',
        color='Outcome',
        color_discrete_map={'Target Hit': 'green', 'Stop Loss': 'red', 'Timeout': 'gray'}
    )
    fig_hist.write_html(f'{output_dir}/outcome_histogram.html')
    
    # 4. Equity Curve
    fig_equity = px.line(ledger, x=ledger.index, y='NAV', title='Portfolio Equity Curve')
    fig_equity.write_html(f'{output_dir}/equity_curve.html')
    
    print(f"\nExports complete. Data and Plotly HTML files saved to {output_dir}/")
    
