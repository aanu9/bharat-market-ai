from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.providers.upstox import UpstoxProvider
from app.providers.news import GdeltNewsProvider
from app.analysis import directional_outlook

app = FastAPI(title="BHARAT MARKET AI API",version="0.1.0",
 description="Market data and news intelligence. No fabricated prices or uncalibrated probabilities.")
origins=[x.strip() for x in settings.frontend_origins.split(",") if x.strip()]
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,
 allow_methods=["*"],allow_headers=["*"])
market=UpstoxProvider(settings.upstox_access_token,settings.instruments)
news_provider=GdeltNewsProvider()

@app.get("/api/health")
async def health():
    return {"status":"ok","service":settings.app_name,"version":"0.1.0"}

@app.get("/api/market/quotes")
async def market_quotes():
    try: return await market.quotes()
    except Exception as exc: raise HTTPException(502,detail=f"Market provider error: {type(exc).__name__}: {exc}")

@app.get("/api/market/outlook")
async def market_outlook():
    try:
        q=await market.quotes()
        return {"data_status":q["status"],"source":q.get("source"),
                "outlook":directional_outlook(q.get("items",[]))}
    except Exception as exc: raise HTTPException(502,detail=f"Market provider error: {type(exc).__name__}: {exc}")

@app.get("/api/news")
async def news(query: str=Query('(India OR NIFTY OR RBI OR "Federal Reserve" OR crude oil OR tariffs)',max_length=300),
 timespan: str=Query(settings.gdelt_timespan,pattern="^(1h|3h|6h|12h|24h|48h|7d)$")):
    try: return await news_provider.headlines(query,timespan)
    except Exception as exc: raise HTTPException(502,detail=f"News provider error: {type(exc).__name__}: {exc}")
