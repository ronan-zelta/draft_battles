import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

from models import Player
from utils import make_name_searchable

load_dotenv()


class PlayerRepository:
    def __init__(self,
                 uri: str = None,
                 db_name: str = None,
                 collection_name: str = None):
        uri = uri or os.getenv("MONGO_URI")
        db_name = db_name or os.getenv("MONGO_DB")
        collection_name = collection_name or "players"

        self.client = AsyncIOMotorClient(uri)
        self.collection = self.client[db_name][collection_name]


    async def create_player(self, player: Player) -> Player:
        """Create a new player"""
        result = await self.collection.insert_one(player.model_dump(by_alias=True))
        player.id = str(result.inserted_id)
        return player
    

    async def get_player(self, uid: str) -> Player:
        """Get a player by ID"""
        result = await self.collection.find_one({"_id": uid})
        return Player(**result) if result else None
    

    async def search_players(self, search_term: str, pos: str, limit: int = 20) -> list[Player]:
        if not search_term:
            return []
        
        pattern = f"\\b{make_name_searchable(search_term)}"
        query = {"name_searchable": {"$regex": pattern, "$options": "i"}}
        if pos:
            query["pos"] = pos.upper()
        cursor = self.collection.find(query)

        if limit:
            cursor = cursor.limit(limit)
        
        players = []
        async for doc in cursor:
            players.append(Player(**doc))
        
        return players
