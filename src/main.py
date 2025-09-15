# Import the libraries
import hikari
import lightbulb
import miru

from core import Config
import ext

# Load config
config = Config.from_path("config.yaml")

# Create a GatewayBot instance + miru client
bot = hikari.GatewayBot(config.bot.secret)
miru_client = miru.Client(bot)
client = lightbulb.client_from_app(bot)

# Ensure the client will be started when the bot is run
bot.subscribe(hikari.StartingEvent, client.start)

@bot.listen(hikari.StartingEvent)
async def on_starting(_: hikari.StartingEvent) -> None:
    # Load any extensions
    await client.load_extensions_from_package(ext)
    # Start the bot - make sure commands are synced properly
    await client.start()

bot.run()