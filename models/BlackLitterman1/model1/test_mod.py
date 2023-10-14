
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import yfinance as yf
import pypfopt
from pypfopt import black_litterman, risk_models
from pypfopt import BlackLittermanModel, plotting

from pypfopt import EfficientFrontier, objective_functions
import datetime
import os


cur_dir = "models/BlackLitterman1/res/" + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

os.mkdir(cur_dir)

# Check if 'data' directory exists, and clone the data if not.
if not os.path.isdir('data'):
    os.system('git clone https://github.com/robertmartin8/PyPortfolioOpt.git')
    os.chdir('PyPortfolioOpt/cookbook')

# Stock tickers - change these as needed.
tickers = ["GM", "HMC", "AAL", "PCAR", "CYD", "DAL", "GMAB", "GILD", "SEIC", "APAM", "BEN", "BBSEY"]

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
plt.savefig(cur_dir + "/" + "covariance.png")
#plt.show() #visualization of the covariaence matrix

market_prior = black_litterman.market_implied_prior_returns(mcaps, delta, S)
print(market_prior)


market_prior.plot.barh(figsize=(10, 5));
plt.savefig(cur_dir + "/" + "market_prior.png")
#plt.show() #estimated expected returns for different assets
#replace with LSTM???
df = pd.read_excel(f"models/LSTM/data/predictions/{datetime.datetime}.xlsx")
# Define your views on assets.
viewdict = {
    "GM": 0.06,
    "HMC": -0.01,
    "AAL": 0.34,
    "PCAR": 0.02,
    "CYD": 0.38,
    "DAL": 0.25,
    "GMAB": 0.16,
    "GILD": 0.04,
    "SEIC": 0.02,
    "APAM": 0.07,
    "BEN": 0.22,
    "LAZ": 0.15,
    "BBSEY": 0.21
}
bl = BlackLittermanModel(S, pi=market_prior, absolute_views=viewdict)
# Define view confidences as proportions (between 0 and 1).
confidences = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

# Create the Black-Litterman model with views and confidences.
bl = BlackLittermanModel(S, pi=market_prior, absolute_views=viewdict, omega="idzorek", view_confidences=confidences)

# Visualize the omega matrix.
fig, ax = plt.subplots(figsize=(7, 7));
im = ax.imshow(bl.omega)

ax.set_xticks(np.arange(len(bl.tickers)))
ax.set_yticks(np.arange(len(bl.tickers)))

ax.set_xticklabels(bl.tickers)
ax.set_yticklabels(bl.tickers)
plt.savefig(cur_dir + "/" + "omega.png")
#plt.show()

# Extract the diagonal of the omega matrix.
print(np.diag(bl.omega))

intervals = [
    (0.05, 0.15),
    (0.05, 0.15),
    (0.05, 0.15),
    (0.05, 0.15),
    (0.05, 0.15),
    (0.05, 0.15),
    (0.05, 0.15),
    (0.05, 0.15),
    (0.05, 0.15),
    (0.05, 0.15),
    (0.05, 0.15),
    (0.05, 0.15),
    (0.05, 0.15)
]

variances = []
for lb, ub in intervals:
    sigma = (ub - lb)/2
    variances.append(sigma ** 2)

print(variances)
omega = np.diag(variances)



# Automatic market-implied prior (use LSTM module returns).
bl = BlackLittermanModel(S, pi="market", market_caps=mcaps, risk_aversion=delta,
                        absolute_views=viewdict, omega=omega)

# Posterior estimate of returns.
ret_bl = bl.bl_returns()
print(ret_bl)

# Comparison to prior/views.
rets_df = pd.DataFrame([market_prior, ret_bl, pd.Series(viewdict)],
                       index=["Prior", "Posterior", "Views"]).T
print(rets_df)
rets_df.plot.bar(figsize=(12, 8));
#plt.show()
plt.savefig(cur_dir + "/" + "returns.png")
# Posterior covariance estimate.
S_bl = bl.bl_cov()
plotting.plot_covariance(S_bl)
plt.savefig(cur_dir + "/" + "posterior_covariance.png")
#plt.show()

# Optimize the portfolio using the Black-Litterman expected returns and covariance.
ef = EfficientFrontier(ret_bl, S_bl)
ef.add_objective(objective_functions.L2_reg)
ef.max_sharpe()
weights = ef.clean_weights()
print(weights)

# Visualize the portfolio weights as a pie chart.
pd.Series(weights).plot.pie(figsize=(10, 10));
#plt.show()
plt.savefig(cur_dir + "/" + "results.png")
# Perform discrete allocation based on the optimized weights.
from pypfopt import DiscreteAllocation

da = DiscreteAllocation(weights, prices.iloc[-1], total_portfolio_value=60000)
alloc, leftover = da.lp_portfolio()
print(f"Leftover: ${leftover:.2f}")
print(alloc)