"""Main entry point for the investment application."""

from app.gui import InvestmentApp
from utils.config import CSV_FILE_PATH
from utils.data_provider import CSVDataProvider
from utils.screener import StockScreener
import strategies.buy_and_hold # AT - tady sice IDE hlásí, že je to zbytečné, ale nefungovala by factory - lze to nějkak lépe?
import strategies.periodic_rebalance
from strategies.registry import _REG as strategies


def main() -> None:
    """Run the investment GUI."""
    data_provider: CSVDataProvider = CSVDataProvider(CSV_FILE_PATH)
    screener: StockScreener = StockScreener(data_provider)
    app: InvestmentApp = InvestmentApp(screener, strategies)
    app.run()


if __name__ == "__main__":
    main()