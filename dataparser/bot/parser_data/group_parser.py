import json

from telethon.tl.functions.channels import JoinChannelRequest, GetFullChannelRequest
from telethon.tl.types import PeerChat, PeerUser, PeerChannel, Message as TelethonMessage, User as TelethonUser,\
    Channel as ChannelTelethon, Chat

from bot.database.methods.main import Database
from bot.clients import client
from bot.database.models.posts import Post
from bot.parser_data.utils import convert_dict_to_task_item
from bot.database.models.channel import Channel, ChannelData


class GroupParser:

    def __init__(self, uid: int, task_data: dict):
        self.task_data = task_data
        self.db = Database(uid=uid)
        self.cli = client

    async def _join(self, entity):
        return await self.cli(JoinChannelRequest(channel=entity))

    async def create_new_user(self, users: list):

        for user in users:
            ...

    async def get_type_entity(self, entity):

        if isinstance(entity, PeerChannel):
            return "PeerChannel"
        elif isinstance(entity, PeerChat):
            return "PeerChat"
        elif isinstance(entity, ChannelTelethon):
            return "Channel"
        elif isinstance(entity, Chat):
            return "Chat"
        elif isinstance(entity, TelethonMessage):
            return 'Message'
        elif isinstance(entity, TelethonUser):
            return 'User'
        elif isinstance(entity, PeerUser):
            return "PeerUser"
        else:
            return "Unexpected type"

    async def update_channel(self, entity):
        ...

    async def update_group(self, group_id: int, data):
        ...

    async def check_channel_in_db(self, channel_id: int):
        return any([item.id for item in await self.db.get_channel(channel_id=channel_id)])

    async def create_chanel_in_db(self, chanel: ChannelData):
        cn = Channel(chanel)

        new_chanel_data = await self.db.add_channel(channel_data=chanel, chanel=cn)

        return new_chanel_data

    async def get_limited_messages(self, entity):

        list_msg = []
        async for msg in self.cli.iter_messages(entity=entity, limit=1):
            message = json.loads(msg.to_json())
            try:
                print(message['message'])
            except Exception:
                continue

            # msg = Post(channel_id=)

            list_msg.append(message)

        return list_msg

    async def get_full_channel_info(self, entity):
        channel_info = await self.cli(GetFullChannelRequest(channel=entity))
        return channel_info

    async def compare_subscribers(self, entity):
        channel_info = await self.get_full_channel_info(entity=entity)
        full_info = channel_info.to_dict()
        last_total_users_in_chanel = [item.user_count for item in await self.db.get_channel(
            channel_id=full_info['full_chat']['id'])]

        return f"Новых подписчиков: {full_info['full_chat']['participants_count'] - last_total_users_in_chanel[0]}"

    async def get_users(self, entity):
        try:
            result = {"all_users": None}
            tmp = []
            async for user in client.iter_participants(entity=entity, aggressive=True):
                tmp.append(user.to_dict())
            result['all_users'] = tmp
            return result
        except Exception as e:
            print(f"Undefined exception: {e}")

    async def start_parsing(self):

        task = await convert_dict_to_task_item(task_item=self.task_data)

        try:
            entity = await self.cli.get_entity(task.target_url)

            entity_to_dict = entity.to_dict()

            entity_type = await self.get_type_entity(entity=entity)

            if entity_type == "Channel":

                if entity_to_dict['left'] is True:
                    update_data = await self._join(entity)

                if not await self.check_channel_in_db(channel_id=entity_to_dict['id']):

                    channel_info = await self.get_full_channel_info(entity=entity)
                    full_channel_info = channel_info.to_dict()

                    channel = ChannelData(id=entity_to_dict['id'],
                                          name=entity_to_dict['title'],
                                          link=task.target_url,
                                          description=full_channel_info['full_chat']['about'],
                                          user_count=full_channel_info['full_chat']['participants_count'])

                    updated_channel_data = await self.create_chanel_in_db(chanel=channel)
                    print(updated_channel_data)

                    # users = await self.get_users(entity=entity)
                    # print(users)
                    #
                    # messages = await self.get_limited_messages(entity=entity)
                    # print(messages)

                else:
                    c = await self.compare_subscribers(entity=entity)
                    print(c)
                    print("NEXT STEP CHANNEL WORK -> get info chanel")

        except Exception as e:
            print(e)
