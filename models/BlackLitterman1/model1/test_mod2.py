
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


cur_dir = "models/BlackLitterman1/res/" + datetime.datetime.now().strftime('%Y-%m-%d')

prefix = datetime.datetime.now().strftime('%Y-%m-%d')
try:
    os.mkdir(cur_dir)
except:
    pass


t0 = "daily"
t1 = "weekly"
t2 = "quarter"
t = t0

# Check if 'data' directory exists, and clone the data if not.
if not os.path.isdir('data'):
    os.system('git clone https://github.com/robertmartin8/PyPortfolioOpt.git')
    os.chdir('PyPortfolioOpt/cookbook')

# Stock tickers - change these as needed.
tickers = ["PAVE", "INDA", "SMH", "VGT"]

# Download historical stock prices.
ohlc = yf.download(tickers, period="max")
prices = ohlc["Adj Close"]
print(prices.tail())

# How to decide market price? Download historical data for a market index.
market_prices = yf.download("MSCI", period="max")["Adj Close"]
print(market_prices.head())
# Get market capitalizations for tickers.
mcaps = {}
for a in tickers:
    stock = yf.Ticker(a)
    mcaps[a] = stock.get_info()["totalAssets"]
print(mcaps)

print(pypfopt.__version__)
# Construct prior using the risk model.
S = risk_models.CovarianceShrinkage(prices).ledoit_wolf()
delta = black_litterman.market_implied_risk_aversion(market_prices)
print(delta)

plotting.plot_covariance(S, plot_correlation=True);
plt.savefig(cur_dir + "/" + t + "ETFcovariance.png")
#plt.show() #visualization of the covariaence matrix

market_prior = black_litterman.market_implied_prior_returns(mcaps, delta, S)
print(market_prior)


market_prior.plot.barh(figsize=(10, 5));
plt.savefig(cur_dir + "/" + t + "ETFmarket_prior.png")
#plt.show() #estimated expected returns for different assets
#replace with LSTM???
df = pd.read_excel(f"models/LSTM/data/predictions/{prefix}.xlsx")
df = df.set_index("Ticker")
# Define your views on assets.

viewdict = {
    "PAVE": df[f"{t}_increase"].loc["PAVE"],
    "INDA": df[f"{t}_increase"].loc["INDA"],
    "SMH": df[f"{t}_increase"].loc["SMH"],
    "VGT": df[f"{t}_increase"].loc["VGT"],
}
print(f"viewdict: {viewdict}")
bl = BlackLittermanModel(S, pi=market_prior, absolute_views=viewdict)
# Define view confidences as proportions (between 0 and 1).
confidences = [1, 1, 1, 1]

# Create the Black-Litterman model with views and confidences.
bl = BlackLittermanModel(S, pi=market_prior, absolute_views=viewdict, omega="idzorek", view_confidences=confidences)

# Visualize the omega matrix.
fig, ax = plt.subplots(figsize=(7, 7));
im = ax.imshow(bl.omega)

ax.set_xticks(np.arange(len(bl.tickers)))
ax.set_yticks(np.arange(len(bl.tickers)))

ax.set_xticklabels(bl.tickers)
ax.set_yticklabels(bl.tickers)
plt.savefig(cur_dir + "/" + t + "omegaETF.png")
#plt.show()

# Extract the diagonal of the omega matrix.
print(np.diag(bl.omega))

intervals = [
    (0.05, 0.15),
    (0.05, 0.15),
    (0.05, 0.15),
    (0.05, 0.15),
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
plt.savefig(cur_dir + "/" + t + "ETFreturns.png")
# Posterior covariance estimate.
S_bl = bl.bl_cov()
plotting.plot_covariance(S_bl)
plt.savefig(cur_dir + "/" + t + "ETFposterior_covariance.png")
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
plt.savefig(cur_dir + "/" + t + "ETFresults.png")
# Perform discrete allocation based on the optimized weights.
from pypfopt import DiscreteAllocation

da = DiscreteAllocation(weights, prices.iloc[-1], total_portfolio_value=30000)
alloc, leftover = da.lp_portfolio()
print(f"Leftover: ${leftover:.2f}")
print(alloc)
pd.DataFrame(alloc, index = [0]).to_excel(cur_dir + "/" + t + "_ETF_result.xlsx")