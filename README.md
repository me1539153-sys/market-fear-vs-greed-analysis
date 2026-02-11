# market-fear-vs-greed-analysis
**To View Project Output Visit:-** http://localhost:8501/
This project analyzes the relationship between market sentiment (Fear vs Greed) and trader behavior and performance on the Hyperliquid trading platform. The objective is to understand whether overall market psychology influences how traders act (trade frequency, position bias, trade size) and how well they perform in terms of realized profit and loss (PnL).

Two datasets are used: a daily Bitcoin Fear & Greed Index, representing market sentiment, and historical trade-level data from Hyperliquid, containing information such as trader account, trade size, side (buy/sell), timestamp, and realized PnL. Trade timestamps are converted from Unix epoch format and aligned with sentiment data at a daily level.

Key behavioral and performance metrics are derived at the trader-day level, including daily PnL, number of trades per day, average trade size, long/short ratio, and win rate. Comparative analysis is then performed to evaluate differences in trader behavior and performance during Fear versus Greed market conditions. Traders are also segmented based on observable behavior patterns such as trading frequency.

As a bonus, a simple logistic regression model is implemented to predict whether a trader will have a profitable day using sentiment and behavioral features. The project concludes with actionable strategy recommendations that translate analytical insights into practical trading rules.
