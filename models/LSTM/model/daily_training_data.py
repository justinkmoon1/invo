from final_data_query import get_data
import pandas as pd

for l in ["GM", "HMC", "AAL", "PCAR", "CYD", "DAL", "GMAB", "GILD", "SEIC", "APAM", "BEN", "BBSEY"]:
    get_data(l)