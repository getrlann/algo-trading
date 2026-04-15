import os
import pandas as pd
import shinybroker as sb
from strategy import run_backtest
from metrics import generate_reports
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

def main():
    print("Fetching data via shinybroker...")
    
    # Retrieve the variables, providing a default fallback for reproducibility
    host_ip = os.getenv("WINDOWS_HOST_IP", "127.0.0.1")
    tws_port = int(os.getenv("TWS_PORT", 7497)) 
    
    contract = sb.Contract({'symbol': 'SPY', 'secType': 'STK', 'exchange': 'SMART', 'currency': 'USD'})
    
    fetch_result = sb.fetch_historical_data(
        contract=contract, 
        barSizeSetting='1 day', 
        durationStr='2 Y', 
        host=host_ip, 
        port=tws_port
    )
    
    df = fetch_result['hst_dta'].copy()
    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.date
    df.set_index('timestamp', inplace=True)
    df.index = pd.to_datetime(df.index)
    
    print("Running backtest...")
    blotter, ledger = run_backtest(df)
    
    print("Generating reports and visualizations...")
    generate_reports(blotter, ledger)

if __name__ == "__main__":
    main()
