from datetime import datetime, timezone
import httpx

class GdeltNewsProvider:
    async def headlines(self, query, timespan="24h"):
        params = {"query":query,"mode":"ArtList","format":"json","maxrecords":30,
                  "timespan":timespan,"sort":"DateDesc"}
        async with httpx.AsyncClient(timeout=20, headers={"User-Agent":"BharatMarketAI/0.1"}) as client:
            response = await client.get("https://api.gdeltproject.org/api/v2/doc/doc", params=params)
            response.raise_for_status()
            data = response.json()
        seen, articles = set(), []
        for a in data.get("articles", []):
            title, url = (a.get("title") or "").strip(), a.get("url")
            if not title or title.casefold() in seen: continue
            seen.add(title.casefold())
            articles.append({"title":title,"url":url,"source":a.get("domain") or "GDELT indexed source",
                "published_at":a.get("seendate"),"country":a.get("sourceCountry"),
                "language":a.get("language"),"tone":a.get("tone"),
                "sentiment":"unclassified","impact":"Requires verification against market data and context."})
        return {"status":"connected","source":"GDELT DOC 2.0",
                "as_of":datetime.now(timezone.utc).isoformat(),"articles":articles}
