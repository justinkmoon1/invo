import PyValuation as pv


stock1 = pv.DCF('AAPL')

print(stock1.projected_cashflows())