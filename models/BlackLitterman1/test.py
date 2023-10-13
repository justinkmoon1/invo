from pypfopt import black_litterman
from pypfopt import risk_models
from pypfopt import plotting
from pypfopt import objective_functions
from pypfopt.black_litterman import BlackLittermanModel
from pypfopt.efficient_frontier import EfficientFrontier
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import yfinance as yf
import os
if not os.path.isdir('data'):
    os.system('git clone https://github.com/robertmartin8/PyPortfolioOpt.git')
    os.chdir('PyPortfolioOpt/cookbook')

#stock prices- change company (may not be needed at all after LSTM)
tickers = ["MSFT", "AMZN", "NAT", "BAC", "DPZ", "DIS", "KO", "MCD", "COST", "SBUX"]
ohlc = yf.download(tickers, period="max")
prices = ohlc["Adj Close"]
prices.tail()

#how to decide market price?
market_prices = yf.download("SPY", period="max")["Adj Close"]
market_prices.head()
mcaps = {}
for t in tickers:
    stock = yf.Ticker(t)
    mcaps[t] = stock.info["marketCap"]
mcaps

#construct prior
S = risk_models.CovarianceShrinkage(prices).ledoit_wolf()
delta = black_litterman.market_implied_risk_aversion(market_prices)
plotting.plot_covariance(S, plot_correlation=True)
market_prior = black_litterman.market_implied_prior_returns(mcaps, delta, S)
market_prior
market_prior.plot.barh(figsize=(10,5))

viewdict = {
    "AMZN": 0.10,
    "BAC": 0.30,
    "COST": 0.05,
    "DIS": 0.05,
    "DPZ": 0.20,
    "KO": -0.05,  # I think Coca-Cola will go down 5%
    "MCD": 0.15,
    "MSFT": 0.10,
    "NAT": 0.50,  # but low confidence, which will be reflected later
    "SBUX": 0.10
}
bl = BlackLittermanModel(S, pi=market_prior, absolute_views=viewdict)

#view confidences
confidences = [
    0.6,
    0.4,
    0.2,
    0.5,
    0.7, # confident in dominos
    0.7, # confident KO will do poorly
    0.7, 
    0.5,
    0.1,
    0.4
]
bl = BlackLittermanModel(S, pi=market_prior, absolute_views=viewdict, omega="idzorek", view_confidences=confidences)
fig, ax = plt.subplots(figsize=(7,7))
im = ax.imshow(bl.omega)

ax.set_xticks(np.arange(len(bl.tickers)))
ax.set_yticks(np.arange(len(bl.tickers)))

ax.set_xticklabels(bl.tickers)
ax.set_yticklabels(bl.tickers)
plt.show()

np.diag(bl.omega)


#automatic market-implied prior (use LSTM module returns)
bl = BlackLittermanModel(S, pi="market", market_caps=mcaps, risk_aversion=delta,
                        absolute_views=viewdict, omega= "idzorek", view_confidences=confidences)
# Posterior estimate of returns
ret_bl = bl.bl_returns()
ret_bl
#comparison to prior / views
rets_df = pd.DataFrame([market_prior, ret_bl, pd.Series(viewdict)], 
             index=["Prior", "Posterior", "Views"]).T
rets_df
rets_df.plot.bar(figsize=(12,8))
#posterior covarience estimate
S_bl = bl.bl_cov()
plotting.plot_covariance(S_bl)


ef = EfficientFrontier(ret_bl, S_bl)
ef.add_objective(objective_functions.L2_reg)
ef.max_sharpe()
weights = ef.clean_weights()
weights

pd.Series(weights).plot.pie(figsize=(10,10))


from pypfopt import DiscreteAllocation

da = DiscreteAllocation(weights, prices.iloc[-1], total_portfolio_value=20000)
alloc, leftover = da.lp_portfolio()
print(f"Leftover: ${leftover:.2f}")
print(alloc)