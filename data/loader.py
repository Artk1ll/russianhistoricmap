import json

def load_borders(path="data/borders.json"):
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return {int(year): polys for year, polys in raw.items()}  # здесь можно оставить int

def load_events(path="data/events.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)  # Ключи остаются строками, как в JSON

def load_points_of_interest(path="data/points_of_interest.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
