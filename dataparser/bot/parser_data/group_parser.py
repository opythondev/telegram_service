import logging

from telethon.tl.functions.channels import JoinChannelRequest, \
    GetFullChannelRequest
from telethon.tl.types import PeerChat, PeerUser, PeerChannel, \
    Message as TelethonMessage, User as TelethonUser, \
    Channel as ChannelTelethon, Chat

from bot.configs.settings import MAX_UPDATE_MESSAGES
from bot.database.methods.main import Database
from bot.clients import client
from bot.database.models.posts import Post, PostData
from bot.database.models.user import UserData, User
from bot.database.models.user_channel import UserChannel, UserChannelData
from bot.parser_data.utils import convert_dict_to_task_item, convert_dict_to_channel_data
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
            item.id: UserData(
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
            item.user_id: UserData(
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
                            old_posts: list[tuple]) -> list:
        result = []

        index_for_update = [index[0] for index in old_posts]

        msg_id_old = [item[1] for item in old_posts]
        msg_id_new = [item.message_id for item in new_posts]

        diff = list(set(msg_id_old) ^ set(msg_id_new))

        if diff:

            for item in new_posts:

                if item.message_id in diff:
                    get_index = index_for_update.index(max(index_for_update))
                    index = index_for_update.pop(get_index)

                    result.append({
                        index: item
                    })

        return result

    async def update_last_messages(self, last_posts: list[PostData]):
        new_posts = []

        channel_id = last_posts[0].channel_id

        posts = [(item.id, item.message_id, item.state) for item in
                 await self.db.get_posts_by_channel_id(channel_id=channel_id)]

        if posts:

            new_posts = await self.compare_posts(new_posts=last_posts,
                                                 old_posts=posts)

            if len(posts) + len(new_posts) <= MAX_UPDATE_MESSAGES:
                new_items = []

                for i in new_posts:
                    for k, v in i.items():
                        new_items.append(v)

                await self.db.add_posts(items=[Post(item) for item in new_items])

            else:
                await self.db.update_posts(items=new_posts)

        else:
            await self.db.add_posts(items=[Post(item) for item in last_posts])

        all_id = [post[0] for post in posts]

        if new_posts:
            for new_post in new_posts:
                for id_ in new_post.keys():
                    if id_ in all_id:
                        idx = all_id.index(id_)
                        all_id.pop(idx)

            await self.update_status_post(all_id=all_id, posts=posts)
        else:
            await self.update_status_post(all_id=all_id, posts=posts)

    async def update_status_post(self, all_id, posts):

        for post in posts:
            if post[0] in all_id and post[2] != "old":
                await self.db.update_post(post_id=post[0], data={"state": "old"})

    async def create_chanel_in_db(self, chanel: ChannelData):
        cn = Channel(chanel)

        new_chanel_data = await self.db.add_channel(channel_data=chanel,
                                                    chanel=cn)

        return new_chanel_data

    async def create_post_entity(self, message_data: dict):

        all_reactions_count = 0
        try:
            for reaction_item in message_data['reactions']['results']:
                all_reactions_count += reaction_item['count']
        except Exception as e:
            logging.info(f"Error: {e}")

        try:
            replies = message_data['replies']['channel_id']
            if replies is None:
                replies = 0
        except Exception as e:
            logging.info(f"error: {e}")
            replies = 0

        message_id = message_data['id']
        date = str(message_data['date'])

        try:
            text = message_data['message']
        except Exception as e:
            logging.info(f"error: {e}")
            text = ''
        try:
            views_count = message_data['views']
        except Exception as e:
            logging.info(f"error: {e}")
            views_count = 0

        if text:
            post_data_item = PostData(channel_id=message_data['peer_id']['channel_id'],
                                      message_id=message_id,
                                      date=date,
                                      text=text,
                                      state="new",
                                      views_count=views_count,
                                      reactions_count=all_reactions_count,
                                      comments_channel_id=replies)
        else:
            post_data_item = PostData(channel_id=message_data['peer_id']['channel_id'],
                                      message_id=message_id,
                                      date=date,
                                      text=text,
                                      state="new",
                                      views_count=views_count,
                                      reactions_count=all_reactions_count,
                                      comments_channel_id=replies,
                                      type="Media/Docs")

        return post_data_item

    async def get_limited_messages(self, entity, limit=10):

        list_post_data = []

        async for msg in self.cli.iter_messages(entity=entity, limit=limit):

            try:
                list_post_data.append(
                    await self.create_post_entity(message_data=msg.to_dict())
                )
            except Exception as e:
                logging.info(f"error in get_limited_message: {e}")
                continue

        await self.update_last_messages(last_posts=list_post_data)

        return list_post_data

    async def get_full_channel_info(self, entity):
        channel_info = await self.cli(GetFullChannelRequest(channel=entity))
        return channel_info

    async def add_unique_users(self, entity, channel_id: int):

        all_users_in_channel = await self.get_users(entity=entity)

        if all_users_in_channel is not None:

            user_data_list = await self.create_users_in_db(
                users=all_users_in_channel,
                channel_id=channel_id)

            return user_data_list
        else:

            return None

    async def compare_subscribers(self, entity):
        channel_info = await self.get_full_channel_info(entity=entity)

        full_info = channel_info.to_dict()

        last_total_users_in_chanel = [item.user_count for item in await self.db.get_channel(
            channel_id=full_info['full_chat']['id'])]

        user_count = full_info['full_chat']['participants_count']

        return f"Новых подписчиков: {user_count - last_total_users_in_chanel[0]}"

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

                if not await self.check_channel_in_db(channel_id=entity_to_dict['id']):

                    channel_info = await self.get_full_channel_info(
                        entity=entity)

                    full_channel_info = channel_info.to_dict()

                    channel = await convert_dict_to_channel_data(link=task.target_url,
                                                                 entity_data=entity_to_dict,
                                                                 channel_info=full_channel_info)

                    await self.create_chanel_in_db(chanel=channel)

                    await self.add_unique_users(
                        entity=entity,
                        channel_id=entity_to_dict['id'])

                    await self.get_limited_messages(
                        entity=entity)

                else:

                    await self.get_limited_messages(
                        entity=entity)

            # CHANGE STATUS
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
