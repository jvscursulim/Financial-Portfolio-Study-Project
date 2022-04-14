import numpy as np
import matplotlib.pyplot as plt
import re
import seaborn as sns
import yfinance as yf
from asset import Asset
from datetime import date, timedelta, datetime
from portfolio import Portfolio
from typing import Optional, List


def plot_assets_close_price_custom_date(assets_list: List[Asset], start_date: str, end_date: Optional[str] = None, save_fig: Optional[bool] = False, fig_name: Optional[str] = None) -> None:
    """Creates a plot of the close price of the assets in a custom time period.

    Args:
        assets_list (List[Asset]): A list of assets.
        start_date (str): The start date.
        end_date (Optional[str], optional): The end date. Defaults to None.
        save_fig (Optional[bool], optional): If we want to save the figure. Defaults to False.
        fig_name (Optional[str], optional): The name that we want to give for the plot. Defaults to None.

    Raises:
        ValueError: If the start_date is ahead 
        ValueError: If the start_date is ahead 
        ValueError: Wrong input date format
        ValueError: Wrong input date format
        TypeError: If the inputs are not a List, a str, a str, a bool and a str.
    """
    if isinstance(assets_list, List) and isinstance(start_date, str) and (isinstance(end_date, str) or end_date is None) and isinstance(save_fig, bool) and (isinstance(fig_name, str) or fig_name is None):
        
        if len(assets_list) != 0:
            
            tickers_list = [asset.ticker for asset in assets_list]
            if end_date is None:
                
                today = date.today()
                today_str = today.strftime("%Y-%m-%d")
                if isinstance(re.match(r'\d{4}-\d{2}-\d{2}', start_date), re.Match):
                    
                    if start_date >= today_str:
                        
                        raise ValueError("The start_date can't be ahead from the today date.")
                    else:
                        
                        data = yf.download(tickers_list, start=start_date, end=today_str, progress=False)
                        data.dropna()
                        sns.set()
                        data["Adj Close"].plot()
                        plt.title(f"Assets close price from {start_date} to {today_str}")
                        plt.xlabel("Date")
                        plt.ylabel("Close Price - $USD")
                        if save_fig:
                            
                            if fig_name is None:
                                
                                datetime_str_list = str(datetime.now()).split(" ")
                                date_extracted = datetime_str_list[0].split("-")
                                year = date_extracted[0]
                                month = date_extracted[1]
                                day = date_extracted[2]
                                plt.savefig(f"figures/assets_close_price_plot_custom_{year}_{month}_{day}.jpg", dpi=300)
                            else:
                                
                                plt.savefig(f"figures/{fig_name}.jpg", dpi=300)
                else:
                    
                    raise ValueError("Wrong date format! The date format for this function is yyyy-mm-dd.")
            else:
                
                if isinstance(re.match(r'\d{4}-\d{2}-\d{2}', start_date), re.Match) and isinstance(re.match(r'\d{4}-\d{2}-\d{2}', end_date), re.Match):
                    
                    if start_date >= end_date:
                        
                        raise ValueError("The start_date can't be ahead from the end date.")
                    else:
                        
                        data = yf.download(tickers_list, start=start_date, end=end_date, progress=False)
                        data.dropna()
                        sns.set()
                        data["Adj Close"].plot()
                        plt.title(f"Assets close price from {start_date} to {end_date}")
                        plt.xlabel("Date")
                        plt.ylabel("Close Price - $USD")
                        if save_fig:
                            
                            if fig_name is None:
                                
                                datetime_str_list = str(datetime.now()).split(" ")
                                date_extracted = datetime_str_list[0].split("-")
                                year = date_extracted[0]
                                month = date_extracted[1]
                                day = date_extracted[2]
                                plt.savefig(f"figures/assets_close_price_plot_custom_{year}_{month}_{day}.jpg", dpi=300)
                            else:
                                
                                plt.savefig(f"figures/{fig_name}.jpg", dpi=300)
                else:
                    
                    raise ValueError("Wrong date format! The date format for this function is yyyy-mm-dd.")
        else:
            
            print("Empty assets list!")               
    else:
        
        raise TypeError("Invalids types! This function expects a List, a str, a str, a bool and a str as input.")

def plot_assets_close_price_time_period(assets_list: List[Asset], time_period: str, save_fig: Optional[bool] = False, fig_name: Optional[str] = None) -> None:
    """Creates a plot of the close price of the assets in a fixed time period.

    Args:
        assets_list (List[Asset]): The assets list.
        time_period (str): The time period that we want to see the close price of the assets.
        save_fig (Optional[bool], optional): If we want to save the plot. Defaults to False.
        fig_name (Optional[str], optional): The name that we want to give for the plot. Defaults to None.

    Raises:
        TypeError: If the inputs are not equal to a List, a str, a bool and a str.
        TypeError: If the fig_name is not equal to a str.
    """
    if isinstance(assets_list, List) and isinstance(time_period, str) and isinstance(save_fig, bool) and (isinstance(fig_name, str) or fig_name is None):
        
        if len(assets_list) != 0:
            
            tickers_list = [asset.ticker for asset in assets_list]
            if time_period in Portfolio.VALIDS_TIME_PERIODS:
                
                data = yf.download(tickers_list, period=time_period, progress=False)
                sns.set()
                data["Adj Close"].plot()
                plt.title(f"Assets close price in {time_period}")
                plt.xlabel("Date")
                plt.ylabel("Close Price - $USD")
                if save_fig:
                    
                    if fig_name is None:
                        
                        datetime_str_list = str(datetime.now()).split(" ")
                        date_extracted = datetime_str_list[0].split("-")
                        year = date_extracted[0]
                        month = date_extracted[1]
                        day = date_extracted[2]
                        plt.savefig(f"figures/assets_close_price_plot_{year}_{month}_{day}.jpg", dpi=300)
                    else:
                        
                        plt.savefig(f"figures/{fig_name}.jpg", dpi=300)
            else:
                
                raise TypeError("Invalid type! The fig_name must be a str.")
        else:
            
            print("Empty assets list!")
    else:
        
        raise TypeError("Invalids types! The input of this functions must be a List, a str, a bool and a str.")
    
def plot_assets_liquidity(assets_list: List[Asset], input_date: Optional[str] = None, save_fig: Optional[bool] = False, fig_name: Optional[str] = None) -> None:
    """Creates a bar plot with the assets liquidity.

    Args:
        assets_list (List[Asset]): The assets list.
        input_date (Optional[str], optional): The date that we want to know the assets liquidity. Defaults to None.
        save_fig (Optional[bool], optional): If we want to save the plot. Defaults to False.
        fig_name (Optional[str], optional): The name that we want to give for the plot. Defaults to None.

    Raises:
        ValueError: If the start_date is in the future.
        TypeError: If the inputs are not a List, str, bool and str.
        TypeError: If the fig_name is not a str.
    """
    if isinstance(assets_list, List) and (isinstance(input_date, str) or input_date is None) and isinstance(save_fig, bool) and (isinstance(fig_name, str) or fig_name is None):
        
        if len(assets_list) != 0:
            
            tickers_list = [asset.ticker for asset in assets_list]
            if input_date is None:
                
                today = date.today()
                start = today - timedelta(days=1)
                today_str = today.strftime("%Y-%m-%d")
                start_str = start.strftime("%Y-%m-%d")
                data = yf.download(tickers_list, start=start_str, end=today_str, progress=False)
                assets_volume_list = [data["Volume"][ticker][0] for ticker in tickers_list]
                sns.set()
                sns.barplot(x=tickers_list, y=assets_volume_list)
                plt.xlabel("Assets")
                plt.ylabel("Transactions Volume ($USD)")
                plt.title(f"Assets liquidity in {today_str}")
                if save_fig:
                    
                    if fig_name is None:
                        
                        datetime_str_list = str(datetime.now()).split(" ")
                        date_extracted = datetime_str_list[0].split("-")
                        year = date_extracted[0]
                        month = date_extracted[1]
                        day = date_extracted[2]
                        plt.savefig(f"figures/assets_liquidity_plot_{year}_{month}_{day}.jpg", dpi=300)
                    else:
                        
                        plt.savefig(f"figures/{fig_name}.jpg", dpi=300)
            else:
                
                if isinstance(re.match(r'\d{4}-\d{2}-\d{2}', input_date), re.Match):
                    
                    today = date.today().strftime("%Y-%m-%d")
                    if input_date > today:
                        
                        raise ValueError("The input_date can't be after today date.")
                    else:
                        
                        end_date = date.fromisoformat(input_date)
                        start = end_date - timedelta(days=1)
                        start_str = start.strftime("%Y-%m-%d")
                        data = yf.download(tickers_list, start=start_str, end=input_date, progress=False)
                        assets_volume_list = [data["Volume"][ticker][0] for ticker in tickers_list]
                        sns.set()
                        sns.barplot(x=tickers_list, y=assets_volume_list)
                        plt.xlabel("Assets")
                        plt.ylabel("Transactions Volume ($USD)")
                        plt.title(f"Assets liquidity in {input_date}")
                        if save_fig:
                            
                            if fig_name is None:
                                
                                datetime_str_list = str(datetime.now()).split(" ")
                                date_extracted = datetime_str_list[0].split("-")
                                year = date_extracted[0]
                                month = date_extracted[1]
                                day = date_extracted[2]
                                plt.savefig(f"figures/assets_liquidity_plot_{year}_{month}_{day}.jpg", dpi=300)
                            else:
                                
                                plt.savefig(f"figures/{fig_name}.jpg", dpi=300)
                else:
                    
                    raise TypeError("Invalid type! The fig_name must be a str.")            
        else:
            
            print("Empty assets list!")
    else:
        
        raise TypeError("Invalids types! The input of this function expects a List, str, bool, str.")

def plot_assets_matrix_correlation(portfolio: Portfolio, time_period: str, save_fig: Optional[bool] = False, fig_name: Optional[str] = None) -> None:
    """Creates a matrix correlation of the assets in the portfolio.

    Args:
        portfolio (Portfolio): The portfolio that we will use to calculate the matrix correlation.
        time_period (str): The time period to get data for the calculation the matrix correlation.
        save_fig (Optional[bool], optional): If we want to save the plot. Defaults to False.
        fig_name (Optional[str], optional): The name we want to give for the plot. Defaults to None.

    Raises:
        TypeError: If the inputs are not a Portfolio, str, bool and str.
        TypeError: If the fig_name is not equal to a str.
    """
    if isinstance(portfolio, Portfolio) and isinstance(time_period, str) and isinstance(save_fig, bool) and (isinstance(fig_name, str) or fig_name is None):
        
        if len(portfolio.assets) != 0:
            
            if time_period in Portfolio.VALIDS_TIME_PERIODS:
                
                assets_correlation = portfolio.correlation_between_assets(time_period=time_period)
                sns.set()
                sns.heatmap(assets_correlation, annot=True)
                plt.title("Assets correlation matrix")
                if save_fig:
                    
                    if fig_name is None:
                        
                        datetime_str_list = str(datetime.now()).split(" ")
                        date_extracted = datetime_str_list[0].split("-")
                        year = date_extracted[0]
                        month = date_extracted[1]
                        day = date_extracted[2]
                        plt.savefig(f"figures/correlation_matrix_{year}_{month}_{day}.jpg", dpi=300)
                    elif isinstance(fig_name, str):
                        
                        plt.savefig(f"figures/{fig_name}.jpg", dpi=300)
                    else:
                        
                        raise TypeError("Invalid type! The fig_name must be a str.")
        else:
            
            print("Empty assets list!")
    else:
        
        raise TypeError("Invalids types! This functions expects a Portfolio, a str, a bool and a str as input.")
    
def plot_assets_pie_chart(portfolio: Portfolio, save_fig: Optional[bool] = False) -> None:
    """Creates a pie chart of the assets allocation.

    Args:
        portfolio (Portfolio): The portfolio that we want to see the pie chart assets.
        save_fig (Optional[bool], optional): If we want to save the plot. Defaults to False. Defaults to False.

    Raises:
        TypeError: If the inputs are not a Portfolio and a bool.
    """
    if isinstance(portfolio, Portfolio) and isinstance(save_fig, bool):
        
        if len(portfolio.assets) != 0:
            
            portfolio_value = 0.0
            labels = [asset.name for asset in portfolio.assets]
            assets_amount = {asset.ticker: asset.amount for asset in portfolio.assets}
            assets_value = []
            for asset in portfolio.assets:
                
                data = yf.download(asset.ticker, period="1d", progress=False)
                data.dropna()
                assets_value.append(assets_amount[asset.ticker]*data["Adj Close"][0])
                portfolio_value += np.round(assets_amount[asset.ticker]*data["Adj Close"][0], 2)
            assets_value_np = np.array(assets_value)
            assets_percentage = (assets_value_np/portfolio_value)*100
            colors = sns.color_palette('pastel')[0:len(assets_percentage)]
            sns.set()
            plt.pie(assets_percentage, labels=labels, colors=colors, autopct='%.1f%%')
            plt.title("Portfolio assets allocation")
            if save_fig:
                
                plt.savefig("figures/assets_percentage_pie_chart.jpg", dpi=300)
        else:
            
            print("The assets list of this portfolio is empty!")
    else:
        
        raise TypeError("Invalids types! This functions expects a Portfolio and a bool.")
    
def plot_assets_category_pie_chart(portfolio: Portfolio, save_fig: Optional[bool] = False) -> dict:
    """Creates a pie chart of the assets category.

    Args:
        portfolio (Portfolio): The portfolio that we want to see the pie chart assets category.
        save_fig (Optional[bool], optional): If we want to save the plot. Defaults to False.

    Raises:
        TypeError: If the inputs are not a Portfolio and a bool.
    """
    if isinstance(portfolio, Portfolio) and isinstance(save_fig, bool):
        
        if len(portfolio.assets) != 0:
            
            num_assets = len(portfolio.assets)
            category_count = {category: 0 for category in Asset.VALIDS_ASSET_CATEGORIES}
            for asset in portfolio.assets:
                
                if asset.category.lower() == 'stocks':
                    
                    category_count['stocks'] = category_count['stocks'] + 1
                elif asset.category.lower() == 'etf':
                    
                    category_count['etf'] = category_count['etf'] + 1
                elif asset.category.lower() == 'reits':
                    
                    category_count['reits'] = category_count['reits'] + 1
                elif asset.category.lower() == 'currency':
                    
                    category_count['currency'] = category_count['currency'] + 1
                elif asset.category.lower() == 'cryptocurrency':
                    
                    category_count['cryptocurrency'] = category_count['cryptocurrency'] + 1
                elif asset.category.lower() == 'funds':
                    
                    category_count['funds'] = category_count['funds'] + 1
            labels = [key for key, value in category_count.items() if value != 0]
            category_count_list = [count for _,count in category_count.items() if count > 0]
            category_count_np = np.array(category_count_list)
            category_percentage = (category_count_np/num_assets)*100
            colors = sns.color_palette('pastel')[0:len(category_percentage)]
            sns.set()
            plt.pie(category_percentage, labels=labels, colors=colors, autopct='%.2f%%')
            plt.title("Portfolio assets category") 
            if save_fig:
                
                plt.savefig("figures/assets_category_percentage_pie_chart.jpg", dpi=300)
        else:
            
            print("The assets list of this portfolio is empty!")
    else:
        
        raise TypeError("Invalids types! This functions expects a Portfolio and a bool.")
