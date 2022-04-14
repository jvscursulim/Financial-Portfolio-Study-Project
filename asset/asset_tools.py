import sys

sys.path.append("../")

import numpy as np
import pandas as pd
import re
import yfinance as yf
from asset import Asset
from datetime import date, timedelta
from pandas import DataFrame
from typing import List, Optional

def asset_return_for_a_time_period(assets_list: List[Asset], time_period: str) -> DataFrame:
    """Calculates the returns of a list of assets for a given time period.

    Args:
        assets_list (List[Asset]): A list of assets.
        time_period (str): The period of time that we want to know the return of the assets.

    Raises:
        TypeError: If function input is not equal to a List and a str.
        TypeError: If the itens in the input list are not equal to a class Asset.

    Returns:
        DataFrame: A table with the returns of the assets in the given time period.
    """
    if isinstance(assets_list, List) and isinstance(time_period, str):
        
        data = []
        for asset in assets_list:
            
            if isinstance(asset, Asset):
                
                if time_period in asset.VALIDS_TIME_PERIODS:
                    
                    asset_return_list_info = [asset.name]
                    columns_list = ["Asset", f"Return (%) - {time_period}"]
                    if time_period == "1d" and asset.category.lower() != "cryptocurrency":
                        
                        end = date.today()
                        if date.weekday(end) == 0:
                            
                            start = end - timedelta(days=4)
                        elif date.weekday(end) == 5:
                            
                            start = end - timedelta(days=2)
                        elif date.weekday(end) == 6:
                            
                            start = end - timedelta(days=3)
                        else:
                            
                            start = end - timedelta(days=2)
                            if date.weekday(start) == 5:
                                
                                start = start - timedelta(days=1)
                            elif date.weekday(start) == 6:
                                
                                start = start - timedelta(days=2)
                        end_date = end.strftime("%Y-%m-%d")
                        start_date = start.strftime("%Y-%m-%d")
                        asset_data = yf.download(asset.ticker, start=start_date, end=end_date, progress=False)
                        asset_return = np.round(((asset_data["Adj Close"][-1] - asset_data["Adj Close"][0])/asset_data["Adj Close"][0])*100, 2)
                    elif time_period == "1d" and asset.category.lower() == "cryptocurrency":
                        
                        end = date.today()
                        start = end - timedelta(days=1)
                        end_date = end.strftime("%Y-%m-%d")
                        start_date = start.strftime("%Y-%m-%d")
                        asset_data = yf.download(asset.ticker, start=start_date, end=end_date, progress=False)
                        asset_return = np.round(((asset_data["Adj Close"][-1] - asset_data["Adj Close"][0])/asset_data["Adj Close"][0])*100, 2)
                    else:
                        
                        asset_data = yf.download(asset.ticker, period=time_period, progress=False)
                        asset_return = np.round(((asset_data["Adj Close"][-1] - asset_data["Adj Close"][0])/asset_data["Adj Close"][0])*100, 2)
                    asset_return_list_info.append(asset_return)
                    data.append(asset_return_list_info)
            else:
                
                raise TypeError("Invalid type! The elements of the list must be an Asset.")
        asset_returns_pd = pd.DataFrame(data=data, columns=columns_list)
        return asset_returns_pd
    else:
        
        raise TypeError("Invalid types! This expects a List and a str as input.")

def asset_return_for_all_time_periods(assets_list: List[Asset]) -> DataFrame:
    """Calculates the returns of the assets for all time period available in Yahoo Finance.

    Args:
        assets_list (List[Asset]): A list with assets.

    Raises:
        TypeError: If the elements of the list is not a Asset.
        TypeError: If the input is not a List.

    Returns:
        DataFrame: A table with assets returns.
    """
    if isinstance(assets_list, List):
        
        data = []
        for asset in assets_list:
            
            if isinstance(asset, Asset):
                
                asset_return_list_info = [asset.name]
                columns_list = ["Asset"]
                time_period_columns = [f"Return (%) - {time_period}" for time_period in asset.VALIDS_TIME_PERIODS]
                columns_list.extend(time_period_columns)
                for time_period in asset.VALIDS_TIME_PERIODS:
                    
                    if time_period == "1d" and asset.category.lower() != "cryptocurrency":
                        
                        end = date.today()
                        if date.weekday(end) == 0:
                            
                            start = end - timedelta(days=4)
                        elif date.weekday(end) == 5:
                            
                            start = end - timedelta(days=2)
                        elif date.weekday(end) == 6:
                            
                            start = end - timedelta(days=3)
                        else:
                            
                            start = end - timedelta(days=2)
                            if date.weekday(start) == 5:
                                
                                start = start - timedelta(days=1)
                            elif date.weekday(start) == 6:
                                
                                start = start - timedelta(days=2)
                        end_date = end.strftime("%Y-%m-%d")
                        start_date = start.strftime("%Y-%m-%d")
                        asset_data = yf.download(asset.ticker, start=start_date, end=end_date, progress=False)
                        asset_data.dropna()
                        asset_return = np.round(((asset_data["Adj Close"][-1] - asset_data["Adj Close"][0])/asset_data["Adj Close"][0])*100, 2)
                    elif time_period == "1d" and asset.category.lower() == "cryptocurrency":
                        
                        end = date.today()
                        start = end - timedelta(days=1)
                        end_date = end.strftime("%Y-%m-%d")
                        start_date = start.strftime("%Y-%m-%d")
                        asset_data = yf.download(asset.ticker, start=start_date, end=end_date, progress=False)
                        asset_data.dropna()
                        asset_return = np.round(((asset_data["Adj Close"][-1] - asset_data["Adj Close"][0])/asset_data["Adj Close"][0])*100, 2)
                    else:
                        
                        asset_data = yf.download(asset.ticker, period=time_period, progress=False)
                        asset_data.dropna()
                        asset_return = np.round(((asset_data["Adj Close"][-1] - asset_data["Adj Close"][0])/asset_data["Adj Close"][0])*100, 2)
                    asset_return_list_info.append(asset_return)
                data.append(asset_return_list_info)
            else:
                
                raise TypeError("Invalid type! The elements of the list must be an Asset.")
        asset_returns_pd = pd.DataFrame(data=data, columns=columns_list)
        return asset_returns_pd
    else:
        
        raise TypeError("Invalid type! This function expects a list of assets.")

def get_asset_data_in_a_custom_time_period(asset: Asset, start_date: str, end_date: Optional[str] = None) -> DataFrame:
    """Obtains the data of the input asset in a custom time period.

    Args:
        asset (Asset): The asset.
        start_date (str): The start date (format:yyyy-mm-dd)
        end_date (Optional[str], optional): The end date (format:yyyy-mm-dd). Defaults to None.

    Raises:
        ValueError: If start_date is ahead from today date.
        ValueError: If start_date is ahead from end_date.
        ValueError: Wrong format date.
        ValueError: Wrong format date.
        TypeError: If the inputs are not an Asset, a str and a str.

    Returns:
        DataFrame: A table with information about an asset in a custom time period.
    """
    if isinstance(asset, Asset) and isinstance(start_date, str) and (isinstance(end_date, str) or end_date is None):
        
        if end_date is None:
            
            end_date = date.today()
            end_date_str = end_date.strftime("%Y-%m-%d")
            if isinstance(re.match(r'\d{4}-\d{2}-\d{2}', start_date), re.Match):
                
                if start_date >= end_date_str:
                    
                    raise ValueError("The start_date can't be ahead from the today date.")
                else:
                    
                    if asset.category.lower() != "cryptocurrency":
                        
                        start_date_obj = date.fromisoformat(start_date)
                        if date.weekday(start_date_obj) == 5:
                            
                            start_date_obj = start_date_obj - timedelta(days=1)
                            start_date = start_date_obj.strftime("%Y-%m-%d")
                        elif date.weekday(start_date_obj) == 6:
                            
                            start_date_obj = start_date_obj - timedelta(days=2)
                            start_date = start_date_obj.strftime("%Y-%m-%d")
                        asset_data = yf.download(asset.ticker, start=start_date, end=end_date_str, progress=False)
                        asset_data.dropna()
                        asset_data["Date"] = asset_data.index
                        columns_list = ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
                        for column in columns_list:
                            
                            if column == "Date" or column == "Volume":
                                
                                pass
                            else:
                                
                                asset_data[column] = np.round(asset_data[column], 2)
                        asset_data.reset_index(drop=True, inplace=True)
                        asset_data_pd = pd.DataFrame(data=asset_data, columns=columns_list)
                        return asset_data_pd
            else:
                
                raise ValueError("Wrong format date! The date should be in the following format: yyyy-mm-dd.")
                    
        else:
            
            if isinstance(re.match(r'\d{4}-\d{2}-\d{2}', start_date), re.Match) and isinstance(re.match(r'\d{4}-\d{2}-\d{2}', end_date), re.Match):
                
                if start_date >= end_date:
                    
                    raise ValueError("The start_date can't be ahead from the end_date.")
                else:
                    
                    if asset.category.lower() != "cryptocurrency":
                        
                        start_date_obj = date.fromisoformat(start_date)
                        if date.weekday(start_date_obj) == 5:
                            
                            start_date_obj = start_date_obj - timedelta(days=1)
                            start_date = start_date_obj.strftime("%Y-%m-%d")
                        elif date.weekday(start_date_obj) == 6:
                            
                            start_date_obj = start_date_obj - timedelta(days=2)
                            start_date = start_date_obj.strftime("%Y-%m-%d")
                        asset_data = yf.download(asset.ticker, start=start_date, end=end_date, progress=False)
                        asset_data.dropna()
                        asset_data["Date"] = asset_data.index
                        columns_list = ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
                        for column in columns_list:
                            
                            if column == "Date" or column == "Volume":
                                
                                pass
                            else:
                                
                                asset_data[column] = np.round(asset_data[column], 2)
                        asset_data.reset_index(drop=True, inplace=True)
                        asset_data_pd = pd.DataFrame(data=asset_data, columns=columns_list)
                        return asset_data_pd
                    else:
                        
                        asset_data = yf.download(asset.ticker, start=start_date, end=end_date, progress=False)
                        asset_data.dropna()
                        asset_data["Date"] = asset_data.index
                        columns_list = ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
                        for column in columns_list:
                            
                            if column == "Date" or column == "Volume":
                                
                                pass
                            else:
                                
                                asset_data[column] = np.round(asset_data[column], 2)
                        asset_data.reset_index(drop=True, inplace=True)
                        asset_data_pd = pd.DataFrame(data=asset_data, columns=columns_list)
                        return asset_data_pd
            else:
                
                raise ValueError("Wrong format date! The date should be in the following format: yyyy-mm-dd.")
    else:
        
        raise TypeError("Invalid types! This function expects an Asset, a str and a str.")

def get_asset_data_in_a_time_period(asset: Asset, time_period: str) -> DataFrame:
    """Obtains the data of the input asset in a fixed time period.

    Args:
        asset (Asset): The asset.
        time_period (str): The time period valid in the Yahoo Finance API.

    Raises:
        ValueError: If the time period is not a valid Yahoo Finance API.
        TypeError: If the inputs are not equal to an Asset and a str.

    Returns:
        DataFrame: A table with data about the asset gave in the input.
    """
    if isinstance(time_period, str) and isinstance(asset, Asset):
        
        if time_period in Asset.VALIDS_TIME_PERIODS:
            
            asset_data = yf.download(asset.ticker, period=time_period, progress=False)
            asset_data.dropna()
            asset_data["Date"] = asset_data.index
            columns_list = ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
            for column in columns_list:
                
                if column == "Date" or column == "Volume":
                    
                    pass
                else:
                    
                    asset_data[column] = np.round(asset_data[column], 2)
            asset_data.reset_index(drop=True, inplace=True)
            asset_data_pd = pd.DataFrame(data=asset_data, columns=columns_list)
            return asset_data_pd
        else:
            
            raise ValueError("Invalid time period! Check the valids time period in Yahoo Finance API.")
    else:
        
        raise TypeError("Invalid types! This function expects a str and an Asset class as input.")
    
def today_asset_info(assets_list: List[Asset]) -> DataFrame:
    """Obtain the information about the assets through Yahoo Finance API.

    Args:
        assets_list (List[Asset]): A list with the assets.

    Raises:
        TypeError: If the elements of the list are not equal to a Asset class.
        TypeError: If the input is not equal to a List.

    Returns:
        DataFrame: A table with today information about the assets.
    """
    if isinstance(assets_list, List):
        
        data = []
        for asset in assets_list:
            
            if isinstance(asset, Asset):
                
                today = date.today()
                end_date = today.strftime("%Y-%m-%d")
                start = today - timedelta(days=2)
                start_date = start.strftime("%Y-%m-%d")
                asset_data = yf.download(asset.ticker, start=start_date, end=end_date, progress=False)
                asset_data.dropna()
                asset_return = np.round(((asset_data["Adj Close"][-1] - asset_data["Adj Close"][0])/asset_data["Adj Close"][0])*100, 2)
                columns_list = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]
                for column in columns_list:
                    
                    if column == "Date" or column == "Volume":
                        
                        pass
                    else:
                        
                        asset_data[column] = np.round(asset_data[column], 2)
            else:
                
                raise TypeError("Invalid type! The elements of the list must be an Asset.")
            asset_info = [asset.name, asset_return, asset_data["Open"][0], asset_data["High"][0], asset_data["Low"][0], asset_data["Close"][0], asset_data["Adj Close"][0], asset_data["Volume"][0]]
            data.append(asset_info)
        columns_list.insert(0, "Asset")
        columns_list.insert(1, "Return (%)")
        asset_data_pd = pd.DataFrame(data=data, columns=columns_list)
        return asset_data_pd
    else:
        
        raise TypeError("Invalid type! This function expects a list of assets.")
