import re

def make_name_searchable(name: str) -> str:
    name_searchable = re.sub(r"[^a-z ]", "", name.lower()).strip()
    name_searchable = re.sub(r"\s+", " ", name_searchable)
    return name_searchable