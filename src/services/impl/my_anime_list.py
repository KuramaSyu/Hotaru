import asyncio
from typing import Sequence, List, Optional, Dict
from urllib.parse import urlencode
from datetime import datetime
from pprint import pformat as pf
import logging
from enum import Enum
from copy import copy, deepcopy
from pprint import pprint
import traceback

import aiohttp
import asyncio
from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from fuzzywuzzy import fuzz # type: ignore
from expiring_dict import ExpiringDict # type: ignore
from pprint import pformat

from models.anime import PartialAnime, Anime
from services.api import AnimeService

log = logging.getLogger(__name__)


@dataclass
class SearchEntry(DataClassJsonMixin):
    node: PartialAnime

@dataclass
class MyAnimeListSearchRoot(DataClassJsonMixin):
    data: List[SearchEntry]

class MALRatings(Enum):
    g = "G - All Ages"
    pg = "PG - Children"
    pg_13 = "PG-13 - Teens 13 or older"
    r = "R - 17+ (violence & profanity) "
    r_plus = "R+ - Mild Nudity 17+"
    rx = "Rx - Hentai 18+"




class MALTypes(Enum):
    ANIME = 1
    MANGA = 2

class MyAnimeListRestService(AnimeService):
    """Wrapper for MyAnimeList API Endpoint"""
    client_id: str = ""
    TTL = 60*60
    response_cache = ExpiringDict(ttl=TTL)


    def __init__(
        self,
        client_id: str,
    ):
        """A wrapper for the Non-user based mal api endpoints (-> no oauth needed)"""
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.INFO)
        self._id = client_id
        self._base_url = r"https://api.myanimelist.net/v2"
        self._session: Optional[aiohttp.ClientSession] = None

    @classmethod
    def set_credentials(cls, client_id: str) -> None:
        """"set the client id"""
        cls.client_id = client_id

    @property
    def session(self) -> aiohttp.ClientSession:
        """Get AioHTTP session by creating it if it doesn't already exist"""
        if not self._session or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def _make_request(
        self,
        endpoint: str,
        value: Optional[str] = None,
        optional_query: Dict[str, str] | None = None,
    ) -> str:
        query = None
        if value and not value.startswith("/"):
            value = "/" + value
        if optional_query:
            query = f"?{urlencode(optional_query)}"
        url = f"{self._base_url}/{endpoint}{value or ''}{query or ''}"
        async with self.session.get(url, headers=self.headers) as resp:
            json = await resp.text()
        if self._session:
            await self._session.close()
        self.log.debug(f"request: {url}")
        self.log.debug(f"response: {pf(json)}")
        if not resp.ok:
            raise RuntimeError(f"{url} returned status code {resp.status}")
        return json

    @property
    def headers(self) -> Dict[str, str]:
        if not self._id:
            raise RuntimeError("Client id has to be passed into the constructor or in the .env file under key `ID`")
        return {"X-MAL-CLIENT-ID": self._id}

    async def fetch_anime(
        self,
        id: int
    ) -> Anime:
        """fetch an Anime by it's ID
        
        Args:
        -----
        id : int
            the mal ID of that anime
        """
        fields = (
            "id,title,main_picture,alternative_titles,"
            "start_date,end_date,synopsis,mean,rank,popularity,"
            "num_list_users,num_scoring_users,nsfw,created_at,"
            "updated_at,media_type,status,genres,my_list_status,"
            "num_episodes,start_season,broadcast,source,"
            "average_episode_duration,rating,pictures,background,"
            "related_anime,related_manga,recommendations,studios,statistics,"
            "average_episode_duration,opening_themes,ending_themes"
        )
        resp = await self._make_request(
            endpoint="anime",
            value=str(id),
            optional_query={"fields": fields}
        )
        return Anime.from_json(resp) 

    async def _search(self) -> None:
        pass

    async def search_anime(
        self, 
        query: str, 
        include_nsfw: bool = True, 
        fallback: bool = False
    ) -> Sequence[PartialAnime]:
        """search for anime by name

        Args:
        -----
        query : str
            the query to search for
        include_nsfw : bool
            whether to include nsfw results
        fallback : bool
            whether or not to limit the query to 50 chars
        Returns:
        --------
        Dict[str, Any]
            the response json
        """
        try:
            resp = self.response_cache[query]
            return deepcopy(resp)
        except KeyError:
            pass
        fields = (
            "id,title,main_picture,alternative_titles,"
            "start_date,end_date,synopsis,mean,rank,popularity,"
            "num_list_users,num_scoring_users,nsfw,created_at,"
            "updated_at,media_type,status,genres,my_list_status,"
            "num_episodes,start_season,broadcast,source,"
            "average_episode_duration,rating,pictures,background,"
            "related_anime,related_manga,recommendations,studios,statistics,"
            "average_episode_duration,opening_themes,ending_themes"
        )
        a = datetime.now()
        kwargs = {"nsfw": "true" if include_nsfw else "false"}
        try:
            resp = await self._make_request(
                endpoint="anime", 
                optional_query={
                    "q": query, 
                    "fields":fields, 
                    "limit":"50", 
                    **kwargs
            })
            parsed = MyAnimeListSearchRoot.from_json(resp)

        except RuntimeError as e:
            if fallback:
                log.warning(f"Error while fetching anime - title len = {len(query)}")
                log.warning(traceback.format_exc())
                return []
            else:
                log.warning(f"search again with nsfw for title {query}")
                return await self.search_anime(query[:50], include_nsfw, True)
        log.info(f"fetched {len(parsed.data)} anime in {(datetime.now() - a).total_seconds():.2f}s")
        self.response_cache.ttl(query, deepcopy(resp), self.TTL)
        return [entry.node for entry in parsed.data]