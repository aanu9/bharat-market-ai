from typing import Optional

def rsi(closes: list[float], period: int = 14) -> Optional[float]:
    if len(closes) <= period: return None
    d = [closes[i]-closes[i-1] for i in range(1,len(closes))]
    gains = [max(x,0) for x in d[-period:]]
    losses = [abs(min(x,0)) for x in d[-period:]]
    avg_gain, avg_loss = sum(gains)/period, sum(losses)/period
    if avg_loss == 0: return 100.0
    return round(100-(100/(1+avg_gain/avg_loss)),2)

def ema(values: list[float], period: int) -> Optional[float]:
    if len(values) < period: return None
    alpha = 2/(period+1)
    result = sum(values[:period])/period
    for value in values[period:]: result = alpha*value+(1-alpha)*result
    return round(result,4)

def directional_outlook(quotes: list[dict]) -> dict:
    valid = [q for q in quotes if isinstance(q.get("change_percent"),(int,float))]
    if not valid:
        return {"status":"insufficient_data","label":"UNAVAILABLE","score":None,
          "confidence":"Unavailable","bullish_probability":None,"bearish_probability":None,
          "sideways_probability":None,
          "explanation":["Connect a licensed market-data provider and configure index instruments."],
          "method":"No score calculated because current quote data is unavailable."}
    avg = sum(q["change_percent"] for q in valid)/len(valid)
    score = max(-100,min(100,round(avg*20,1)))
    label = "BULLISH" if score>12 else "BEARISH" if score< -12 else "MIXED / SIDEWAYS"
    return {"status":"calculated","label":label,"score":score,
      "confidence":"Low" if len(valid)<3 else "Moderate",
      "bullish_probability":None,"bearish_probability":None,"sideways_probability":None,
      "explanation":[f"Average change across {len(valid)} configured instruments: {avg:.3f}%.",
        "This is a snapshot breadth score, not a calibrated forecast.",
        "Global macro factors, derivatives positioning and historical validation are not yet included."],
      "method":"Clipped average quote percentage change × 20. Not a probability or trading signal."}
