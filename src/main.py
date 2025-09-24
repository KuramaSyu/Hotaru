import logging
from pprint import pformat, pprint
from typing import NewType
import hikari
import lightbulb
import miru

from core import Config
import ext
from services.api.anime import AnimeService
from services.impl.my_anime_list import MyAnimeListRestService

# Load config
config = Config.from_path("config.yaml")

# Create a GatewayBot instance + miru client
bot = hikari.GatewayBot(config.bot.secret)
miru_client = miru.Client(bot)
client = lightbulb.client_from_app(bot)

# Get the registry for the default context
registry = client.di.registry_for(lightbulb.di.Contexts.DEFAULT)
# Register our new dependency
registry.register_factory(AnimeService, lambda: MyAnimeListRestService(config.mal.id))
registry.register_factory(miru.Client, lambda: miru_client)


# Ensure the client will be started when the bot is run
bot.subscribe(hikari.StartingEvent, client.start)

@bot.listen(hikari.StartingEvent)
async def on_starting(_: hikari.StartingEvent) -> None:
    # Load any extensions
    await client.load_extensions_from_package(ext)
    # Start the bot - make sure commands are synced properly
    await client.start()

bot.run()