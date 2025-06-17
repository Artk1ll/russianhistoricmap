import json

def load_borders(path="data/borders.json"):
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    borders_by_year = {}
    departing_by_year = {}

    for year, polys in raw.items():
        if year.startswith("_"):
            try:
                departing_by_year[int(year[1:])] = polys
            except ValueError:
                continue
        else:
            try:
                borders_by_year[int(year)] = polys
            except ValueError:
                continue

    return borders_by_year, departing_by_year

def load_events(path="data/events.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)  # Ключи остаются строками, как в JSON

def load_points_of_interest(path="data/points_of_interest.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
