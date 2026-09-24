"""Reusable dashboard chrome for the impact intelligence lab."""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

APP_VERSION = "1.3"


def apply_chart(fig: go.Figure, title: str) -> go.Figure:
    fig.update_layout(
        title=dict(text=title, font=dict(size=18)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e7eef8", size=14),
        margin=dict(l=12, r=12, t=56, b=12),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25),
    )
    fig.update_xaxes(gridcolor="#314158", zerolinecolor="#314158")
    fig.update_yaxes(gridcolor="#314158", zerolinecolor="#314158")
    return fig


def show_chart(fig: go.Figure) -> None:
    st.plotly_chart(fig, width="stretch")


def kpi_row(items: list[tuple]) -> None:
    with st.container(horizontal=True):
        for item in items:
            label, value, delta = item[0], item[1], item[2]
            color = item[3] if len(item) > 3 else "normal"
            st.metric(label, value, delta=delta, delta_color=color, border=True)


def page_intro(purpose: str, questions: list[str]) -> None:
    st.markdown(purpose)
    with st.container(border=True):
        st.markdown("**Questions this page answers**")
        for question in questions:
            st.markdown(f"- {question}")


def section(title: str, note: str = "") -> None:
    st.subheader(title)
    if note:
        st.caption(note)


def callout(kind: str, message: str) -> None:
    if kind == "warning":
        st.warning(message, icon=":material/warning:")
    elif kind == "error":
        st.error(message, icon=":material/error:")
    elif kind == "success":
        st.success(message, icon=":material/check_circle:")
    else:
        st.info(message, icon=":material/info:")


def page_footer(about: str, interpret: str, limits: str, next_action: str) -> None:
    st.divider()
    st.subheader("About this view")
    left, right = st.columns(2)
    with left:
        with st.container(border=True):
            st.markdown("**How to interpret**")
            st.markdown(interpret)
        with st.container(border=True):
            st.markdown("**Recommended next action**")
            st.markdown(next_action)
    with right:
        with st.container(border=True):
            st.markdown("**About**")
            st.markdown(about)
        with st.container(border=True):
            st.markdown("**Limitations**")
            st.markdown(limits)


def severity_label(value: str) -> str:
    return {"High": "High — review first", "Medium": "Medium — review", "Low": "Low — monitor"}.get(value, value)


def status_header(backend: str, health: str, refreshed: str) -> None:
    st.markdown("### Nonprofit Impact Intelligence Lab")
    st.caption("Synthetic operating view for impact reporting, data quality, and diagnostic analytics.")
    with st.container(horizontal=True):
        st.badge("SYNTHETIC DEMO", color="violet", icon=":material/science:")
        st.badge(backend, color="blue", icon=":material/database:")
        color = {"Healthy": "green", "Watch": "orange", "Needs review": "red"}.get(health, "gray")
        st.badge(f"Data health: {health}", color=color, icon=":material/monitor_heart:")
        st.badge(f"Last refresh {refreshed}", color="gray", icon=":material/schedule:")


def sidebar_help() -> None:
    st.caption(f"Portfolio build {APP_VERSION}")
    with st.expander("How to use this demo"):
        st.markdown(
            "Start with Executive Impact, then open Data Quality for issues that need review. "
            "Use Funding Lookup and Country Operations for filtered briefings. "
            "Analytics and Migration pages are diagnostic. Exports stay on preset datasets."
        )
    st.caption(
        "Synthetic data only. Independent demonstration; not affiliated with or endorsed by buildOn."
    )


def latest_refresh(refreshes: pd.DataFrame) -> str:
    if refreshes.empty:
        return pd.Timestamp.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    stamp = pd.to_datetime(refreshes["refreshed_at"]).max()
    return pd.Timestamp(stamp).strftime("%Y-%m-%d %H:%M UTC")
