# BHARAT MARKET AI — runnable starter

Web dashboard + Expo mobile client + FastAPI backend.

## Data integrity
No fabricated prices. Without valid credentials and exact instrument mappings the dashboard says NOT CONNECTED. The first-version market bias is an explainable snapshot score, not a calibrated probability or investment advice.

## Requirements
Node.js 20+, Python 3.11+. For mobile preview, install Expo Go.

## Configure Upstox
Copy `backend/.env.example` to `backend/.env`, then set `UPSTOX_ACCESS_TOKEN` and `UPSTOX_INSTRUMENT_KEYS`. The latter is JSON mapping display labels to exact instrument keys from the official Upstox instrument master, e.g.
```json
{"NIFTY 50":"NSE_INDEX|<official-key>","BANK NIFTY":"NSE_INDEX|<official-key>","INDIA VIX":"NSE_INDEX|India VIX"}
```
Do not guess instrument keys. Upstox quote snapshots: https://upstox.com/developer/api-documentation/get-full-market-quote/
Real-time WebSocket V3: https://upstox.com/developer/api-documentation/v3/get-market-data-feed/

## Run backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```
Health: http://localhost:8000/api/health — API docs: http://localhost:8000/docs

## Run web
```bash
cd web
npm install
cp .env.example .env
npm run dev
```
Open http://localhost:5173

## Run mobile
```bash
cd mobile
npm install
```
Copy `.env.example` to `.env`, set `EXPO_PUBLIC_API_URL` to your computer's LAN IP and port 8000 (not localhost on a physical phone), then `npx expo start`.

## Included
- Authenticated Upstox REST quote snapshots.
- GDELT DOC 2.0 global news discovery (keyless public endpoint; rate limits apply).
- Market source/status/freshness labels.
- Simple transparent directional snapshot score.
- Responsive React dashboard and Expo companion app.

## Production work still needed
OAuth/token refresh and secure credential storage; Upstox V3 streaming and reconnect logic; instrument master ingestion; licensed global/index feeds; historical candle storage; validated horizon-specific ML with walk-forward testing and transaction costs; PostgreSQL/Redis/auth/alerts/monitoring; SEBI, exchange licensing and privacy review. Exchange data display and redistribution require appropriate permissions. This starter is not a finished regulated financial product.
