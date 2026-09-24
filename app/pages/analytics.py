import sys
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from analytics.methods import bounded_forecast, diagnostic, iqr_flags, trend
from app.queries import table
from app.ui import apply_chart, callout, kpi_row, page_footer, page_intro, section, show_chart

page_intro(
    "Spot synthetic trends, anomaly markers, and a bounded one-period forecast. These are diagnostic indicators, not causes or commitments.",
    [
        "Is period-average enrollment rising, flat, or falling?",
        "Which recent periods sit outside an IQR fence?",
        "What one-period range does the bounded forecast show, and what might be contributing?",
    ],
)
enrollment = table("fact_enrollment")
submissions = table("fact_data_submission")
series = trend(enrollment)
forecast = bounded_forecast(enrollment)
change = float(series["pct_change"].iloc[-1]) if len(series) else 0.0
stale_rate = float(submissions["is_stale"].mean()) if len(submissions) else 0.0
flags = iqr_flags(series["enrolled"])
series = series.copy()
series["anomaly"] = flags.reindex(series.index).fillna(False).to_numpy()
kpi_row(
    [
        ("Latest period average", f"{series.enrolled.iloc[-1]:,.0f}" if len(series) else "n/a", f"{change:+.1%}"),
        ("Rolling 3-period mean", f"{series.rolling_3.iloc[-1]:,.0f}" if len(series) else "n/a", None),
        ("IQR anomaly periods", f"{int(series.anomaly.sum()):,}", "Marker, not a cause", "off"),
        ("Stale submission rate", f"{stale_rate:.0%}", "Possible contributor", "off"),
    ]
)
section("Trend and rolling signal")
fig = go.Figure()
fig.add_trace(go.Scatter(x=series.period_id, y=series.enrolled, name="Period average", mode="lines+markers"))
fig.add_trace(go.Scatter(x=series.period_id, y=series.rolling_3, name="Rolling 3", mode="lines"))
marked = series[series.anomaly]
if len(marked):
    fig.add_trace(go.Scatter(x=marked.period_id, y=marked.enrolled, name="IQR anomaly", mode="markers", marker=dict(size=12, symbol="diamond")))
show_chart(apply_chart(fig, "Enrollment trend with anomaly markers"))
section("Bounded forecast", forecast.get("method", forecast.get("reason", "")))
if forecast.get("available"):
    kpi_row(
        [
            ("Forecast estimate", f"{forecast['estimate']:,.0f}", f"Period {forecast['forecast_period_id']}"),
            ("Lower bound", f"{forecast['lower_bound']:,.0f}", None),
            ("Upper bound", f"{forecast['upper_bound']:,.0f}", None),
            ("Observations", f"{forecast['observations']}", None),
        ]
    )
    st.caption(forecast.get("label", ""))
else:
    callout("warning", forecast.get("reason", "Forecast unavailable"))
callout("warning", diagnostic(change, stale_rate, 0.03) + " This is not a causal claim.")
section("Recent periods")
st.dataframe(series.tail(10), width="stretch", hide_index=True)
page_footer(
    "The forecast fits an ordinary least-squares line to recent period means and shows a residual uncertainty band.",
    "Use the band, not the point estimate. An IQR marker means the period is unusual relative to the series. A stale-rate note is a possible contributor to investigate.",
    "The forecast is illustrative. It does not predict real enrollment, and coincidence with stale data is not proof of a cause.",
    "If a marker and a stale-rate note appear together, open Data Quality and Country Operations for the same periods.",
)
