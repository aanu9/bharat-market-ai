from datetime import datetime, timezone
import httpx

class UpstoxProvider:
    def __init__(self, token: str, instruments: dict):
        self.token, self.instruments = token, instruments

    async def quotes(self):
        if not self.token:
            return {"status":"not_connected","source":"Upstox","as_of":None,
                    "message":"Add UPSTOX_ACCESS_TOKEN and instrument keys in backend/.env.","items":[]}
        if not self.instruments:
            return {"status":"not_configured","source":"Upstox","as_of":None,
                    "message":"Add exact official Upstox instrument keys.","items":[]}
        headers = {"Accept":"application/json","Api-Version":"2.0","Authorization":f"Bearer {self.token}"}
        params = {"instrument_key":",".join(self.instruments.values())}
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get("https://api.upstox.com/v2/market-quote/quotes", headers=headers, params=params)
            response.raise_for_status()
            payload = response.json()
        reverse = {v:k for k,v in self.instruments.items()}
        items = []
        for key, q in (payload.get("data") or {}).items():
            ohlc = q.get("ohlc") or {}
            last, close = q.get("last_price"), ohlc.get("close")
            change = q.get("net_change")
            pct = (float(last)-float(close))/float(close)*100 if last is not None and close else None
            items.append({"symbol":reverse.get(key) or q.get("symbol") or key,
                "instrument_key":key,"last_price":last,"change":change,
                "change_percent":round(pct,3) if pct is not None else None,
                "open":ohlc.get("open"),"high":ohlc.get("high"),"low":ohlc.get("low"),
                "previous_close":close,"volume":q.get("volume"),
                "timestamp":q.get("timestamp") or q.get("last_trade_time")})
        return {"status":"connected","source":"Upstox API v2 snapshot",
                "as_of":datetime.now(timezone.utc).isoformat(),"items":items}
