# Import the libraries
import hikari
import lightbulb
from core import Config


# Create a GatewayBot instance
config = Config.from_path("../config.yaml")
bot = hikari.GatewayBot(config.bot.secret)
client = lightbulb.client_from_app(bot)

# Ensure the client will be started when the bot is run
bot.subscribe(hikari.StartingEvent, client.start)

# Register the command with the client
@client.register()
class Ping(
    # Command type - builtins include SlashCommand, UserCommand, and MessageCommand
    lightbulb.SlashCommand,
    # Command declaration parameters
    name="ping",
    description="checks the bot is alive",
):
    # Define the command's invocation method. This method must take the context as the first
    # argument (excluding self) which contains information about the command invocation.
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        # Send a message to the channel the command was used in
        await ctx.respond("Pong!")

# Run the bot
# Note that this is blocking meaning no code after this line will run
# until the bot is shut off
bot.run()