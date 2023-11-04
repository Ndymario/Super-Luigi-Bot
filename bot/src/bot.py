import hikari
import miru
import lightbulb
from db_common import db, Server, User

with open("/run/secrets/bot_token", "r") as token:
    bot = lightbulb.BotApp(token.read(), banner=None, intents=hikari.Intents.GUILD_MEMBERS)
miru.install(bot)


@bot.command
@lightbulb.command("stats", "Get your stats in the server")
@lightbulb.implements(lightbulb.SlashCommand)
async def reload(ctx: lightbulb.Context) -> None:
    await ctx.respond(db.get_user(ctx.author.id), flags=hikari.MessageFlag.EPHEMERAL)


@bot.listen()
async def on_ready(event: hikari.StartedEvent):
    my_guilds = await event.app.rest.fetch_my_guilds()
    for guild in my_guilds:
        if db.get_server(guild.id) is None:
            server = Server()
            server.id = guild.id
            server.name = guild.name
            db.add_server(server)
            async for member in event.app.rest.fetch_members(guild.id):
                if db.get_user(member.id) is None:
                    user = User()
                    user.id = member.id
                    user.name = member.global_name
                    user.exp = 0
                    user.total_exp = 0
                    user.level = 0
                    db.add_user(user, guild.id)


bot.run()
