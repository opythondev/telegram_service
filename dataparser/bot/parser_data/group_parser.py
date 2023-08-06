import json

from telethon.tl.functions.channels import JoinChannelRequest, \
    GetFullChannelRequest
from telethon.tl.types import PeerChat, PeerUser, PeerChannel, \
    Message as TelethonMessage, User as TelethonUser, \
    Channel as ChannelTelethon, Chat

from bot.database.methods.main import Database
from bot.clients import client
from bot.database.models.posts import Post, PostData
from bot.database.models.user import UserData, User
from bot.database.models.user_channel import UserChannel, UserChannelData
from bot.parser_data.utils import convert_dict_to_task_item
from bot.database.models.channel import Channel, ChannelData


class GroupParser:

    def __init__(self, uid: int, task_data: dict):
        self.task_data = task_data
        self.db = Database(uid=uid)
        self.cli = client

    async def _join(self, entity):
        return await self.cli(JoinChannelRequest(channel=entity))

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

    async def check_channel_in_db(self, channel_id: int) -> bool:
        return any([item.id for item in
                    await self.db.get_channel(channel_id=channel_id)])

    async def concat_full_name(self, f_name: str, l_name: str) -> str:

        if f_name is not None:
            pass
        else:
            f_name = ''

        if l_name is not None:
            pass
        else:
            l_name = ''

        if f_name and l_name:
            return f_name + " " + l_name
        elif f_name:
            return f_name
        elif l_name:
            return l_name
        else:
            return "Noname"

    async def _cast_to_user_data(self, user: dict):

        u_data = UserData(
            id=int(user['id']),
            role=1,
            full_name=str(await self.concat_full_name(
                f_name=user['first_name'],
                l_name=user['last_name'])),
            user_name=str(user['username'])
        )

        return u_data

    async def create_users_in_db(self, users: dict, channel_id: int):
        user_list = []
        user_for_user_channel = []

        # CHECK USER IN DB
        users_in_db = {
            f"{item.id}": UserData(
                id=item.id,
                role=item.role,
                full_name=item.full_name,
                user_name=item.user_name,
                phone=item.phone,
                email=item.email,
                is_subscribed=item.is_subscribed
            ) for item in await self.db.get_all_users()
        }

        # CHECK USER IN USER_CHANNEL
        all_users_in_group = {
            f"{item.user_id}": UserData(
                id=item.id,
                channel_id=item.channel_id,
                user_id=item.user_id
            ) for item in
            await self.db.get_all_users_in_channel(cid=channel_id)
        }

        for user in users['all_users']:
            if user['id'] in users_in_db:
                if user['id'] in all_users_in_group:
                    continue
                else:
                    user_for_user_channel.append(
                        await self._cast_to_user_data(user=user))
            else:
                user_list.append(
                    User(await self._cast_to_user_data(user=user)))
                user_for_user_channel.append(
                    await self._cast_to_user_data(user=user))

        if user_list:
            await self.db.add_users(users=user_list)

        if user_for_user_channel:
            await self.create_userchannel_in_db(users=user_for_user_channel,
                                                channel_id=channel_id)

        return user_for_user_channel

    async def create_userchannel_in_db(self, users: list[UserData],
                                       channel_id: int):

        user_channel_list = []

        for user in users:
            user_channel = UserChannelData(
                user_id=user.id,
                channel_id=channel_id
            )

            user_channel_list.append(UserChannel(user_channel))

        await self.db.add_user_channel(items=user_channel_list)

    async def compare_posts(self, new_posts: list[PostData],
                            old_posts: list[tuple]) -> dict:
        ids = [item[0] for item in old_posts]
        ids.sort()

        old_posts = {item[1]: {"id": item[0],
                               "message_id": item[1]} for item in old_posts}
        result = {}

        for new_post in new_posts:
            if new_post.message_id in old_posts:
                continue
            else:
                result[ids.pop(0)] = new_post

        return result

    async def update_last_10_messages(self, last_msg: list[PostData],
                                      channel_id: int):
        posts = [(item.id, item.message_id) for item in
                 await self.db.get_posts_by_channel_id(channel_id=channel_id)]

        if posts:
            need_update_posts = await self.compare_posts(new_posts=last_msg,
                                                         old_posts=posts)

            await self.db.update_posts(items=[{
                "id": item.id,
                "channel_id": item.channel_id,
                "message_id": item.message_id,
                "date": item.date,
                "photo": item.photo,
                "title": item.title,
                "text": item.text,
                "reactions_count": item.reactions_count,
                "views_count": item.views_count,
                "comments_channel_id": item.comments_channel_id
            }
                for item in need_update_posts])
        else:
            await self.db.add_posts(items=[Post(item) for item in last_msg])

    async def create_chanel_in_db(self, chanel: ChannelData):
        cn = Channel(chanel)

        new_chanel_data = await self.db.add_channel(channel_data=chanel,
                                                    chanel=cn)

        return new_chanel_data

    async def create_post_entity(self, message_data: dict, channel_id: int):
        all_reactions_count = 0

        for reaction_item in message_data['reactions']['results']:
            all_reactions_count += reaction_item['count']

        post_data_item = PostData(channel_id=channel_id,
                                  message_id=message_data['id'],
                                  date=message_data['date'],
                                  text=message_data['message'],
                                  title="None title",
                                  views_count=message_data['views'],
                                  reactions_count=all_reactions_count,
                                  comments_channel_id=message_data['replies'][
                                      'channel_id'])
        return post_data_item

    async def get_limited_messages(self, entity, channel_id: int, limit=10):

        list_post_data = []

        async for msg in self.cli.iter_messages(entity=entity, limit=limit):
            message = json.loads(msg.to_json())

            try:
                list_post_data.append(
                    await self.create_post_entity(message_data=message,
                                                  channel_id=channel_id))
            except Exception:
                continue

        await self.update_last_10_messages(last_msg=list_post_data,
                                           channel_id=channel_id)

        return list_post_data

    async def get_full_channel_info(self, entity):
        channel_info = await self.cli(GetFullChannelRequest(channel=entity))
        return channel_info

    async def check_double(self, users: list):
        ...

    async def add_unique_users(self, entity, channel_id: int):

        users = await self.get_users(entity=entity)

        if users is not None:
            user_data_list = await self.create_users_in_db(
                users=users,
                channel_id=channel_id)

            return user_data_list
        else:

            return None

    async def compare_subscribers(self, entity):
        channel_info = await self.get_full_channel_info(entity=entity)

        full_info = channel_info.to_dict()
        last_total_users_in_chanel = [item.user_count for item in
                                      await self.db.get_channel(
                                          channel_id=full_info['full_chat'][
                                              'id'])]
        count = full_info['full_chat']['participants_count']
        return f"Новых подписчиков: {count - last_total_users_in_chanel[0]}"

    async def compare_messages(self, messages):
        ...

    async def get_users(self, entity) -> None | dict:
        try:
            result = {"all_users": None}
            tmp = []
            async for user in client.iter_participants(entity=entity,
                                                       aggressive=True):
                tmp.append(user.to_dict())

            result['all_users'] = tmp
            return result
        except Exception as e:
            print(f"Undefined exception: {e}")
            return None

    async def start_parsing(self):

        task = await convert_dict_to_task_item(task_item=self.task_data)

        try:
            entity = await self.cli.get_entity(task.target_url)

            entity_to_dict = entity.to_dict()
            entity_type = await self.get_type_entity(entity=entity)

            task.channel_id = entity_to_dict['id']

            if entity_type == "Channel":

                if entity_to_dict['left'] is True:
                    await self._join(entity)

                if not await self.check_channel_in_db(
                        channel_id=entity_to_dict['id']):

                    channel_info = await self.get_full_channel_info(
                        entity=entity)
                    full_channel_info = channel_info.to_dict()

                    about = full_channel_info['full_chat']['about']
                    co = full_channel_info['full_chat']['participants_count']

                    channel = ChannelData(id=entity_to_dict['id'],
                                          name=entity_to_dict['title'],
                                          link=task.target_url,
                                          description=about,
                                          user_count=co
                                          )

                    await self.create_chanel_in_db(chanel=channel)

                    await self.add_unique_users(
                        entity=entity,
                        channel_id=entity_to_dict['id'])

                else:

                    messages = await self.get_limited_messages(
                        entity=entity,
                        channel_id=entity_to_dict['id'])

                    print(messages)

            task_item_update = {
                "channel_id": task.channel_id,
                "status": "success"
            }

            await self.db.update_task_item(task_item_id=task.id,
                                           update_data=task_item_update)

        except Exception as e:
            print(e)

            task_item_update = {
                "status": "error"
            }

            await self.db.update_task_item(task_item_id=task.id,
                                           update_data=task_item_update)
