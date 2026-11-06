import numpy as np
import pandas as pd


def calculate_performance(portfolio_value, portfolio_returns):

    # Performance totale du portefeuille
    total_performance = (
        portfolio_value.iloc[-1] / portfolio_value.iloc[0]
    ) - 1

    # Rendement journalier moyen
    average_daily_return = portfolio_returns.mean()

    # Volatilité journalière
    daily_volatility = portfolio_returns.std()

    # Volatilité annualisée
    annualized_volatility = daily_volatility * np.sqrt(252)

    return (
        total_performance,
        average_daily_return,
        daily_volatility,
        annualized_volatility
    )