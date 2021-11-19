import sklearn
import numpy as np
import pandas as pd


class SklearnLogger():

    def feature_diff(df, id_col, comp_col):

        items = df[id_col].unique()

        start_diff_dict = dict()
        end_diff_dict = dict()

        for item in items:

            model_indexs = (np.where(df[id_col].str.match(item) == True)
                            [0].tolist())

            comps = df[comp_col].iloc[model_indexs].to_list()

            for i in reversed(range(0, len(model_indexs))):

                if i == len(model_indexs) - 1:

                    start_diff_dict.update({model_indexs[-1]: "End"})
                    end_diff_dict.update({model_indexs[-1]: "End"})

                else:

                    diff = list(set(comps[i+1]).difference(set(comps[i])))

                    diff_start = (np.unique([col[:col.find("_")]
                                             for col in diff])
                                  .tolist())

                    diff_end = (np.unique([col[col.find("__"):]
                                for col in diff])
                                .tolist())

                    start_diff_dict.update({model_indexs[i]: diff_start})

                    end_diff_dict.update({model_indexs[i]: diff_end})

        df["col_start_diff"] = (df.reset_index()["index"]

                                .apply(lambda x: start_diff_dict[x]))

        df["col_end_diff"] = (df.reset_index()["index"]

                                .apply(lambda x: end_diff_dict[x]))

        return df
