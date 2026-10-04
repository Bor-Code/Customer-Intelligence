import pandas as pd
import streamlit as st
from evidently.metric_preset import DataDriftPreset
from evidently.report import Report

def generate_drift_report(ref_data: pd.DataFrame, curr_data: pd.DataFrame) -> Report:
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=ref_data, current_data=curr_data)
    return report

def main() -> None:
    st.title("Customer Intelligence Dashboard")
    st.sidebar.header("Navigation")

    page = st.sidebar.radio("Go to", ["Home", "Data Drift Monitoring"])

    if page == "Home":
        st.write("Welcome to the Retail Customer Intelligence Platform.")
        st.write("Use the navigation bar to monitor data drift and view predictions.")

    elif page == "Data Drift Monitoring":
        st.header("Evidently Data Drift Report")

        ref_data = pd.DataFrame(
            {
                "Recency": [10, 20, 30],
                "Frequency": [1, 2, 3],
                "Monetary": [100.0, 200.0, 300.0],
            }
        )
        curr_data = pd.DataFrame(
            {
                "Recency": [12, 22, 35],
                "Frequency": [1, 2, 4],
                "Monetary": [110.0, 210.0, 350.0],
            }
        )

        if st.button("Generate Report"):
            with st.spinner("Calculating data drift..."):
                report = generate_drift_report(ref_data, curr_data)
                st.components.v1.html(report.get_html(), height=1000, scrolling=True)

if __name__ == "__main__":
    main()
