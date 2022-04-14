import pandas as pd
from pandas import DataFrame
from typing import Optional
from datetime import datetime


def load_data_from_csv(file_path: str) -> DataFrame:
    """Loads data from a .csv file

    Args:
        file_path (str): The path to the file.

    Raises:
        TypeError: If file_path is not a str.

    Returns:
        DataFrame: A table with loaded data from a .csv file.
    """
    if isinstance(file_path, str):
        
        data_pd = pd.read_csv(file_path)
        return data_pd
    else:
        
        raise TypeError("Invalid type! The file_path must be a str.")

def store_data(data: DataFrame, file_name: Optional[str] = None) -> None:
    """Stores data obtained in the Yahoo Finance API in a .csv file.

    Args:
        data (DataFrame): The DataFrame with the data we want to store.
        file_name (Optional[str], optional): The name that we want to give for the file. Defaults to None.

    Raises:
        TypeError: If file_name is not a str.
    """
    if file_name is None:
        
        datetime_str_list = str(datetime.now()).split(" ")
        date = datetime_str_list[0].split("-")
        year = date[0]
        month = date[1]
        day = date[2]
        data.to_csv(f"csv_files/asset_data_{year}_{month}_{day}.csv")
    elif isinstance(file_name, str):
        
        data.to_csv(f"csv_files/{file_name}.csv")
    else:
        
        raise TypeError("Invalid type! The file_name must be a str.")