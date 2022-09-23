from statsmodels.stats.outliers_influence import variance_inflation_factor
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def df_summarier(df, percentiles=[0.25, 0.5, 0.75]) -> pd.DataFrame:
    a = df.isna().any(axis=0)
    notnan = df.count()
    b = df.dtypes
    c = df.nunique()
    d = pd.Series({col: df[col].unique() for col in df})
    print("df.shape", df.shape)
    # print("df.created_time.min()", df.created_time.min(), "df.created_time.max()", df.created_time.max(), )
    print("df summary")
    return pd.concat(
        [a, notnan, b, c, d, df.describe(percentiles=percentiles).T], axis=1
    ).rename(
        columns={
            0: "has nan?",
            1: "num of notnan",
            2: "dtypes",
            3: "num of unique values",
            4: "list of unique values",
        }
    )


def get_vif(xtrain):  

  # VIF dataframe
  vif_data = pd.DataFrame()
  vif_data["feature"] = xtrain.columns
    
  # calculating VIF for each feature
  vif_data["VIF"] = [variance_inflation_factor(xtrain.values, i)
                            for i in range(len(xtrain.columns))]
    
  return (vif_data)
