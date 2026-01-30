"""
yfinance API module
===================
Package: `api`

Retrieves financial data for game publishers using yfinance.

Functions
---------
- `getPublishers`
"""


import typing
import datetime
import yfinance as yf
from . import utils, models


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

    utils.echoInfo(f"--- Début de l'extraction Yahoo finance pour {len(publishers_ids)} éditeurs ---", indent=1)

    for publisher in publishers_ids:
        utils.echoInfo(f"Récupération des données pour \"{publisher.name}\" ({publisher.symbol})...", indent=2)

        try:
            ticker = yf.Ticker(publisher.symbol)

            info: dict[str, typing.Any] = ticker.info
            symbol: str | None = utils.extractValueFromDict(info, 'symbol', None, str)
            short_name: str | None = utils.extractValueFromDict(info, 'shortName', None, str)
            long_name: str | None = utils.extractValueFromDict(info, 'longName', None, str)
            currency: str | None = utils.extractValueFromDict(info, 'currency', None, str)
            market: str | None = utils.extractValueFromDict(info, 'market', None, str)
            country: str | None = utils.extractValueFromDict(info, 'country', None, str)
            fullTimeEmployees: int | None = utils.extractValueFromDict(info, 'fullTimeEmployees', None, int)
            all_time_high: float | None = utils.extractValueFromDict(info, 'allTimeHigh', None, float)
            all_time_low: float | None = utils.extractValueFromDict(info, 'allTimeLow', None, float)
            total_cash: int | None = utils.extractValueFromDict(info, 'totalCash', None, int)
            total_debt: int | None = utils.extractValueFromDict(info, 'totalDebt', None, int)
            total_revenue: int | None = utils.extractValueFromDict(info, 'totalRevenue', None, int)

            history_dict: dict[datetime.date, models.StockValue] = {
                date.date(): models.StockValue(
                    close_price=float(row['Close']),
                    volume=int(row['Volume']),
                )
                for date, row in ticker.history(period="max").iterrows()
            }

            publisher_list.append(models.Publisher(
                used_name=publisher.name,
                symbol=symbol,
                short_name=short_name,
                long_name=long_name,
                currency=currency,
                history=history_dict,
                market=market,
                country=country,
                fullTimeEmployees=fullTimeEmployees,
                all_time_high=all_time_high,
                all_time_low=all_time_low,
                total_cash=total_cash,
                total_debt=total_debt,
                total_revenue=total_revenue,
            ))

        except Exception:
            utils.echoError(f"Erreur lors de la récupération des données pour \"{publisher.name}\" ({publisher.symbol})", indent=2)

    utils.echoInfo("--- Fin de la récupération des éditeurs sur Yahoo finance ---", indent=1)

    return publisher_list
