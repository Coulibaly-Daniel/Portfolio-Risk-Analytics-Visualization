import pandas as pd
import yfinance as yf

def load_data():

    portfolio = pd.read_excel("data/portfolio.xlsx")

    prices_eur = pd.read_csv(
        "data/prices_eur.csv",
        index_col=0,
        parse_dates=True
    )

    return portfolio, prices_eur



def calculate_portfolio(portfolio, prices_eur):

    weights = portfolio.set_index("Ticker")["Weight"]

    # Sélection des actions du portefeuille
    prices = prices_eur[weights.index].copy()

    # Première date à laquelle tous les titres ont un prix disponible
    valid_initial_dates = prices.dropna().index

    initial_prices = prices.loc[valid_initial_dates[0]]

    # Vérification des prix initiaux
    if initial_prices.isna().any() or (initial_prices <= 0).any():
        raise ValueError("Certains prix initiaux sont manquants ou invalides.")

    # Quantités achetées pour une valeur initiale de 100 EUR
    quantities = 100 * weights / initial_prices

    # Valorisation avec le dernier cours disponible
    prices_valuation = prices.ffill()

    # Valeur quotidienne du portefeuille
    portfolio_value = prices_valuation.mul(
        quantities
    ).sum(axis=1, min_count=len(quantities))

    # Suppression des dates sans valorisation complète
    portfolio_value = portfolio_value.dropna()

    # Performance base 100
    portfolio_performance = (
        portfolio_value / portfolio_value.iloc[0]
    ) * 100

    # Rendements journaliers
    portfolio_returns = portfolio_value.pct_change(
        fill_method=None
    ).dropna()

    return (
        quantities,
        portfolio_value,
        portfolio_performance,
        portfolio_returns
    )


def load_benchmark():

    ticker = "EUNL.DE"

    benchmark = yf.Ticker(ticker).history(
        period="5y",
        interval="1d",
        auto_adjust=True
    )

    if benchmark.empty:
        raise ValueError("Impossible de récupérer les données du benchmark.")

    benchmark_prices = benchmark["Close"]

    # Normalisation des dates
    benchmark_prices.index = pd.to_datetime(
        benchmark_prices.index
    )

    if benchmark_prices.index.tz is not None:
        benchmark_prices.index = benchmark_prices.index.tz_localize(None)

    benchmark_prices.index = benchmark_prices.index.normalize()

    benchmark_prices = benchmark_prices.groupby(
        benchmark_prices.index
    ).last()

    return benchmark_prices.rename("Benchmark")