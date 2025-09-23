from lightbulb import Loader, invoke
import lightbulb

loader = Loader()

@loader.command
class Anime(
    lightbulb.SlashCommand,
    name="anime",
    description="Get information about an anime",
):
    @invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await ctx.respond("This is a placeholder for the anime command.")