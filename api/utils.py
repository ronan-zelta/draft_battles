import re

def make_name_searchable(name: str) -> str:
    name_searchable = re.sub(r"[^a-z ]", "", name.lower()).strip()
    name_searchable = re.sub(r"\s+", " ", name_searchable)
    return name_searchable

def get_position_query(pos: str) -> dict:
    match pos.upper():
        case "QB":
            return {"pos": "QB"}
        case "RB":
            return {"pos": "RB"}
        case "WR":
            return {"pos": "WR"}
        case "TE":
            return {"pos": "TE"}
        case "FLEX":
            return {"pos": {"$in": ["RB", "WR", "TE"]}}
        case "SFLX":
            return {"pos": {"$in": ["QB", "RB", "WR", "TE"]}}
        case _:
            raise ValueError(f"Invalid position: {pos}")
        