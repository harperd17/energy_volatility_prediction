import pandas as pd
from pandas.api.types import is_numeric_dtype
from sklearn.preprocessing import OneHotEncoder

class Fengine:

    def outlier_thresh(df, threshold=3):

        _ = df['target_COV'].hist(bins=100)

        outlier_thresh = df['target_COV'].mean()+threshold*df['target_COV'].std()
        print("Outlier Threshold Applied:", outlier_thresh)

        df = df.query('target_COV < '+str(outlier_thresh))
        _ = df['target_COV'].pow(0.5).hist(bins=100)

        return df

    def col_startswith(df, startswith_criteria="R_"):

        df_change = df[[col for col in df.columns
                        if col.startswith(startswith_criteria)
                        and not col == "year.1"]]

        return df_change

    def col_endswith(df, endswith_criteria="R_"):

        df_change = df[[col for col in df.columns
                        if col.endswith(endswith_criteria)
                        and not col == "year.1"]]

        return df_change

    def col_not_startswith(df, startswith_criteria="R_"):

        df_change = df[[col for col in df.columns
                        if not col.startswith(startswith_criteria)
                        and not col == "year.1"]]

        return df_change

    def col_not_endswith(df, endswith_criteria="R_"):

        df_change = df[[col for col in df.columns
                        if not col.endswith(endswith_criteria)
                        and not col == "year.1"]]

        return df_change

    def solar_mwh_hot_months(df, column_name=""):

        df[column_name] = df['Hot Summer Months'] * df['Agg_R_Solar_MWh']

        return df
    
    def add_entities(df):
      # variable to show which region a state belongs to
      # https://www.nerc.com/AboutNERC/keyplayers/Pages/default.aspx
      WECC = ['WA','OR','CA','ID','NV','AZ','UT','MT','CO','WY','NM']
      df['WECC'] = df['State'].isin(WECC).astype(int)
      Texas_RE = ['TX']
      df['TX_RE'] = df['State'].isin(Texas_RE).astype(int)
      MRO = ['ND','SD','NE','KS','OK','MN','WI','IA']
      df['MRO'] = df['State'].isin(MRO).astype(int)
      RF = ['MI','IN','OH','WV','PA','NJ','DE','MD']
      df['RF'] = df['State'].isin(RF).astype(int)
      SERC = ['MO','AR','LA','IL','KY','TN','VA','NC','SC','GA','AL','MS','FL']
      df['SERC'] = df['State'].isin(SERC).astype(int)
      NPCC = ['NY','VT','NH','MA','CT','RI','ME']
      df['NPCC'] = df['State'].isin(NPCC).astype(int)
      return df

    def add_carbon_policy(df):
      # give states that have some sort of carbon policy a value of 1
      # variable to track whether states are part of a carbon pricing program - https://www.c2es.org/document/us-state-carbon-pricing-policies/
      CA_CAP = ['CA','WA']
      RGGI = ['ME','NH','VT','NY','MA','CT','RI','NJ','MD','DE','VA']
      MA_CAP = ['MA']
      #carbon_policy = ['WA','CA','ME','NH','VT','NY','MA','CT','RI','NJ','MD','DE','VA']
      #df['Carbon Policy'] = df['State'].isin(carbon_policy).astype(int)
      df['CA Cap'] = df['State'].isin(CA_CAP).astype(int)
      df['RGGI'] = df['State'].isin(RGGI).astype(int)
      df['MA Cap'] = df['State'].isin(MA_CAP).astype(int)
      return df

    def standardize_numeric_by_state(df):
      df_mean = df.groupby(by='State').mean().reset_index()
      df_std = df.groupby(by='State').std().reset_index()
      for col in df.columns:
        if is_numeric_dtype(df[col]):
          df_mean['Mean '+str(col)] = df_mean[col]
          df_std['Std '+str(col)] = df_std[col]
          df_merged = pd.merge(df, df_mean[['State','Mean '+str(col)]],on='State')
          df_merged = pd.merge(df_merged, df_std[['State','Std '+str(col)]],on='State')
          df[str(col)+'_state'] = (df_merged[col]-df_merged['Mean '+str(col)])/df_merged['Std '+str(col)]
          del df[col]
      return df

    def standardize_numeric_by_nation(df):
      for col in df.columns:
        if is_numeric_dtype(df[col]):
          df[str(col)+'_stand'] = (df[col] - df[col].mean())/df[col].std()
          del df[col]
      return df

    def one_hot_encode(df,col):
      encoder = OneHotEncoder(sparse=False)
      encoder.fit(np.array(df[col]).reshape(-1,1))
      encoded = encoder.transform(np.array(df[col]).reshape(-1,1))
      encoded_names = encoder.get_feature_names()
      new_names = []
      for name in encoded_names:
        if name[:3] == 'x0_':
          new_names.append(name[3:])
        else:
          new_names.append(col)
      df[new_names] = encoded
      del df[col]
      return df
