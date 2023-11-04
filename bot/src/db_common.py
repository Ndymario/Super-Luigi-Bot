from typing import Union
from pydantic import BaseModel
from datetime import datetime
from pocketbase import PocketBase


class Item(BaseModel):
    id: Union[int, None] = None
    name: Union[str, None] = None
    cost: Union[int, None] = None


class Tag(BaseModel):
    id: Union[int, None] = None
    tag: Union[str, None] = None
    title: Union[str, None] = None
    description: Union[str, None] = None
    url: Union[str, None] = None


class FAQ(BaseModel):
    id: Union[int, None] = None
    question: Union[str, None] = None
    title: Union[str, None] = None
    description: Union[str, None] = None
    url: Union[str, None] = None


class User(BaseModel):
    id: Union[int, None] = None
    name: Union[str, None] = None
    exp: Union[int, None] = None
    total_exp: Union[int, None] = None
    level: Union[int, None] = None
    birthday: Union[datetime, None] = None
    inventory: Union[list, None] = None
    preferences: Union[dict, None] = None


class Server(BaseModel):
    id:Union[int, None] = None
    name: Union[str, None] = None
    members: Union[list, None] = None
    items: Union[list, None] = None
    faqs: Union[list, None] = None
    tags: Union[list, None] = None
    levels: Union[dict, None] = None


class Database:
    def __init__(self):
        self.client = PocketBase("http://pocketbase:8090")

    def _get_pb_server(self, server_id: int):
        try:
            record = self.client.collection("servers").get_list(1, 1, {"filter": f"server_id = {server_id}"}).items[0]
        except IndexError:
            return None
        return record

    def _get_pb_user(self, user_id: int):
        try:
            record = self.client.collection("users").get_list(1, 1, {"filter": f"user_id = {user_id}"}).items[0]
        except IndexError:
            return None
        return record

    def get_server(self, server_id: int) -> Server:
        record = self._get_pb_server(server_id)
        if record is None:
            return None

        server = Server()
        server.name = record.name
        server.id = record.server_id
        server.items = record.items
        server.faqs = record.faqs
        server.tags = record.tags
        server.levels = record.levels
        server.members = record.members

        return server

    def add_server(self, server: Server):
        self.client.collection("servers").create({
            "name": server.name,
            "server_id": server.id,
            "items": server.items,
            "faqs": server.faqs,
            "tags": server.tags,
            "levels": server.levels,
            "members": server.members
        })

    def add_member(self, user_id: int, server_id: int):
        user = self._get_pb_user(user_id)
        server = self._get_pb_server(server_id)
        if user is None:
            return
        if server is None:
            return

        members = server.members
        members.append(user.id)
        self.client.collection("servers").update(server.id, {"members": members})

    def get_user(self, user_id: int) -> User:
        record = self._get_pb_user(user_id)
        if record is None:
            return None

        user = User()
        user.id = record.user_id
        user.name = record.username
        user.exp = record.exp
        user.total_exp = record.total_exp
        user.level = record.level
        user.birthday = record.birthday
        user.inventory = record.inventory
        user.preferences = record.preferences

        return user

    def add_user(self, user: User, guild_id: int):
        self.client.collection("users").create({
            "username": user.name,
            "user_id": user.id,
            "exp": user.exp,
            "total_exp": user.total_exp,
            "level": user.level,
            "birthday": user.birthday,
            "preferences": user.preferences,
            "inventory": user.inventory
        })
        self.add_member(user.id, guild_id)

    def get_item(self, user_id: int) -> User:
        record = self._get_pb_user(user_id)
        if record is None:
            return None

        user = User()
        user.id = record.user_id
        user.name = record.username
        user.exp = record.exp
        user.total_exp = record.total_exp
        user.level = record.level
        user.birthday = record.birthday
        user.inventory = record.inventory
        user.preferences = record.preferences

        return user

    def add_item(self, user: User, guild_id: int):
        self.client.collection("users").create({
            "username": user.name,
            "user_id": user.id,
            "exp": user.exp,
            "total_exp": user.total_exp,
            "level": user.level,
            "birthday": user.birthday,
            "preferences": user.preferences,
            "inventory": user.inventory
        })
        self.add_member(user.id, guild_id)


db = Database()

if __name__ == "__main__":
    # TODO: Write script to restore user EXP
    pass
