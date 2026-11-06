
import streamlit as st
import pandas as pd
import numpy as np

from modules.portfolio import (load_data, calculate_portfolio, load_benchmark)
from modules.performance import calculate_performance
from modules.risk_metrics import (
    calculate_var_cvar,
    calculate_max_drawdown,
    calculate_tracking_error,
    calculate_risk_contribution
)
from modules.visualization import (
    plot_portfolio_vs_benchmark,
    plot_portfolio_drawdown,
    plot_sector_allocation,
    plot_geographic_allocation,
    plot_risk_contribution
)

# ============================================================
# 1. CONFIGURATION DE L'APPLICATION
# ============================================================

st.set_page_config(
    page_title="Portfolio Risk Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 SUIVI DE RISQUES DE PORTEFEUILLE")

st.markdown("""
Bienvenue dans notre application d'analyse de portefeuille.

Cet outil permet de suivre la composition, la performance
et les risques d'un portefeuille d'actions.
""")

# ============================================================
# 2. CHARGEMENT DES DONNÉES
# ============================================================

@st.cache_data
def get_data():
    return load_data()


try:
    portfolio, prices_eur = get_data()
    st.success("Données chargées avec succès !")

    # Test du benchmark
    benchmark_prices = load_benchmark()
    benchmark_returns = benchmark_prices.pct_change(fill_method=None).dropna()


    # ========================================================
    # 3. COMPOSITION DU PORTEFEUILLE
    # ========================================================

    st.header("1. Composition du portefeuille")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Nombre d'actifs", len(portfolio))

    with col2:
        st.metric("Nombre d'observations", len(prices_eur))

    with col3:
        st.metric("Nombre d'actions", prices_eur.shape[1])

    st.dataframe(portfolio, use_container_width=True)

    # ========================================================
    # 4. CALCUL DU PORTEFEUILLE
    # ========================================================

    (
        quantities,
        portfolio_value,
        portfolio_performance,
        portfolio_returns
    ) = calculate_portfolio(portfolio, prices_eur)

    # ========================================================
    # 5. INDICATEURS DE PERFORMANCE
    # ========================================================

    (
        total_performance,
        average_daily_return,
        daily_volatility,
        annualized_volatility
    ) = calculate_performance(
        portfolio_value,
        portfolio_returns
    )

    st.header("2. Performance du Portefeuille")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Performance",
            f"{total_performance:.2%}"
        )

    with col2:
        st.metric(
            "Rendement journalier moyen",
            f"{average_daily_return:.2%}"
        )

    with col3:
        st.metric(
            "volatilité journalière",
            f"{daily_volatility:.2%}"
        )

    with col4:
        st.metric(
            "Volatilité annualisée",
            f"{annualized_volatility:.2%}"
        )

    st.subheader("Prix historiques du Benchmark")
    st.dataframe(benchmark_prices.tail())

    # Comparaison avec le benchmark
    st.subheader("Portefeuille vs Performance du Benchmark ")

    fig_benchmark = plot_portfolio_vs_benchmark(
        portfolio_returns,
        benchmark_returns
    )

    st.plotly_chart(
        fig_benchmark,
        use_container_width=True,
        key="benchmark_performance_chart"
    )

   


    # ========================================================
    # 6. INDICATEURS DE RISQUE
    # ========================================================

    st.header("3. Analyse des risques de marché")

    # VaR et CVaR
    var_95, cvar_95, var_99, cvar_99 = calculate_var_cvar(
        portfolio_returns
    )

    # Maximum Drawdown
    drawdown, max_drawdown = calculate_max_drawdown(
        portfolio_value
    )

    # Graphique Drawdown
    st.subheader("Evolution du Drawdown du portefeuille")

    fig_drawdown = plot_portfolio_drawdown(drawdown)

    st.plotly_chart(
        fig_drawdown,
        use_container_width=True,
        key="portfolio_drawdown_chart"
    )

    # Sector & Geographic Allocation

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Allocation Sectorielle du Portefeuille ")

        fig_sector = plot_sector_allocation(portfolio)

        st.plotly_chart(
            fig_sector,
            use_container_width=True,
            key="sector_allocation_chart"
    )

    with col2:
        st.subheader("Allocation Géographique du Portefeuille ")

        fig_geo = plot_geographic_allocation(portfolio)

        st.plotly_chart(
            fig_geo,
            use_container_width=True,
            key="geographic_allocation_chart"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("VaR 95%", f"{var_95:.2%}")

    with col2:
        st.metric("CVaR 95%", f"{cvar_95:.2%}")

    with col3:
        st.metric("VaR 99%", f"{var_99:.2%}")

    with col4:
        st.metric("CVaR 99%", f"{cvar_99:.2%}")

    st.metric(
        "Maximum Drawdown",
        f"{max_drawdown:.2%}"
    )

    daily_te, annualized_te = calculate_tracking_error(
    portfolio_returns,
    benchmark_returns
)

    st.subheader("Benchmark & Tracking Error")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Daily Tracking Error", f"{daily_te:.2%}")

    with col2:
        st.metric("Annualized Tracking Error", f"{annualized_te:.2%}")

    # Risk Contribution by Asset
    st.subheader("Portfolio Weight vs Risk Contribution")

    risk_data = calculate_risk_contribution(
        portfolio,
        prices_eur
)

    fig_risk = plot_risk_contribution(risk_data)

    st.plotly_chart(
        fig_risk,
        use_container_width=True,
        key="risk_contribution_chart"
)

except FileNotFoundError as error:
    st.error(f"Fichier introuvable : {error}")

except Exception as error:
    st.error(f"Une erreur est survenue : {error}")


