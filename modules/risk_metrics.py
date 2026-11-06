import numpy as np
import pandas as pd


def calculate_var_cvar(portfolio_returns):

    # VaR historique
    var_95 = -portfolio_returns.quantile(0.05)
    var_99 = -portfolio_returns.quantile(0.01)

    # CVaR historique
    cvar_95 = -portfolio_returns[
        portfolio_returns <= -var_95
    ].mean()

    cvar_99 = -portfolio_returns[
        portfolio_returns <= -var_99
    ].mean()

    return var_95, cvar_95, var_99, cvar_99


def calculate_max_drawdown(portfolio_value):

    # Plus haut niveau historique atteint
    running_max = portfolio_value.cummax()

    # Drawdown quotidien
    drawdown = (portfolio_value / running_max) - 1

    # Drawdown maximal
    max_drawdown = drawdown.min()

    return drawdown, max_drawdown


def calculate_tracking_error(portfolio_returns, benchmark_returns):

    # Alignement des dates
    returns_data = pd.concat(
        [
            portfolio_returns.rename("Portfolio"),
            benchmark_returns.rename("Benchmark")
        ],
        axis=1
    ).dropna()

    # Rendements actifs
    active_returns = (
        returns_data["Portfolio"] - returns_data["Benchmark"]
    )

    # Tracking Error
    daily_tracking_error = active_returns.std()
    annualized_tracking_error = daily_tracking_error * np.sqrt(252)

    return daily_tracking_error, annualized_tracking_error

def calculate_risk_contribution(portfolio, prices_eur):

    # Pondérations des titres
    weights = portfolio.set_index("Ticker")["Weight"]

    # Rendements journaliers des titres
    asset_returns = prices_eur[weights.index].pct_change(
        fill_method=None
    )

    # On conserve les dates où tous les rendements sont disponibles
    asset_returns = asset_returns.dropna()

    # Matrice de covariance
    cov_matrix = asset_returns.cov()

    # Vecteur des pondérations
    w = weights.loc[cov_matrix.index].values

    # Variance et volatilité du portefeuille
    portfolio_variance = w @ cov_matrix.values @ w
    portfolio_volatility = np.sqrt(portfolio_variance)

    if portfolio_volatility == 0:
        raise ValueError("La volatilité du portefeuille est nulle.")

    # Contribution relative de chaque titre au risque
    risk_contribution = (
        w * (cov_matrix.values @ w)
    ) / portfolio_variance

    # Tableau récapitulatif
    result = pd.DataFrame({
        "Ticker": cov_matrix.index,
        "Weight": w,
        "Risk Contribution": risk_contribution
    })

    return result.sort_values(
        "Risk Contribution",
        ascending=False
    )