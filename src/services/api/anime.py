from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any, Sequence
from dataclasses import dataclass, field

from models.anime import Anime, PartialAnime






class AnimeService(ABC):

    @abstractmethod
    async def fetch_anime(
        self,
        id: int
    ) -> Anime:
        """
        Fetch an anime by ID, to get a detailed view.
        
        Args:
        -----
        id : int
            the mal ID of that anime    
        """
        pass

    @abstractmethod
    async def search_anime(self, query: str, include_nsfw: bool = True) -> Sequence[PartialAnime]:
        """search for anime by name

        Args:
        -----
        query : str
            the query to search for
        include_nsfw : bool
            whether to include nsfw results

        Returns:
        --------
        Dict[str, Any]
            the response json
        """
        pass