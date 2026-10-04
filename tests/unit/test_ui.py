from unittest.mock import MagicMock, patch

import pandas as pd

from ci.ui.dashboard import generate_drift_report, main

def test_generate_drift_report() -> None:
    ref_data = pd.DataFrame({"A": [1, 2, 3]})
    curr_data = pd.DataFrame({"A": [2, 3, 4]})

    report = generate_drift_report(ref_data, curr_data)

    assert report is not None
    html_output = report.get_html()
    assert isinstance(html_output, str)
    assert len(html_output) > 0

@patch("ci.ui.dashboard.st")
def test_dashboard_main_home(mock_st: MagicMock) -> None:
    mock_st.sidebar.radio.return_value = "Home"
    main()
    mock_st.title.assert_called_once_with("Customer Intelligence Dashboard")
    mock_st.write.assert_called()

@patch("ci.ui.dashboard.st")
@patch("ci.ui.dashboard.generate_drift_report")
def test_dashboard_main_drift(mock_generate: MagicMock, mock_st: MagicMock) -> None:
    mock_st.sidebar.radio.return_value = "Data Drift Monitoring"
    mock_st.button.return_value = True

    mock_report = MagicMock()
    mock_report.get_html.return_value = "<html></html>"
    mock_generate.return_value = mock_report

    main()

    mock_st.header.assert_called_once_with("Evidently Data Drift Report")
    mock_generate.assert_called_once()
    mock_st.components.v1.html.assert_called_once_with(
        "<html></html>", height=1000, scrolling=True
    )
