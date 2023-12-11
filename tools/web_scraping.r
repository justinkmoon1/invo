require("rvest")

ticker = "AAPL"

getFin = function(ticker)
{
  url = paste0("https://finance.yahoo.com/quote/", AAPL, "/key-statistics?p=", ticker)

  a <- read_html(url)
  
  print(a)
  }