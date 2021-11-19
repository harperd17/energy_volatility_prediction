class Fengine:

    def outlier_thresh(df, threshold=3):

        threshold_amount = threshold * df["target_COV"].std()

        df["target_COV"] = df["target_COV"].mean()+threshold_amount

        df = df.rename(columns={"target_COV": {f"target_COV_OT_{threshold}"}})

        print("Outlier Threshold Applied:", threshold)

        #_ = df['target_COV'].hist(bins=100)

        df = df.query('target_COV < +str(outlier_thresh))

        #_ = df['target_COV'].pow(0.5).hist(bins=100)

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
