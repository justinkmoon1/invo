import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

import FinanceDataReader as fdr

class Macro():
    cpi_df = pd.DataFrame()
    gdp_df = pd.DataFrame()
    ffr_df = pd.DataFrame()

    def __init__(self, year):
        self.start = year


    def get_cpi(self, start):
        df_cpi = fdr.DataReader('FRED:CPIAUCSL', start = str(start))
        df_cpi = df_cpi.rename(columns={'CPIAUCSL': 'CPI Index'})
        return df_cpi

    def get_gdp(self, start):
        df_gdp = fdr.DataReader('FRED:GDP',start=str(start))
        return df_gdp

    def get_fedfundrate(self, start):
        df_ffr = fdr.DataReader('FRED:DFF', start = str(start))
        df_ffr = df_ffr.rename(columns={'DFF' : 'Fed Fund Rate'})
        return df_ffr

    def convert_m_to_d(self, df):
        start_date = df.index.min() - pd.DateOffset(day=1)
        end_date = df.index.max() + pd.DateOffset(day=31)
        dates = pd.date_range(start_date, end_date, freq='D')
        dates.name = 'date'
        dataframe = df.reindex(dates, method = 'ffill')
        return dataframe

    def get_complete_macro(self):
        cpi_df = self.get_cpi(self.start)
        gdp_df = self.get_gdp(self.start)
        ffr_df = self.get_fedfundrate(self.start)
        cpi_df = self.convert_m_to_d(cpi_df)
        gdp_df = self.convert_m_to_d(gdp_df)
        comp = pd.concat([cpi_df, gdp_df, ffr_df], axis=1)
        comp = comp.fillna(method='ffill')
        print(comp)
        return comp
    

    