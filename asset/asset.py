

class Asset:
    """Asset class"""

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

    VALIDS_ASSET_CATEGORIES = [
        "stocks",
        "etf",
        "reits",
        "currency",
        "cryptocurrency",
        "funds",
    ]

    def __init__(self, name: str, ticker: str, category: str, amount: float = 0.0) -> None:
        """
        Args:
            name (str): The asset name.
            ticker (str): The asset ticker used in the Yahoo Finance API.
            category (str): The category of the asset. For instance: Stocks
            amount (float, optional): The amount of the asset. Defaults to 0.0.

        Raises:
            TypeError: If asset name is not a str.
            TypeError: If asset ticker is not a str.
            TypeError: If asset category is not a str.
            TypeError: If asset amount is not a float number.
        """
        if isinstance(name, str):
            
            self.name = name
        else:
            
            raise TypeError("Invalid type! The asset name must be a str.")
        if isinstance(ticker, str):
            
            self.ticker = ticker
        else:
            
            raise TypeError("Invalid type! The asset ticker must be a str.")
        if isinstance(category, str):
            
            if category.lower() in Asset.VALIDS_ASSET_CATEGORIES:
                
                self.category = category
            else:
                
                self.category = 'Other'
        else:
            
            raise TypeError("Invalid type! The asset category must be a str.")
        if isinstance(amount, float):
            
            self.amount = amount
        else:
            
            raise TypeError("Invalid type! The asset amount must be a float number.")
