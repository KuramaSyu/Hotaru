from typing import Sequence, List
from hikari import Embed
from miru.ext import nav
from abc import ABC, abstractmethod

from models.anime import PartialAnime
from services.api.anime import AnimeService

class NavigatorGetter(ABC):

    @abstractmethod
    async def get_navigator(self) -> nav.NavigatorView:
        ...
    

class AnimeNavigationBuilder(NavigatorGetter):
    def __init__(self, anime_name: str, anime_service: AnimeService):
        self.anime_name = anime_name
        self.anime_service = anime_service
        self.animes: Sequence[PartialAnime] = []

    async def search_anime(self) -> Sequence[PartialAnime]:
        return await self.anime_service.search_anime(self.anime_name, include_nsfw=True)

    def _make_pages(self) -> List[Embed]:
        pages = []
        for anime in self.animes:
            page = Embed(
                title=anime.title,
                description=anime.synopsis or "No synopsis available.",
                url=f"https://myanimelist.net/anime/{anime.id}",
            )
            page.set_image(anime.main_picture.medium)
            pages.append(page)
        return pages

    async def get_navigator(self) -> nav.NavigatorView:
        self.animes = await self.search_anime()
        pages = self._make_pages()
        return nav.NavigatorView(pages=pages, autodefer=True)
    