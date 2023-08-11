df = pd.DataFrame()

temp_df = nasdaq_df[nasdaq_df['Market Cap']>100000000]
for index, row in temp_df.iloc[:20, ].iterrows():
    ticker_start_time = time.time()
    symbol = row['Symbol']
    ticker = yf.Ticker(symbol)
    raw_info = ticker.info
    try:
        if raw_info['quoteType'] == 'EQUITY':  # ETF를 제외한 개별 종목
            inner_dict = {}

            # 기본 정보 추가
            inner_dict['symbol'] = row['Symbol']
            inner_dict['name'] = row['Name']
            inner_dict['country'] = row['Country']
            inner_dict['origin_sector'] = row['Sector']
            inner_dict['industry'] = row['Industry']

            # info 정보 추가
            for info_column in info_columns_mapper:
                value = raw_info[info_column]
                inner_dict[info_columns_mapper[info_column]] = value

            # ticker.financials : 직전 4년 매출관련 데이터 추가
            financial_dict = ticker.financials.T.to_dict('list')
            for financial_column in financial_columns_mapper:
                value_list = list(reversed(financial_dict[financial_column]))
                inner_dict["list_financial_" + financial_columns_mapper[financial_column]] = value_list

            # ticker.balance_sheet : 직전 4년 재무상태 데이터 추가
            balance_sheet_dict = ticker.balance_sheet.T.to_dict('list')
            for balance_sheet_column in balance_sheet_columns_mapper:
                value_list = list(reversed(balance_sheet_dict[balance_sheet_column]))
                inner_dict["list_balancesheet_" + balance_sheet_columns_mapper[balance_sheet_column]] = value_list

            # append to df
            df = df.append(inner_dict, ignore_index=True)
            
            # time check
            print(symbol)
            print("--- %s seconds ---" % (time.time() - total_start_time))
    except Exception as e:
        print(symbol, 'Error:', e)