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
    
    def add_entities(df,name=None):
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

    def add_carbon_policy(df,name=None):
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

    def standardize_numeric_by_state(df,name=None):
      df_mean = df.groupby(by='State').mean().reset_index()
      df_std = df.groupby(by='State').std().reset_index()
      if name is None:
        col_to_loop_through = list(df.columns)
      else:
        col_to_loop_through = [name]
      for col in col_to_loop_through:
        if is_numeric_dtype(df[col]):
          df_mean['Mean '+str(col)] = df_mean[col]
          df_std['Std '+str(col)] = df_std[col]
          df_merged = pd.merge(df, df_mean[['State','Mean '+str(col)]],on='State')
          df_merged = pd.merge(df_merged, df_std[['State','Std '+str(col)]],on='State')
          df[str(col)+'_state'] = (df_merged[col]-df_merged['Mean '+str(col)])/df_merged['Std '+str(col)]
          del df[col]
      return df

    def standardize_numeric_by_nation(df,name=None):
      if name is None:
        col_to_loop_through = list(df.columns)
      else:
        col_to_loop_through = [name]
      for col in col_to_loop_through:
        if is_numeric_dtype(df[col]):
          df[str(col)+'_stand'] = (df[col] - df[col].mean())/df[col].std()
          del df[col]
      return df

    def one_hot_encode(df,col,name=None):
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

    def average_weather_columns(df,string_term,or_terms, weights=None, new_name = None):
      # string term - a term that must be matched in column names
      # or_terms - a list of terms that can be tacked onto the end of the string term to complete the column names of interest ex. string_term = 'Average ' and or_terms = [1,2,3] would look at columns ['Averag 1','Average 2','Average 3']
      # weights - defaults to None so that equal weights are given, but if you wanted unequal weights - like giving month of July more weight than june or august, these weights could be passed
      cols_to_average = []
      for t in or_terms:
        cols_to_average.append(str(string_term)+str(t))
      if new_name is None:
        new_name = ''
        for s in string_terms:
          new_name += s
        for t in or_terms:
          new_name += str(t)
      if weights is None:
        weights = [1]*len(cols_to_average)
      if len(weights) != len(cols_to_average):
        raise ValueError("weights argument must be same length as 'or_terms'. There are {} columns and the weights passed in are length {}.\n{}".format(len(cols_to_average),len(weights),cols_to_average))
      df[new_name] =  [0]*df.shape[0]
      for i, col in enumerate(cols_to_average):
        df[new_name] = df[new_name] + df[col]*weights[i]
        del df[col]
      df[new_name] = df[new_name]/sum(weights)
      return df
