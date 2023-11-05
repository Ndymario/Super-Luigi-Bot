import math
from datetime import datetime
from pocketbase import PocketBase


class Item:
    pass


class User:
    def __init__(self, user_id: int, username: str = None, stats: dict = None, birthday: datetime = None,
                 items: [Item] = None, preferences: dict = None, pb_id: int = None):
        self.user_id = user_id
        self.username = username
        self.stats = stats
        self.birthday = birthday
        self.items = items
        self.preferences = preferences
        self.pb_id = pb_id

    @classmethod
    def get_user(cls, user_id):
        user = db.get_pb_user(user_id)

        if user is None:
            return cls(user_id, pb_id=user.id)

        return cls(user_id, user.username, user.stats, user.birthday, user.items, user.preferences, int(user.id))

    def save(self):
        if db.get_pb_user(self.pb_id) is None:
            db.client.collection("users").create({
                "username": self.username,
                "user_id": self.user_id,
                "stats": self.stats,
                "birthday": self.birthday,
                "preferences": self.preferences,
                "inventory": self.items
            })
            return

        db.client.collection("users").update(str(self.pb_id), {
            "username": self.username,
            "user_id": self.user_id,
            "stats": self.stats,
            "birthday": self.birthday,
            "preferences": self.preferences,
            "inventory": self.items
        })

    def modify_exp(self, exp: int, guild_id: int):
        exp = math.floor(exp)
        if self.stats[guild_id][0] + exp < 0:
            return False

        self.stats[guild_id][0] += exp
        # Lifetime EXP should not be affected by purchasing things
        if exp > 0:
            self.stats[guild_id][1] += exp

        return True


class Server:
    def __init__(self, server_id: int, name: str = None, members: [User] = None, items: [Item] = None,
                 tags: dict = None, levels: dict = None, multiplier: int = None, pb_id: int = None):
        self.server_id = server_id
        self.name = name
        self.members = members
        self.items = items
        self.tags = tags
        self.levels = levels
        self.multiplier = multiplier
        self.pb_id = pb_id

    @classmethod
    def get_user(cls, server_id):
        server = db.get_pb_server(server_id)

        if server is None:
            return cls(server_id, pb_id=server.id)

        return cls(server_id, server.name, server.members, server.items, server.tags, server.levels, server.multiplier,
                   int(server.id))

    def save(self):
        if db.get_pb_server(self.pb_id) is None:
            db.client.collection("servers").create({
                "name": self.name,
                "server_id": self.server_id,
                "items": self.items,
                "tags": self.tags,
                "levels": self.levels,
                "members": self.members,
                "multiplier": self.multiplier
            })
            return

        db.client.collection("servers").update(str(self.pb_id), {
                "name": self.name,
                "server_id": self.server_id,
                "items": self.items,
                "tags": self.tags,
                "levels": self.levels,
                "members": self.members,
                "multiplier": self.multiplier
            })


class Database:
    def __init__(self):
        self.client = PocketBase("http://pocketbase:8090")

    def get_pb_server(self, server_id: int):
        try:
            record = self.client.collection("servers").get_list(1, 1, {"filter": f"server_id = {server_id}"}).items[0]
        except IndexError:
            return None
        return record

    def get_pb_user(self, user_id: int):
        try:
            record = self.client.collection("users").get_list(1, 1, {
                "filter": f"user_id = {user_id}"}).items[0]
        except IndexError:
            return None
        return record


db = Database()
