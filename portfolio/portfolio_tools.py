import sys

sys.path.append("../")

import numpy as np
import pandas as pd
import yfinance as yf
from pandas import DataFrame
from typing import Optional
from portfolio import Portfolio
from datetime import date, datetime, timedelta
from qiskit import Aer
from qiskit.algorithms import VQE, QAOA, NumPyMinimumEigensolver
from qiskit.algorithms.optimizers import Optimizer, OptimizerResult
from qiskit.algorithms.optimizers import COBYLA
from qiskit.circuit.library import TwoLocal
from qiskit.utils import QuantumInstance
from qiskit_finance.applications.optimization import PortfolioOptimization
from qiskit_finance.data_providers import YahooDataProvider
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit_optimization.problems import QuadraticProgram


def _calculate_returns_for_all_time_periods(portfolio: Portfolio) -> None:
    """Calculates the returns of a portfolio

    Args:
        portfolio (Portfolio): The portfolio that we want to know the returns

    Returns:
        None
    """
    tickers_list = [asset.ticker for asset in portfolio.assets]
    assets_amounts_dict = {asset.ticker: asset.amount for asset in portfolio.assets}
    for time_period in Portfolio.VALIDS_TIME_PERIODS:
        
        portfolio_return = 0
        first_portfolio_valuation = 0
        last_portfolio_valuation = 0
        if time_period == "1d":
            
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
            data = yf.download(tickers_list, start=start_date, end=end_date, progress=False)
            data.dropna()
            for ticker in tickers_list:
                
                first_portfolio_valuation += assets_amounts_dict[ticker]*data["Adj Close"][ticker][0]
                last_portfolio_valuation += assets_amounts_dict[ticker]*data["Adj Close"][ticker][-1]
            portfolio_return = np.round(((last_portfolio_valuation-first_portfolio_valuation)/first_portfolio_valuation)*100, 2)
            portfolio.portfolio_return_dict[time_period] = portfolio_return
        else:
            
            data = yf.download(tickers_list, period=time_period, progress=False)
            data.dropna()
            for ticker in tickers_list:
                
                first_portfolio_valuation += assets_amounts_dict[ticker]*data["Adj Close"][ticker][0]
                last_portfolio_valuation += assets_amounts_dict[ticker]*data["Adj Close"][ticker][-1]
            portfolio_return = np.round(((last_portfolio_valuation-first_portfolio_valuation)/first_portfolio_valuation)*100, 2)
            portfolio.portfolio_return_dict[time_period] = portfolio_return
            
def _index_to_selection(i: int, num_assets: int) -> np.array:
    """Creates an array of selected indexes.

    Args:
        i (int): An index.
        num_assets (int): The number of assets.

    Returns:
        np.array: An array of indexes.
    """
    s = "{0:b}".format(i).rjust(num_assets)
    x = np.array([1 if s[i] == "1" else 0 for i in reversed(range(num_assets))])
    return x

def _print_result(quadratic_program: QuadraticProgram, result: OptimizerResult, num_assets: int) -> None:
    """Prints the result of the portfolio optimization.

    Args:
        quadratic_program (QuadraticProgram): The quadratic program that defines the problem.
        result (OptimizerResult): The result obtained in the optimization process.
        num_assets (int): The number of assets in the portfolio.
    """
    selection = result.x
    value = result.fval
    print(f"Optimal: selection {selection}, value {np.round(value, 4)}")
    
    eigenstate = result.min_eigen_solver_result.eigenstate
    eigenvector = eigenstate if isinstance(eigenstate, np.ndarray) else eigenstate.to_matrix()
    probabilities = np.abs(eigenvector) ** 2
    i_sorted = reversed(np.argsort(probabilities))
    print("\n----------------- Full result ---------------------")
    print("selection\tvalue\t\tprobability")
    print("---------------------------------------------------")
    
    for i in i_sorted:
        
        x = _index_to_selection(i, num_assets)
        value = QuadraticProgramToQubo().convert(quadratic_program).objective.evaluate(x)
        probability = probabilities[i]
        print("%10s\t%.4f\t\t%.4f" % (x, value, probability))
        
def market_benchmark_index_return() -> DataFrame:
    """Creates a table with the returns of the benchmarks.

    Returns:
        DataFrame: A table with the benchmarks returns.
    """
    columns_list = ["Name", "Ticker"]
    time_period_list = [f"Return (%) - {time_period}" for time_period in Portfolio.VALIDS_TIME_PERIODS]
    columns_list.extend(time_period_list)
    data_benchmark_index = []
    for name, ticker in Portfolio.MARKET_BENCHMARKS_TICKERS_DICT.items():
        
        index_info = [name, ticker]
        for time_period in Portfolio.VALIDS_TIME_PERIODS:
            
            if time_period == "1d":
                
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
                data = yf.download(ticker, start=start_date, end=end_date, progress=False)
                data.dropna()
                benchmark_return = np.round(((data["Adj Close"][-1] - data["Adj Close"][0])/data["Adj Close"][0])*100, 2)
                index_info.append(benchmark_return)
            else:
                
                data = yf.download(ticker, period=time_period, progress=False)
                data.dropna()
                benchmark_return = np.round(((data["Adj Close"][-1] - data["Adj Close"][0])/data["Adj Close"][0])*100, 2)
                index_info.append(benchmark_return)
        data_benchmark_index.append(index_info)
    pd_benchmarks_returns = pd.DataFrame(data=data_benchmark_index, columns=columns_list)
    return pd_benchmarks_returns
            
         
def numpy_portfolio_optimization(input_portfolio: Portfolio, start_date: datetime, end_date: datetime, risk_factor: float, budget: int) -> None:
    """Run a portfolio optimization with MinimumEigenOptimizer.

    Args:
        input_portfolio (Portfolio): The portfolio that we want to optimize.
        start_date (datetime): The start date for getting data in the Yahoo Finance API. 
        end_date (datetime): The end date for getting data in the Yahoo Finance API.
        risk_factor (float): The risk factor. 
        budget (int): The budget that we have.

    Raises:
        TypeError: If the inputs are not equal to a Portfolio, a datetime, a datetime, a float and a int.
    """
    if isinstance(input_portfolio, Portfolio) and isinstance(start_date, datetime) and isinstance(end_date, datetime) and isinstance(risk_factor, float) and isinstance(budget, int):
        
        num_assets = len(input_portfolio.assets)
        if num_assets != 0:
            
            quadratic_program = _set_quadratic_program(input_portfolio=input_portfolio, start_date=start_date, end_date=end_date, risk_factor=risk_factor, budget=budget)
            exact_mes = NumPyMinimumEigensolver()
            exact_eigensolver = MinimumEigenOptimizer(exact_mes)
            result = exact_eigensolver.solve(quadratic_program)
            _print_result(quadratic_program=quadratic_program, result=result, num_assets=num_assets)
        else:
            
            print("Empty assets list!")
    else:
        
        raise TypeError("Invalid types! This function expects a Portfolio, a datetime, a datetime, a float and an int.")

def vqe_portfolio_optimization(input_portfolio: Portfolio, start_date: datetime, end_date: datetime, risk_factor: float, budget: int, optimizer: Optional[Optimizer] = None, maxiter: Optional[int] = None) -> None:
    """Run a portfolio optimization with VQE (quantum computing). 

    Args:
        input_portfolio (Portfolio): The portfolio that we want to optimize.
        start_date (datetime): The start date for getting data in the Yahoo Finance API.
        end_date (datetime): The end date for getting data in the Yahoo Finance API.
        risk_factor (float): The risk factor.
        budget (int): The budget that we have.
        optimizer (Optional[Optimizer], optional): The optimizer that we want to use in the VQE. Defaults to None.
        maxiter (Optional[int], optional): The number of max iterations of the optimizer. Defaults to None.

    Raises:
        TypeError: If the inputs are not equal to a Portfolio, a datetime, a datetime, a float, an int, a Optimizer and an int.
    """
    if isinstance(input_portfolio, Portfolio) and isinstance(start_date, datetime) and isinstance(end_date, datetime) and isinstance(risk_factor, float) and isinstance(budget, int) and (isinstance(optimizer, Optimizer) or optimizer is None) and (isinstance(maxiter, int) or maxiter is None):
        
        num_assets = len(input_portfolio.assets)
        if num_assets != 0:
            
            quadratic_program = _set_quadratic_program(input_portfolio=input_portfolio, start_date=start_date, end_date=end_date, risk_factor=risk_factor, budget=budget)
            backend = Aer.get_backend("statevector_simulator")
            quantum_instance = QuantumInstance(backend=backend)
            if maxiter is None:
                
                maxiter = 200
            if optimizer is None:
                
                optimizer = COBYLA(maxiter=maxiter)
            circuit = TwoLocal(num_qubits=num_assets, rotation_blocks="ry", entanglement_blocks="cz", reps=3, entanglement="full")
            vqe_mes = VQE(circuit, optimizer=optimizer, quantum_instance=quantum_instance)
            vqe = MinimumEigenOptimizer(vqe_mes)
            result = vqe.solve(quadratic_program)
            _print_result(quadratic_program=quadratic_program, result=result, num_assets=num_assets)
        else:
            
            print("Empty assets list!")
    else:
        
        raise TypeError("Invalid types! This function expects a Portfolio, a datetime, a datetime, a float, an int, an Optimizer and an int.")

def qaoa_portfolio_optimization(input_portfolio: Portfolio, start_date: datetime, end_date: datetime, risk_factor: float, budget: int, optimizer: Optional[Optimizer] = None, maxiter: Optional[int] = None) -> None:
    """Run a portfolio optimization with QAOA (quantum computing).

    Args:
        input_portfolio (Portfolio): The portfolio that we want to optimize.
        start_date (datetime): The start date for getting data in the Yahoo Finance API.
        end_date (datetime): The end date for getting data in the Yahoo Finance API.
        risk_factor (float): The risk factor.
        budget (int): The budget that we have.
        optimizer (Optional[Optimizer], optional): The optimizer that we want to use in the VQE. Defaults to None.
        maxiter (Optional[int], optional): The number of max iterations of the optimizer. Defaults to None.

    Raises:
        TypeError: If the inputs are not equal to a Portfolio, a datetime, a datetime, a float, an int, a Optimizer and an int.
    """
    if isinstance(input_portfolio, Portfolio) and isinstance(start_date, datetime) and isinstance(end_date, datetime) and isinstance(risk_factor, float) and isinstance(budget, int) and (isinstance(optimizer, Optimizer) or optimizer is None) and (isinstance(maxiter, int) or maxiter is None):
        
        num_assets = len(input_portfolio.assets)
        if num_assets != 0:
            
            quadratic_program = _set_quadratic_program(input_portfolio=input_portfolio, start_date=start_date, end_date=end_date, risk_factor=risk_factor, budget=budget)
            backend = Aer.get_backend("statevector_simulator")
            backend = Aer.get_backend("statevector_simulator")
            quantum_instance = QuantumInstance(backend=backend)
            if maxiter is None:
                
                maxiter = 200
            if optimizer is None:
                
                optimizer = COBYLA(maxiter=maxiter)
            qaoa_mes = QAOA(optimizer=optimizer, reps=3, quantum_instance=quantum_instance)
            qaoa = MinimumEigenOptimizer(qaoa_mes)
            result = qaoa.solve(quadratic_program)
            _print_result(quadratic_program=quadratic_program, result=result, num_assets=num_assets)
        else:
            
            print("Empty assets list!")
    else:
        
        raise TypeError("Invalid types! This function expects a Portfolio, a datetime, a datetime, a float, an int, an Optimizer and an int.")
    
def portfolio_current_valuation(portfolio: Portfolio) -> None:
    """Prints the current valuation of the portfolio.

    Args:
        portfolio (Portfolio): The Portfolio that we want to know the current valuation.

    Raises:
        TypeError: If the input is not a Portfolio.
    """
    if isinstance(portfolio, Portfolio):
        
        if len(portfolio.assets) != 0:
            
            assets_amount = {asset.ticker: asset.amount for asset in portfolio.assets}
            portfolio_valuation = 0
            for asset in portfolio.assets:
                
                data = yf.download(asset.ticker, period="1d", progress=False)
                data.dropna()
                portfolio_valuation += np.round(assets_amount[asset.ticker]*data["Adj Close"][0], 2)
            print(f"Current portfolio valuation in USD: ${portfolio_valuation:.2f}")
        else:
            
            print("The portfolio assets list is empty!")
    else:
        
        raise TypeError("Invalid type! This functions expects a Portfolio.")

def _set_quadratic_program(input_portfolio: Portfolio, start_date: datetime, end_date: datetime, risk_factor: float, budget: int) -> QuadraticProgram:
    """Creates the quadratic program that defines the Portfolio optimization.
    
    Args:
        input_portfolio (Portfolio): The portfolio that we want to optimize.
        start_date (datetime): The start date for getting data in the Yahoo Finance API.
        end_date (datetime): The end date for getting data in the Yahoo Finance API.
        risk_factor (float): The risk factor.
        budget (int): The budget that we have.

    Returns:
        QuadraticProgram: The quadratic program that defines the optimization problem.
    """
    tickers_list = [asset.ticker for asset in input_portfolio.assets]
    data = YahooDataProvider(tickers=tickers_list, start=start_date, end=end_date)
    data.run()
    mu = data.get_period_return_mean_vector()
    sigma = data.get_period_return_covariance_matrix()
    portfolio = PortfolioOptimization(expected_returns=mu, covariances=sigma, risk_factor=risk_factor, budget=budget)
    quadratic_program = portfolio.to_quadratic_program()
    return quadratic_program

def show_portfolio_returns_for_all_time_periods(portfolio: Portfolio) -> DataFrame:
    """Creates a table with the returns of the portfolio for all time periods.

    Args:
        portfolio (Portfolio): The portfolio that we want to calculate the returns for all time periods.

    Raises:
        TypeError: If the input is not a Portfolio.

    Returns:
        DataFrame: A table with the returns of the portfolio for all time periods.
    """
    if isinstance(portfolio, Portfolio):
        
        if len(portfolio.assets) != 0:
            
            _calculate_returns_for_all_time_periods(portfolio=portfolio)
            data = [value for _, value in portfolio.portfolio_return_dict.items()]
            columns = [f"Return (%) - {time_period}" for time_period in Portfolio.VALIDS_TIME_PERIODS]
            pd_portfolio_returns = pd.DataFrame(data=[data], columns=columns)
            return pd_portfolio_returns
        else:
            
            print("The portfolio assets list is empty!")
    else:
        
        raise TypeError("Invalid type! This function expects a Portfolio as an input.")