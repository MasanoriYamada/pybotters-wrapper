import pandas as pd
from pybotters.models.bybit import BybitUSDTDataStore
from pybotters_wrapper.common import DataStoreWrapper
from pybotters_wrapper.common.store import TickerStore, TradesStore, OrderbookStore
from pybotters_wrapper.bybit import BybitUSDTWebsocketChannels


class BybitUSDTTickerStore(TickerStore):
    def _normalize(self, d: dict, op: str) -> "TickerItem":
        return {"symbol": d["symbol"], "price": d["last_price"]}


class BybitUSDTTradesStore(TradesStore):
    def _normalize(self, d: dict, op: str) -> "TickerItem":
        return {
            "id": d["trade_id"],
            "symbol": d["symbol"],
            "side": d["side"].upper(),
            "price": float(d["price"]),
            "size": d["size"],
            "timestamp": pd.to_datetime(d["timestamp"]),
        }


class BybitUSDTOrderbookStore(OrderbookStore):
    def _normalize(self, d: dict, op: str) -> "TickerItem":
        return {
            "symbol": d["symbol"],
            "side": d["side"].upper(),
            "price": float(d["price"]),
            "size": float(d["size"]),
        }


class BybitUSDTDataStoreWrapper(DataStoreWrapper[BybitUSDTDataStore]):
    _WEBSOCKET_CHANNELS = BybitUSDTWebsocketChannels
    _TICKER_STORE = (BybitUSDTTickerStore, "instrument")
    _TRADES_STORE = (BybitUSDTTradesStore, "trade")
    _ORDERBOOK_STORE = (BybitUSDTOrderbookStore, "orderbook")

    def __init__(self, store: BybitUSDTDataStore = None):
        super(BybitUSDTDataStoreWrapper, self).__init__(
            store or BybitUSDTDataStore()
        )
