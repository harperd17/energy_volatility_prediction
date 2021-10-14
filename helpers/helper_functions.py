import csv
import pandas as pd
import glob


def write_csv(fn, columns, data):
    """
    fn: file_name -> str
    columns: column_names -> list
    data: file contents -> list or set

    """
    with open(fn, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(columns)

        if isinstance(data, set):
            data = list(data)

        for line in data:
            writer.writerow(line)

        print(f"File written to {fn}")


def combine_like_files(fn, func):

    f_names = glob.glob(fn)

    df = pd.concat(map(func, f_names)).reset_index(drop=True)

    return df


def clean_eia_df(df, col):

    # Split Country and State
    df[["country", "state"]] = df["geography"].str.split("-", expand=True)

    # Date cleaning
    df_data_split = pd.DataFrame(df['data'].to_list(), columns=["year_month", col])

    df_data_split["date"] = pd.to_datetime(
        df_data_split["year_month"], format='%Y%m').drop(columns=["year_month"])

    # Combine main df and date cleaning
    df_electric = (pd.merge(df, df_data_split, left_index=True, right_index=True, how="left")
                   .drop(columns=["year_month", "geography", "iso3166", "copyright", "data", "start", "end", "units"])
                   )
    df_electric = df_electric.assign(
        year=df_electric["date"].dt.year)

    return df_electric
