from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field






class AnimeService(ABC):

    @abstractmethod
    async def fetch_anime(
        self,
        id: int
    ) -> Dict[str, Any]:
        """
        Fetch an anime by ID, to get a detailed view.
        
        Args:
        -----
        id : int
            the mal ID of that anime    
        """
        pass

    @abstractmethod
    async def search_anime(self, query: str, include_nsfw: bool = True) -> Dict[str, Any]:
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