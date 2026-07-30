"""Project configuration and UI constants."""

from __future__ import annotations
from pathlib import Path

# Stock metric labels and their corresponding data keys.
METRICS: list[tuple[str, str]] = [
    ("Price/Earnings", "pe"),
    ("Price/Sales", "ps"),
    ("Price/Book", "pb"),
    ("Price/Free Cash Flow", "pfcf"),
    ("Current Ratio", "current_ratio"),
    ("Quick Ratio", "quick_ratio"),
    ("Debt to Equity", "debt_to_equity"),
    ("Return on Equity", "roe"),
    ("Return on Assets", "roa"),
    ("Return on Tangible Equity", "rote"),
    ("EBITDA Margin", "ebitda_margin"),
]

# Categories grouping related metrics for UI filtering.
METRIC_CATEGORIES: dict[str, list[tuple[str, str]]] = {
    "Valuation Metrics": METRICS[0:4],
    "Debt Metrics": METRICS[4:7],
    "Efficiency Metrics": METRICS[7:11],
}

# Path to the static CSV file containing quarterly data.
# Resolved relative to the project root so the app runs from any directory.
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
CSV_FILE_PATH: Path = PROJECT_ROOT / "snp500.csv"

# Main window dimensions (width, height).
WINDOW_WIDTH: int = 1300
WINDOW_HEIGHT: int = 750

# UI color settings.
BACKGROUND_COLOR: str = "lightgrey"
GRAPH_COLOR: str = "red"
