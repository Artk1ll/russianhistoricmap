import json

def load_borders(path="data/borders.json"):
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    # Преобразуем ключи из str в int
    borders_by_year = {int(year): polys for year, polys in raw.items()}
    return borders_by_year

def load_events(path="data/events.json"):
    import json
    with open(path, "r", encoding="utf-8") as f:
        return {int(k): v for k, v in json.load(f).items()}
