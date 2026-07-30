"""Main entry point for the investment application."""

from app.gui import InvestmentApp
from utils.config import CSV_FILE_PATH
from utils.data_provider import CSVDataProvider
from utils.screener import StockScreener
from strategies import REG as strategies


def main() -> None:
    """Run the investment GUI."""
    data_provider = CSVDataProvider(CSV_FILE_PATH)
    screener = StockScreener(data_provider)
    app = InvestmentApp(screener, strategies)
    app.run()


if __name__ == "__main__":
    main()
