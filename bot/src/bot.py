import hikari
import miru
import lightbulb
from db_common import db, Server, User

with open("/run/secrets/bot_token", "r") as token:
    bot = lightbulb.BotApp(token.read(), banner=None)
miru.install(bot)


@bot.listen()
async def on_ready(event: hikari.StartedEvent):
    my_guilds = await event.app.rest.fetch_my_guilds()
    for guild in my_guilds:
        if db.get_server(guild.id) is None:
            server = Server()
            server.id = guild.id
            server.name = guild.name
            db.add_server(server)


@bot.listen()
async def on_message(event: hikari.MessageEvent):
    message = await event.app.rest.fetch_message(event.channel_id, event.message_id)
    server = db.get_server(message.guild_id)
    author = db.get_user(message.author.id)

    if author is None:
        return

    if author.modify_exp(1 * server.multiplier):
        db.update_user(author * server.multiplier)


bot.run()
