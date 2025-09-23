from lightbulb import Loader, invoke
import lightbulb
import miru

from services.impl.my_anime_list import MyAnimeListRestService
from views import AnimeNavigationBuilder

loader = Loader()

@loader.command
class Anime(
    lightbulb.SlashCommand,
    name="anime",
    description="Get information about an anime",
):
    search = lightbulb.string("search", "What anime?")

    @invoke
    async def invoke(
        self, 
        ctx: lightbulb.Context, 
        anime_service: MyAnimeListRestService, 
        client: miru.Client
    ) -> None:
            nav_getter = AnimeNavigationBuilder(self.search, anime_service)
            navigator = await nav_getter.get_navigator()

            builder = await navigator.build_response_async(client)
            await builder.create_initial_response(ctx.interaction)
            client.start_view(navigator)