from pydantic import BaseModel, Field, computed_field
from typing import Dict, Optional, List

class Player(BaseModel):
    id: str = Field(..., alias="_id") 
    name: str
    pos: str
    name_searchable: str
    fantasy_points: Dict[str, float]
    
    class Config:
        validate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "ChasJa00",
                "name": "Ja'Marr Chase",
                "pos": "WR",
                "name_searchable": "jamarr chase",
                "fantasy_points": {
                    "2024": 276.0,
                    "2023": 162.72,
                    "2022": 155.4,
                    "2021": 223.6,
                }
            }
        }

    @computed_field
    @property
    def years_played(self) -> Optional[List[int]]:
        if not self.fantasy_points:
            return None
        years = sorted(int(y) for y in self.fantasy_points.keys())
        return years

    def to_mongo_dict(
        self,
        include: Optional[set[str]] = None,
        exclude: Optional[set[str]] = None
    ) -> dict:
        """Convert to MongoDB-compatible dict, with optional field control."""
        doc = self.model_dump(by_alias=True, include=include, exclude=exclude)

        return doc


class PlayerSearchResult(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    pos: str
    years_played: List[int]

    class Config:
        validate_by_name = True
