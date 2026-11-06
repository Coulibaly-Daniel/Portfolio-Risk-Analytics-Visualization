import plotly.express as px
import pandas as pd


def plot_portfolio_vs_benchmark(portfolio_returns, benchmark_returns):

    # Alignement des rendements sur les mêmes dates
    data = pd.concat(
        [
            portfolio_returns.rename("Portfolio"),
            benchmark_returns.rename("Benchmark")
        ],
        axis=1
    ).dropna()

    # Normalisation en base 100
    performance = (1 + data).cumprod() * 100

    fig = px.line(
        performance,
        x=performance.index,
        y=["Portfolio", "Benchmark"],
        title="Portfolio vs Benchmark Performance"
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Performance (Base 100)",
        template="plotly_white",
        hovermode="x unified",
        legend_title=""
    )

    return fig

def plot_portfolio_drawdown(drawdown):

    fig = px.area(
        x=drawdown.index,
        y=drawdown.values * 100,
        title="Portfolio Drawdown Evolution"
    )

    fig.update_traces(
        fill="tozeroy",
        line=dict(width=1.5),
        hovertemplate="Date : %{x}<br>Drawdown : %{y:.2f}%<extra></extra>"
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Drawdown (%)",
        template="plotly_white",
        hovermode="x unified"
    )

    return fig

def plot_sector_allocation(portfolio):

    sector_weights = (
        portfolio.groupby("Sector")["Weight"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        sector_weights,
        names="Sector",
        values="Weight",
        hole=0.5,
        title="Portfolio Sector Allocation"
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="%{label}<br>Weight: %{value:.2%}<extra></extra>"
    )

    fig.update_layout(
        template="plotly_white"
    )

    return fig

def plot_geographic_allocation(portfolio):
    country_weights = (
        portfolio.groupby("Country")["Weight"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        country_weights,
        names="Country",
        values="Weight",
        hole=0.5,
        title="Portfolio Geographic Allocation"
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="%{label}<br>Weight: %{value:.2%}<extra></extra>"
    )

    fig.update_layout(template="plotly_white")

    return fig

def plot_risk_contribution(risk_data):

    fig = px.bar(
        risk_data,
        x="Ticker",
        y=["Weight", "Risk Contribution"],
        barmode="group",
        title="Portfolio Weight vs Risk Contribution",
        labels={
            "value": "Percentage",
            "variable": "Metric",
            "Ticker": "Asset"
        },
        color_discrete_sequence=["#636EFA", "#EF553B"]
    )

    fig.update_layout(
        template="plotly_white",
        yaxis_tickformat=".0%",
        legend_title_text=""
    )

    return fig
