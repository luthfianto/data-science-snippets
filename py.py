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

def get_regression_summary(lm, X, y, feature_names=None):
  params = np.append(lm.intercept_,lm.coef_)
  predictions = lm.predict(X)

  newX = pd.DataFrame({"Constant":np.ones(len(X))}).join(pd.DataFrame(X))
  MSE = (sum((y-predictions)**2))/(len(newX)-len(newX.columns))

  # Note if you don't want to use a DataFrame replace the two lines above with
  # newX = np.append(np.ones((len(X),1)), X, axis=1)
  # MSE = (sum((y-predictions)**2))/(len(newX)-len(newX[0]))

  var_b = MSE*(np.linalg.inv(np.dot(newX.T,newX)).diagonal())
  sd_b = np.sqrt(var_b)
  ts_b = params/ sd_b

  p_values = [2 * (1 - stats.t.cdf(np.abs(i), (len(newX) - len(newX.columns)))) for i in ts_b]

  sd_b = np.round(sd_b,3)
  ts_b = np.round(ts_b,3)
  p_values = np.round(p_values,3)
  params = np.round(params,4)

  myDF3 = pd.DataFrame()
  # feature_names.insert(0, "Intercept")
  myDF3["Name"],myDF3["Coefficients"],myDF3["Standard Errors"],myDF3["t values"],myDF3["pvalue"] = [feature_names, params,sd_b,ts_b,p_values]
  return (myDF3.sort_values("Coefficients", key=abs, ascending=False).reset_index(drop=True))
