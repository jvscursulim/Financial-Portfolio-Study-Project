import sys

sys.path.append("../")

import yfinance as yf
from asset import Asset
from pandas import DataFrame
from typing import List, Optional


class Portfolio:
    """Portfolio class"""

    VALIDS_TIME_PERIODS = [
        "1d",
        "5d",
        "1mo",
        "3mo",
        "6mo",
        "1y",
        "2y",
        "5y",
        "10y",
        "ytd",
        "max",
    ]
    MARKET_BENCHMARKS_TICKERS_DICT = {
        "S&P 500": "^GSPC",
        "Dow Jones Industrial Average": "^DJI",
        "NASDAQ 100": "^NDX",
        "Gold": "GC=F",
    }

    def __init__(self, assets: Optional[List] = None) -> None:
        """

        Args:
            assets (Optional[list], optional): A list with the assets that defines a portfolio. Defaults to None.

        Raises:
            TypeError: If the input is not equal to a list.
        """
        if isinstance(assets, list):
            
            self.assets = assets
        elif assets is None:
            
            self.assets = []
        else:
            
            raise TypeError("Invalid type!")
        self.portfolio_return_dict = {time_period: 0.0 for time_period in Portfolio.VALIDS_TIME_PERIODS}

    def add_an_asset(self, asset: Asset) -> None:
        """Adds an asset in the portfolio assets list.

        Args:
            asset (Asset): An asset that we want to add in the portfolio assets list.

        Raises:
            TypeError: If the input is not an Asset class.
        """
        if isinstance(asset, Asset):
            
            self.assets.append(asset)
        else:
            
            raise TypeError("Invalid type! The input must be an Asset class.")

    def correlation_between_assets(self, time_period: str) -> DataFrame:
        """Builds a table with the correlation between the assets.

        Args:
            time_period (str): The time period that will used to calculate
            the correlation between the assets

        Returns:
            DataFrame: A table with the correlations between the assets.
        """
        if len(self.assets) != 0:
            
            tickers = [asset.ticker for asset in self.assets]
            data = yf.download(tickers, period=time_period, progress=False)
            data.dropna()
            assets_correlation = data["Adj Close"].corr()
            return assets_correlation
        else:
            
            print("Empty assets list!")

    def remove_an_asset(self, asset_name: str) -> None:
        """Removes an asset from the assets list of the portfolio.
        
        Args:
            asset_name (str): The name of the asset we want to remove from the portfolio.

        Raises:
            TypeError: If asset_name is not a str.
        """
        if len(self.assets) == 0:
            
            print(
                "It is not possible to remove assets because the assets list is empty!"
            )
        else:
            
            if isinstance(asset_name, str):
                
                assets_names_list = [asset.name for asset in self.assets]
                if asset_name in assets_names_list:
                    
                    asset_index = assets_names_list.index(asset_name)
                    del self.assets[asset_index]
                else:
                    
                    print(
                        f"The asset called {asset_name} is not in the assets list of this portfolio!"
                    )
            else:
                
                raise TypeError("Invalid type! The asset_name must be a str.")
