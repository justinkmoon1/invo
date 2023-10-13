
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import yfinance as yf
import pypfopt
from pypfopt import black_litterman, risk_models
from pypfopt import BlackLittermanModel, plotting

from pypfopt import EfficientFrontier, objective_functions



import os

# Check if 'data' directory exists, and clone the data if not.
if not os.path.isdir('data'):
    os.system('git clone https://github.com/robertmartin8/PyPortfolioOpt.git')
    os.chdir('PyPortfolioOpt/cookbook')

# Stock tickers - change these as needed.
tickers = ["MSFT", "AMZN", "NAT", "BAC", "DPZ", "DIS", "KO", "MCD", "COST", "SBUX"]

# Download historical stock prices.
ohlc = yf.download(tickers, period="max")
prices = ohlc["Adj Close"]
print(prices.tail())

# How to decide market price? Download historical data for a market index.
market_prices = yf.download("MSCI", period="max")["Adj Close"]
print(market_prices.head())
# Get market capitalizations for tickers.
mcaps = {}
for t in tickers:
    stock = yf.Ticker(t)
    mcaps[t] = stock.info["marketCap"]
print(mcaps)

print(pypfopt.__version__)
# Construct prior using the risk model.
S = risk_models.CovarianceShrinkage(prices).ledoit_wolf()
delta = black_litterman.market_implied_risk_aversion(market_prices)
print(delta)

plotting.plot_covariance(S, plot_correlation=True);
plt.show() #visualization of the covariaence matrix

market_prior = black_litterman.market_implied_prior_returns(mcaps, delta, S)
print(market_prior)


market_prior.plot.barh(figsize=(10, 5));
plt.show() #estimated expected returns for different assets
#replace with LSTM???

# Define your views on assets.
viewdict = {
    "AMZN": 0.50, #10% return
    "BAC": 0.20, 
    "COST": 0.05,
    "DIS": 0.05,
    "DPZ": 0.20,
    "KO": -0.05, #-5% return
    "MCD": 0.15,
    "MSFT": 0.10,
    "NAT": 0.50,
    "SBUX": 0.10
}
bl = BlackLittermanModel(S, pi=market_prior, absolute_views=viewdict)
# Define view confidences as proportions (between 0 and 1).
confidences = [0.6, 0.4, 0.2, 0.5, 0.7, 0.7, 0.7, 0.5, 0.1, 0.4]

# Create the Black-Litterman model with views and confidences.
bl = BlackLittermanModel(S, pi=market_prior, absolute_views=viewdict, omega="idzorek", view_confidences=confidences)

# Visualize the omega matrix.
fig, ax = plt.subplots(figsize=(7, 7));
im = ax.imshow(bl.omega)

ax.set_xticks(np.arange(len(bl.tickers)))
ax.set_yticks(np.arange(len(bl.tickers)))

ax.set_xticklabels(bl.tickers)
ax.set_yticklabels(bl.tickers)
plt.show()

# Extract the diagonal of the omega matrix.
print(np.diag(bl.omega))

intervals = [
    (0, 0),
    (0, 0),
    (0, 0),
    (0, 0),
    (0, 0),
    (0, 0),
    (0, 0),
    (0, 0),
    (0, 0),
    (0, 0),
    (0, 0),
    (0, 0),
    (0, 0)
]

variances = []
for lb, ub in intervals:
    sigma = (ub - lb)/2
    variances.append(sigma ** 2)

print(variances)
omega = np.diag(variances)



# Automatic market-implied prior (use LSTM module returns).
bl = BlackLittermanModel(S, pi="market", market_caps=mcaps, risk_aversion=delta,
                        absolute_views=viewdict, omega= "idzorek", view_confidences=confidences)

# Posterior estimate of returns.
ret_bl = bl.bl_returns()
print(ret_bl)

# Comparison to prior/views.
rets_df = pd.DataFrame([market_prior, ret_bl, pd.Series(viewdict)],
                       index=["Prior", "Posterior", "Views"]).T
print(rets_df)
rets_df.plot.bar(figsize=(12, 8));
plt.show()
# Posterior covariance estimate.
S_bl = bl.bl_cov()
plotting.plot_covariance(S_bl)
plt.show()

# Optimize the portfolio using the Black-Litterman expected returns and covariance.
ef = EfficientFrontier(ret_bl, S_bl)
ef.add_objective(objective_functions.L2_reg)
ef.max_sharpe()
weights = ef.clean_weights()
print(weights)

# Visualize the portfolio weights as a pie chart.
pd.Series(weights).plot.pie(figsize=(10, 10));
plt.show()
# Perform discrete allocation based on the optimized weights.
from pypfopt import DiscreteAllocation

da = DiscreteAllocation(weights, prices.iloc[-1], total_portfolio_value=60000)
alloc, leftover = da.lp_portfolio()
print(f"Leftover: ${leftover:.2f}")
print(alloc)