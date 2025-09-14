# Import the libraries
import hikari
import lightbulb
from core import Config
import ext


# Create a GatewayBot instance
config = Config.from_path("config.yaml")
bot = hikari.GatewayBot(config.bot.secret)
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