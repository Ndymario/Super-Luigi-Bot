import hikari
import lightbulb
from ..db_common import db

exp_plugin = lightbulb.Plugin("EXP")


@exp_plugin.command
@lightbulb.command("stats", "Get your stats in this server")
@lightbulb.implements(lightbulb.SlashCommand)
async def reload(ctx: lightbulb.Context) -> None:
    user = db.get_user(ctx.author.id, ctx.guild_id)
    guild = await ctx.app.rest.fetch_guild(ctx.guild_id)
    response = hikari.Embed(title=f"Here are your stats for {guild.name}",
                            description=f"{user}")
    await ctx.respond("", flags=hikari.MessageFlag.EPHEMERAL)


def load(bot):
    bot.add_plugin(exp_plugin)


def unload(bot):
    bot.remove_plugin(exp_plugin)
