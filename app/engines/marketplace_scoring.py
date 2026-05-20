import json
from pathlib import Path

SCORE_DIR = Path("data/scoring")
SCORE_FILE = SCORE_DIR / "marketplace_scores.json"

DEFAULT_SCORES = {
    "shopify": {
        "success_rate": 100,
        "profit_score": 50,
        "api_health": 100,
        "sales_score": 50,
        "return_rate_score": 100
    }
}


def _ensure():
    SCORE_DIR.mkdir(parents=True, exist_ok=True)

    if not SCORE_FILE.exists():
        SCORE_FILE.write_text(
            json.dumps(DEFAULT_SCORES, indent=2),
            encoding="utf-8"
        )


def get_scores():
    _ensure()
    return json.loads(
        SCORE_FILE.read_text(encoding="utf-8")
    )


def calculate_marketplace_score(data: dict):

    success_rate = float(data.get("success_rate",100))
    profit_score = float(data.get("profit_score",50))
    api_health = float(data.get("api_health",100))
    sales_score = float(data.get("sales_score",50))
    return_rate_score = float(data.get("return_rate_score",100))

    score = round(
        (
            success_rate*0.30+
            profit_score*0.25+
            api_health*0.20+
            sales_score*0.15+
            return_rate_score*0.10
        ),2
    )

    return score


def update_marketplace(channel:str,data:dict):

    scores = get_scores()

    scores[channel] = {
        **data,
        "score": calculate_marketplace_score(data)
    }

    SCORE_FILE.write_text(
        json.dumps(scores,indent=2),
        encoding="utf-8"
    )

    return {
        "ok":True,
        "channel":channel,
        "score":scores[channel]
    }


def get_best_marketplaces(limit=5):

    scores=get_scores()

    items=[]

    for k,v in scores.items():
        items.append({
            "channel":k,
            "score":v.get("score",0)
        })

    items=sorted(
        items,
        key=lambda x:x["score"],
        reverse=True
    )

    return {
        "ok":True,
        "marketplaces":items[:limit]
    }

