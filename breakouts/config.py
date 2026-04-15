# Breakout and Indicator Parameters
LOOKBACK_WINDOW = 20  # Days to look back for the breakout high
ATR_WINDOW = 14       # Window for calculating Average True Range (volatility)

# Risk Management & Exit Parameters
PROFIT_TARGET_ATR = 2.0  # Take profit at 2x ATR above entry
STOP_LOSS_ATR = 1.0      # Stop loss at 1x ATR below entry
TIMEOUT_DAYS = 10        # Maximum days to hold a trade before forcing a market exit

# General Parameters
INITIAL_CASH = 100000.0
POSITION_SIZE = 100      # Static share quantity for this implementation
RISK_FREE_RATE = 0.0375
