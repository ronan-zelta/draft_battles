from fastapi import APIRouter, HTTPException

from repository import PlayerRepository
from models import Player, PlayerSearchResult

router = APIRouter()

player_repository = PlayerRepository()

@router.get("/player/{uid}")
async def get_player(uid: str) -> Player:
    player = await player_repository.get_player(uid)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

@router.get("/player/{uid}/{year}")
async def get_player_year_points(uid: str, year: int) -> float | None:
    player = await player_repository.get_player(uid)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    if str(year) not in player.fantasy_points:
        return None
    return player.fantasy_points[str(year)]

@router.get("/search/{pos}")
async def search_players(q: str, pos: str) -> list[PlayerSearchResult]:
    players = await player_repository.search_players(q, pos)
    return players

@router.get("/search")
async def search_players(q: str) -> list[PlayerSearchResult]:
    players = await player_repository.search_players(q)
    return players
