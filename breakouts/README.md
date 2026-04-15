# Breakout Strategy Analysis: Capturing Momentum in QQQ

## Strategy Logic
This project implements a trend-following breakout strategy designed to capture short-term momentum. The core logic operates on the premise that when an asset pushes past a recent historical high, it signals distinct buying pressure and the potential for a continued upward move. I enter a long position immediately upon identifying this breakout. To manage risk and capital allocation systematically, the strategy utilizes a volatility-adjusted framework, defining dynamic profit targets and stop losses based on the asset's Average True Range (ATR). A strict time limit is also enforced to prevent capital from remaining tied up in trades that fail to develop momentum.

## Asset Selection
I selected the SPDR S&P 500 ETF Trust (SPY) as the primary asset for this backtest, using a two-year historical window. During the initial screening process, I evaluated various index ETFs and highly liquid large-cap equities. SPY was chosen because it provides the deepest liquidity and represents the broadest measure of US equity market momentum. While it exhibits lower absolute volatility than sector-specific or tech-heavy ETFs, its high volume ensures minimal slippage, and its price action provides a clean, macroeconomic baseline for evaluating a foundational ATR-based breakout system.

## Breakout Definition & Execution Rules
The `run_backtest` Python function serves as the core execution engine of the strategy. It iterates through the dataset chronologically. First, it evaluates the portfolio state. If the portfolio is flat (no active position), the function checks if today's closing price is strictly greater than the highest high of the previous 20 trading days. If this condition is met, it executes a long entry. Upon entry, it dynamically calculates and logs the profit target and stop-loss levels based on the asset's Average True Range (ATR) for that specific day. If the portfolio is already holding a position, the function bypasses the entry logic and evaluates whether today's price action breached any of the predefined exit boundaries, logging the trade outcome and updating the cash balance accordingly.

I define a breakout using a modified Donchian Channel framework. The primary indicator parameters and exit cutoffs are defined as follows:

* **Lookback Window:** 20 days
* **Volatility Window:** 14-day Average True Range (ATR)
* **Profit Target:** +2.0x ATR
* **Stop-Loss:** -1.0x ATR
* **Time-Stop:** 10 trading days

A long entry signal triggers when the daily closing price exceeds the highest high of the previous 20 trading days. Upon entry, the trade is subject to three mutually exclusive exit conditions. The position closes successfully if the price reaches 2.0x the ATR above the entry price. Conversely, it closes for a managed loss if the price drops 1.0x the ATR below the entry price. Finally, if neither the target nor the stop-loss is triggered within 10 trading days, the trade times out and automatically closes at the current market price. 

## Trade Ledger & Blotter
The complete log of all executed trades, including entry/exit timestamps, pricing, and position sizing, is available for review. 

### Full Trades

|entry_date|exit_date |direction|size|entry_price|exit_price|outcome   |
|----------|----------|---------|----|-----------|----------|----------|
|2024-05-14|2024-05-29|Long     |100 |523.3      |526.1     |Timeout   |
|2024-06-05|2024-06-12|Long     |100 |534.67     |544.02    |Target Hit|
|2024-06-12|2024-06-27|Long     |100 |541.36     |546.37    |Timeout   |
|2024-07-03|2024-07-10|Long     |100 |551.46     |559.5     |Target Hit|
|2024-07-10|2024-07-11|Long     |100 |561.32     |557.42    |Stop Loss |
|2024-07-16|2024-07-17|Long     |100 |564.86     |560.5     |Stop Loss |
|2024-08-19|2024-09-03|Long     |100 |559.61     |552.08    |Timeout   |
|2024-09-19|2024-10-03|Long     |100 |570.98     |567.82    |Timeout   |
|2024-10-09|2024-10-23|Long     |100 |577.14     |577.99    |Timeout   |
|2024-11-06|2024-11-15|Long     |100 |591.04     |584.78    |Stop Loss |
|2024-11-29|2024-12-13|Long     |100 |602.55     |604.21    |Timeout   |
|2025-01-22|2025-01-27|Long     |100 |606.44     |598.87    |Stop Loss |
|2025-02-18|2025-02-21|Long     |100 |611.49     |605.71    |Stop Loss |


* [Download Full Trades CSV](./data/trades.csv)


### Daily Ledger

|date      |position  |cash|mkt_val|NAV   |
|----------|----------|----|-------|------|
|2024-05-14|100       |47670.0|52330.0|100000.0|
|2024-05-15|100       |47670.0|52978.0|100648.0|
|2024-05-16|100       |47670.0|52869.0|100539.0|
|2024-05-17|100       |47670.0|52945.0|100615.0|
|2024-05-20|100       |47670.0|53006.0|100676.0|
|2024-05-21|100       |47670.0|53136.0|100806.0|
|2024-05-22|100       |47670.0|52983.0|100653.0|
|2024-05-23|100       |47670.0|52596.0|100266.0|
|2024-05-24|100       |47670.0|52944.0|100614.0|
|2024-05-28|100       |47670.0|52981.0|100651.0|
|2024-05-29|0         |100280.0|0.0    |100280.0|
|2024-05-30|0         |100280.0|0.0    |100280.0|
|2024-05-31|0         |100280.0|0.0    |100280.0|
|2024-06-03|0         |100280.0|0.0    |100280.0|
|2024-06-04|0         |100280.0|0.0    |100280.0|
|2024-06-05|100       |46813.0|53467.0|100280.0|
|2024-06-06|100       |46813.0|53466.0|100279.0|
|2024-06-07|100       |46813.0|53401.0|100214.0|
|2024-06-10|100       |46813.0|53566.0|100379.0|
|2024-06-11|100       |46813.0|53695.0|100508.0|
|2024-06-12|100       |47078.57|54136.0|101214.57|
|2024-06-13|100       |47078.57|54245.0|101323.57|
|2024-06-14|100       |47078.57|54278.0|101356.57|
|2024-06-17|100       |47078.57|54710.0|101788.57|
|2024-06-18|100       |47078.57|54849.0|101927.57|
|2024-06-20|100       |47078.57|54700.0|101778.57|
|2024-06-21|100       |47078.57|54451.0|101529.57|
|2024-06-24|100       |47078.57|54274.0|101352.57|
|2024-06-25|100       |47078.57|54483.0|101561.57|
|2024-06-26|100       |47078.57|54551.0|101629.57|
|2024-06-27|0         |101715.57|0.0    |101715.57|
|2024-06-28|0         |101715.57|0.0    |101715.57|
|2024-07-01|0         |101715.57|0.0    |101715.57|
|2024-07-02|0         |101715.57|0.0    |101715.57|
|2024-07-03|100       |46569.57|55146.0|101715.57|
|2024-07-05|100       |46569.57|55464.0|102033.57|
|2024-07-08|100       |46569.57|55528.0|102097.57|
|2024-07-09|100       |46569.57|55582.0|102151.57|
|2024-07-10|100       |46388.0|56132.0|102520.0|
|2024-07-11|0         |102130.43|0.0    |102130.43|
|2024-07-12|0         |102130.43|0.0    |102130.43|
|2024-07-15|0         |102130.43|0.0    |102130.43|
|2024-07-16|100       |45644.43|56486.0|102130.43|
|2024-07-17|0         |101694.21|0.0    |101694.21|
|2024-07-18|0         |101694.21|0.0    |101694.21|
|2024-07-19|0         |101694.21|0.0    |101694.21|
|2024-07-22|0         |101694.21|0.0    |101694.21|
|2024-07-23|0         |101694.21|0.0    |101694.21|
|2024-07-24|0         |101694.21|0.0    |101694.21|
|2024-07-25|0         |101694.21|0.0    |101694.21|
|2024-07-26|0         |101694.21|0.0    |101694.21|
|2024-07-29|0         |101694.21|0.0    |101694.21|
|2024-07-30|0         |101694.21|0.0    |101694.21|
|2024-07-31|0         |101694.21|0.0    |101694.21|
|2024-08-01|0         |101694.21|0.0    |101694.21|
|2024-08-02|0         |101694.21|0.0    |101694.21|
|2024-08-05|0         |101694.21|0.0    |101694.21|
|2024-08-06|0         |101694.21|0.0    |101694.21|
|2024-08-07|0         |101694.21|0.0    |101694.21|
|2024-08-08|0         |101694.21|0.0    |101694.21|
|2024-08-09|0         |101694.21|0.0    |101694.21|
|2024-08-12|0         |101694.21|0.0    |101694.21|
|2024-08-13|0         |101694.21|0.0    |101694.21|
|2024-08-14|0         |101694.21|0.0    |101694.21|
|2024-08-15|0         |101694.21|0.0    |101694.21|
|2024-08-16|0         |101694.21|0.0    |101694.21|
|2024-08-19|100       |45733.21|55961.0|101694.21|
|2024-08-20|100       |45733.21|55870.0|101603.21|
|2024-08-21|100       |45733.21|56062.0|101795.21|
|2024-08-22|100       |45733.21|55622.0|101355.21|
|2024-08-23|100       |45733.21|56213.0|101946.21|
|2024-08-26|100       |45733.21|56079.0|101812.21|
|2024-08-27|100       |45733.21|56156.0|101889.21|
|2024-08-28|100       |45733.21|55830.0|101563.21|
|2024-08-29|100       |45733.21|55835.0|101568.21|
|2024-08-30|100       |45733.21|56368.0|102101.21|
|2024-09-03|0         |100941.21|0.0    |100941.21|
|2024-09-04|0         |100941.21|0.0    |100941.21|
|2024-09-05|0         |100941.21|0.0    |100941.21|
|2024-09-06|0         |100941.21|0.0    |100941.21|
|2024-09-09|0         |100941.21|0.0    |100941.21|
|2024-09-10|0         |100941.21|0.0    |100941.21|
|2024-09-11|0         |100941.21|0.0    |100941.21|
|2024-09-12|0         |100941.21|0.0    |100941.21|
|2024-09-13|0         |100941.21|0.0    |100941.21|
|2024-09-16|0         |100941.21|0.0    |100941.21|
|2024-09-17|0         |100941.21|0.0    |100941.21|
|2024-09-18|0         |100941.21|0.0    |100941.21|
|2024-09-19|100       |43843.21|57098.0|100941.21|
|2024-09-20|100       |43843.21|56825.0|100668.21|
|2024-09-23|100       |43843.21|56967.0|100810.21|
|2024-09-24|100       |43843.21|57130.0|100973.21|
|2024-09-25|100       |43843.21|57004.0|100847.21|
|2024-09-26|100       |43843.21|57230.0|101073.21|
|2024-09-27|100       |43843.21|57147.0|100990.21|
|2024-09-30|100       |43843.21|57376.0|101219.21|
|2024-10-01|100       |43843.21|56862.0|100705.21|
|2024-10-02|100       |43843.21|56886.0|100729.21|
|2024-10-03|0         |100625.21|0.0    |100625.21|
|2024-10-04|0         |100625.21|0.0    |100625.21|
|2024-10-07|0         |100625.21|0.0    |100625.21|
|2024-10-08|0         |100625.21|0.0    |100625.21|
|2024-10-09|100       |42911.21|57714.0|100625.21|
|2024-10-10|100       |42911.21|57613.0|100524.21|
|2024-10-11|100       |42911.21|57958.0|100869.21|
|2024-10-14|100       |42911.21|58432.0|101343.21|
|2024-10-15|100       |42911.21|57978.0|100889.21|
|2024-10-16|100       |42911.21|58230.0|101141.21|
|2024-10-17|100       |42911.21|58235.0|101146.21|
|2024-10-18|100       |42911.21|58459.0|101370.21|
|2024-10-21|100       |42911.21|58363.0|101274.21|
|2024-10-22|100       |42911.21|58332.0|101243.21|
|2024-10-23|0         |100710.21|0.0    |100710.21|
|2024-10-24|0         |100710.21|0.0    |100710.21|
|2024-10-25|0         |100710.21|0.0    |100710.21|
|2024-10-28|0         |100710.21|0.0    |100710.21|
|2024-10-29|0         |100710.21|0.0    |100710.21|
|2024-10-30|0         |100710.21|0.0    |100710.21|
|2024-10-31|0         |100710.21|0.0    |100710.21|
|2024-11-01|0         |100710.21|0.0    |100710.21|
|2024-11-04|0         |100710.21|0.0    |100710.21|
|2024-11-05|0         |100710.21|0.0    |100710.21|
|2024-11-06|100       |41606.21|59104.0|100710.21|
|2024-11-07|100       |41606.21|59561.0|101167.21|
|2024-11-08|100       |41606.21|59819.0|101425.21|
|2024-11-11|100       |41606.21|59876.0|101482.21|
|2024-11-12|100       |41606.21|59690.0|101296.21|
|2024-11-13|100       |41606.21|59719.0|101325.21|
|2024-11-14|100       |41606.21|59335.0|100941.21|
|2024-11-15|0         |100084.57|0.0    |100084.57|
|2024-11-18|0         |100084.57|0.0    |100084.57|
|2024-11-19|0         |100084.57|0.0    |100084.57|
|2024-11-20|0         |100084.57|0.0    |100084.57|
|2024-11-21|0         |100084.57|0.0    |100084.57|
|2024-11-22|0         |100084.57|0.0    |100084.57|
|2024-11-25|0         |100084.57|0.0    |100084.57|
|2024-11-26|0         |100084.57|0.0    |100084.57|
|2024-11-27|0         |100084.57|0.0    |100084.57|
|2024-11-29|100       |39829.57|60255.0|100084.57|
|2024-12-02|100       |39829.57|60363.0|100192.57|
|2024-12-03|100       |39829.57|60391.0|100220.57|
|2024-12-04|100       |39829.57|60766.0|100595.57|
|2024-12-05|100       |39829.57|60666.0|100495.57|
|2024-12-06|100       |39829.57|60781.0|100610.57|
|2024-12-09|100       |39829.57|60468.0|100297.57|
|2024-12-10|100       |39829.57|60280.0|100109.57|
|2024-12-11|100       |39829.57|60746.0|100575.57|
|2024-12-12|100       |39829.57|60433.0|100262.57|
|2024-12-13|0         |100250.57|0.0    |100250.57|
|2024-12-16|0         |100250.57|0.0    |100250.57|
|2024-12-17|0         |100250.57|0.0    |100250.57|
|2024-12-18|0         |100250.57|0.0    |100250.57|
|2024-12-19|0         |100250.57|0.0    |100250.57|
|2024-12-20|0         |100250.57|0.0    |100250.57|
|2024-12-23|0         |100250.57|0.0    |100250.57|
|2024-12-24|0         |100250.57|0.0    |100250.57|
|2024-12-26|0         |100250.57|0.0    |100250.57|
|2024-12-27|0         |100250.57|0.0    |100250.57|
|2024-12-30|0         |100250.57|0.0    |100250.57|
|2024-12-31|0         |100250.57|0.0    |100250.57|
|2025-01-02|0         |100250.57|0.0    |100250.57|
|2025-01-03|0         |100250.57|0.0    |100250.57|
|2025-01-06|0         |100250.57|0.0    |100250.57|
|2025-01-07|0         |100250.57|0.0    |100250.57|
|2025-01-08|0         |100250.57|0.0    |100250.57|
|2025-01-10|0         |100250.57|0.0    |100250.57|
|2025-01-13|0         |100250.57|0.0    |100250.57|
|2025-01-14|0         |100250.57|0.0    |100250.57|
|2025-01-15|0         |100250.57|0.0    |100250.57|
|2025-01-16|0         |100250.57|0.0    |100250.57|
|2025-01-17|0         |100250.57|0.0    |100250.57|
|2025-01-21|0         |100250.57|0.0    |100250.57|
|2025-01-22|100       |39606.57|60644.0|100250.57|
|2025-01-23|100       |39606.57|60975.0|100581.57|
|2025-01-24|100       |39606.57|60797.0|100403.57|
|2025-01-27|0         |99493.14|0.0    |99493.14|
|2025-01-28|0         |99493.14|0.0    |99493.14|
|2025-01-29|0         |99493.14|0.0    |99493.14|
|2025-01-30|0         |99493.14|0.0    |99493.14|
|2025-01-31|0         |99493.14|0.0    |99493.14|
|2025-02-03|0         |99493.14|0.0    |99493.14|
|2025-02-04|0         |99493.14|0.0    |99493.14|
|2025-02-05|0         |99493.14|0.0    |99493.14|
|2025-02-06|0         |99493.14|0.0    |99493.14|
|2025-02-07|0         |99493.14|0.0    |99493.14|
|2025-02-10|0         |99493.14|0.0    |99493.14|
|2025-02-11|0         |99493.14|0.0    |99493.14|
|2025-02-12|0         |99493.14|0.0    |99493.14|
|2025-02-13|0         |99493.14|0.0    |99493.14|
|2025-02-14|0         |99493.14|0.0    |99493.14|
|2025-02-18|100       |38344.14|61149.0|99493.14|
|2025-02-19|100       |38344.14|61293.0|99637.14|
|2025-02-20|100       |38344.14|61038.0|99382.14|
|2025-02-21|0         |98915.43|0.0    |98915.43|
|2025-02-24|0         |98915.43|0.0    |98915.43|
|2025-02-25|0         |98915.43|0.0    |98915.43|
|2025-02-26|0         |98915.43|0.0    |98915.43|
|2025-02-27|0         |98915.43|0.0    |98915.43|
|2025-02-28|0         |98915.43|0.0    |98915.43|
|2025-03-03|0         |98915.43|0.0    |98915.43|
|2025-03-04|0         |98915.43|0.0    |98915.43|
|2025-03-05|0         |98915.43|0.0    |98915.43|
|2025-03-06|0         |98915.43|0.0    |98915.43|
|2025-03-07|0         |98915.43|0.0    |98915.43|
|2025-03-10|0         |98915.43|0.0    |98915.43|
|2025-03-11|0         |98915.43|0.0    |98915.43|
|2025-03-12|0         |98915.43|0.0    |98915.43|
|2025-03-13|0         |98915.43|0.0    |98915.43|
|2025-03-14|0         |98915.43|0.0    |98915.43|
|2025-03-17|0         |98915.43|0.0    |98915.43|
|2025-03-18|0         |98915.43|0.0    |98915.43|
|2025-03-19|0         |98915.43|0.0    |98915.43|
|2025-03-20|0         |98915.43|0.0    |98915.43|
|2025-03-21|0         |98915.43|0.0    |98915.43|
|2025-03-24|0         |98915.43|0.0    |98915.43|
|2025-03-25|0         |98915.43|0.0    |98915.43|
|2025-03-26|0         |98915.43|0.0    |98915.43|


* [Download Daily Ledger CSV](./data/ledger.csv)


## Trade Outcome Analysis
Every backtested trade concludes in one of three ways: Target Hit, Stop Loss, or Timeout. The logic for these outcomes is strictly defined: a trade is stopped out for a managed loss if the price drops 1.0x ATR below the entry price. If the trade fails to hit the profit target or the stop loss within a set timeout period of 10 trading days, a time-stop is triggered, and the position is automatically closed at the current market price. Tracking the distribution of these outcomes is critical for evaluating whether the profit target is too ambitious or the stop loss is too tight.

<iframe src="./data/outcome_histogram.html" width="100%" height="500px" frameborder="0"></iframe>

## Performance Metrics
The table below outlines the backtested performance of the strategy.

| Metric | Value |
| :--- | :--- |
| Total Trades | 13 |
| Win Rate | 46.15% |
| Average Return per Trade | -0.12% |
| Sharpe Ratio (RFR 0.0375) | -1.5319 |
| Sortino Ratio | -1.2558 |
| Max Drawdown | -3.52% |
| Profit Factor | 0.77 |
| Expectancy (Per Trade) | -0.0012 |

**Metric Interpretations:**
* **Average Return per Trade:** Indicates the mean percentage gain or loss across all executed trades. A negative value here highlights that the costs of the false breakouts outweighed the momentum captured by the successful ones.
* **Sharpe & Sortino Ratios:** The Sharpe ratio evaluates the risk-adjusted return against a 3.75% risk-free rate. A negative Sharpe ratio indicates the strategy underperformed cash. The Sortino ratio serves a similar function but only penalizes downside volatility, providing a clearer picture of drawdowns. 
* **Max Drawdown:** Measures the largest peak-to-trough drop in portfolio value. This quantifies the worst-case capital erosion experienced during the backtest.
* **Profit Factor & Expectancy:** The profit factor divides gross profits by gross losses. A value below 1.0 indicates a losing system. Expectancy combines the win rate and average win/loss sizes to project the mathematical expected return of taking one additional trade under this system.

<iframe src="./data/equity_curve.html" width="100%" height="600px" frameborder="0"></iframe>

## Conclusion & Regime Change Analysis

Reviewing the equity curve, the strategy performed consistently well through the first half of the backtest, accumulating positive returns until peaking in July 2024. Following this high-water mark, the portfolio entered a sustained drawdown. The accumulated profits steadily eroded, and the Net Asset Value (NAV) ultimately crossed into negative territory (falling below the $100,000 initial balance) near the end of the testing window in February 2025.

This distinct pivot from profitability to persistent losses strongly suggests a market regime change rather than a random cluster of unsuccessful trades. ATR-based breakout strategies rely heavily on environments characterized by persistent directional momentum and low-to-moderate volatility. When the broader market transitions from a trending regime to a mean-reverting or highly volatile regime, breakout signals frequently fail, leading to repeated stop-outs. 

I hypothesize that this transition was driven by a few specific structural shifts in the SPY market environment during late 2024 and early 2025:

* **Volatility Expansion and Whipsawing:** An increase in baseline market volatility often causes prices to spike above the 20-day high (initiating the long position) only to immediately retrace. In a wider volatility environment, the daily price fluctuations easily hit the relatively tight 1.0x ATR stop-loss before the required momentum can establish itself.
* **Macroeconomic Policy Catalysts:** The fall of 2024 contained significant shifts in central bank interest rate expectations alongside general election uncertainty. These macro events tend to disrupt sustained directional capital flows, replacing them with choppy, sideways price action as institutional capital continuously re-prices risk.
* **Internal Sector Rotation:** If capital began rotating rapidly between different sectors (e.g., shifting out of technology and into defensive stocks) rather than flowing uniformly into the market, SPY would lack the unified participation required to sustain index-level breakouts. This results in false breakouts that lack the follow-through necessary to reach the 2.0x ATR profit target. 

Ultimately, this performance degradation highlights the limitations of deploying a static breakout model across varying market conditions. A logical next step for future iterations would be implementing a regime filter (such as a broader moving average crossover or a volatility index threshold) to dynamically turn the strategy off when the market transitions out of a trending state.