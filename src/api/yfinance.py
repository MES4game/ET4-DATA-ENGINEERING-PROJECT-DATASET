"""
yfinance API module
===================
Package: `api`

Retrieves financial data for game publishers using yfinance.

Functions
---------
- `getPublishers`
"""


import datetime
import yfinance as yf
from . import echo, models


def getPublishers(
        *,
        publishers_ids: list[models.PublisherId],
        ) -> list[models.Publisher]:
    """
    Retrieves financial data and stock history for tracked publishers.

    Parameters:
        publishers_ids (list[models.PublisherId]): List of publisher identities to fetch

    Returns:
        out (list[models.Publisher]): List of publishers with financial data
    """
    publisher_list: list[models.Publisher] = []

    echo.echoInfo(f"--- Début de l'extraction Yahoo finance pour {len(publishers_ids)} éditeurs ---", indent=1)

    for publisher in publishers_ids:
        echo.echoInfo(f"Récupération des données pour \"{publisher.name}\" ({publisher.symbol})...", indent=2)

        try:
            ticker = yf.Ticker(publisher.symbol)

            history_dict: dict[datetime.date, models.StockValue] = {
                date.date(): models.StockValue(
                    close_price=float(row['Close']),
                    volume=int(row['Volume']),
                )
                for date, row in ticker.history(period="max").iterrows()
            }

            publisher_list.append(models.Publisher(
                used_name=publisher.name,
                symbol=str(ticker.info.get('symbol', publisher.symbol) or publisher.symbol),
                short_name=str(ticker.info.get('shortName', publisher.name) or publisher.name),
                long_name=str(ticker.info.get('longName', publisher.name) or publisher.name),
                currency=str(ticker.info.get('currency', 'USD') or 'USD'),
                history=history_dict,
            ))

        except Exception:
            echo.echoError(f"Erreur lors de la récupération des données pour \"{publisher.name}\" ({publisher.symbol})", indent=2)

    echo.echoInfo("--- Fin de la récupération des éditeurs sur Yahoo finance ---", indent=1)

    return publisher_list
