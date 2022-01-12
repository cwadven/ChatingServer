import datetime
from channels.generic.websocket import AsyncWebsocketConsumer

import json
from datetime import datetime, timedelta

from django.db.models import DateTimeField, CharField
from django.db.models.functions import Cast, TruncSecond

from common_library import create_random_string
from websocket.models import GroupCount, GroupChatLog
from asgiref.sync import sync_to_async


LEAVE_MSG = 0
GREET_MSG = 1
NORMAL_MSG = 2

MESSAGE_TYPE = {
    LEAVE_MSG: LEAVE_MSG,
    GREET_MSG: GREET_MSG,
    NORMAL_MSG: NORMAL_MSG,
}

NORMAL_USER = 0
HOST_USER = 1


class ChatConsumer(AsyncWebsocketConsumer):
    # 접속 했을 경우 누가 있는지 확인하기 위한 자료구조
    @sync_to_async
    def add_current_user_to_group(self):
        # try:
        #     GroupCount.objects.get(
        #         nickname=self.scope['nickname'],
        #         groupname=self.groupname
        #     )
        # except:
        GroupCount.objects.create(
            nickname=self.scope['nickname'],
            groupname=self.groupname
        )

    @sync_to_async
    def remove_current_user_to_group(self):
        # try:
        #     GroupCount.objects.get(
        #         nickname=self.scope['nickname'],
        #         groupname=self.groupname,
        #         join_time__gte=datetime.now() - timedelta(seconds=0.5),
        #     )
        # except:
        GroupCount.objects.filter(
            nickname=self.scope['nickname'],
            groupname=self.groupname
        ).delete()

    @sync_to_async
    def get_current_group_user(self):
        qs = list(GroupCount.objects.filter(
            groupname=self.groupname
        ).annotate(
            joined_time=Cast(
                TruncSecond('join_time', DateTimeField()), CharField()
            )
        ).values(
            'nickname',
            'joined_time'
        ))

        return qs

    @sync_to_async
    def create_chat_log(self, username, message):
        GroupChatLog.objects.create(
            nickname=username,
            groupname=self.groupname,
            content=message
        )

    # websocket 연결 시 실행
    async def connect(self):
        # chat/routing.py 에 있는
        # path('ws/test/<str:username>/',consumers.ChatConsumer),
        self.groupname = self.scope['url_route']['kwargs']['room']

        # 접속시 시 바로 닉네임 설정하기
        self.scope['nickname'] = self.scope['user'].username if self.scope['user'].username else create_random_string(10)

        # Join room group
        await self.channel_layer.group_add(
            self.groupname,
            self.channel_name
        )
        await self.accept()

        await self.add_current_user_to_group()

        user_type = NORMAL_USER
        if self.scope['client'][0] == "192.168.0.19":
            user_type = HOST_USER

        current_user_set = await self.get_current_group_user()

        await self.channel_layer.group_send(
            self.groupname, {
                'type': 'greet',
                'username': self.scope['nickname'],
                'user_type': user_type,
                'current_user_set': current_user_set,
            }
        )

    # websocket 연결 종료 시 실행
    async def disconnect(self, close_code):
        await self.remove_current_user_to_group()

        current_user_set = await self.get_current_group_user()

        await self.channel_layer.group_send(
            self.groupname, {
                'type': 'bye',
                'username': self.scope['nickname'],
                'current_user_set': current_user_set,
            }
        )

        # Leave room group
        await self.channel_layer.group_discard(
            self.groupname,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        user_type = NORMAL_USER
        # Send message to room group
        # {}가 chat_message event 매소드이다
        # type 키를 이용해 값을 함수 명으로 결정해 해당 메시지를 보내는 형식
        username = self.scope['nickname']

        if username == "root":
            user_type = HOST_USER

        await self.create_chat_log(username, message)

        await self.channel_layer.group_send(
            self.groupname, {
                'type': 'get_messages',
                'message': message,
                'username': username,
                'sender_channel_name': self.channel_name,
                'user_type': user_type,
            }
        )

    async def get_messages(self, event):
        message = f"[{datetime.today().strftime('%Y-%m-%d %H:%M:%S')}] {event['username']}: {event['message']}"

        if event['user_type'] == HOST_USER:
            message = "[운영자] " + message

        # 나를 제외하고 다른 사람에게 보내기
        if self.channel_name != event['sender_channel_name']:
            await self.send(text_data=json.dumps({
                'type': MESSAGE_TYPE[NORMAL_MSG],
                'message': message,
                'username': event['username'],
                'user_type': event['user_type'],
            }))

    # 환영
    async def greet(self, event):
        message = f"""[{event['username']}] 님이 입장하셨습니다."""

        await self.send(text_data=json.dumps({
            'type': MESSAGE_TYPE[GREET_MSG],
            'message': message,
            'current_user_set': event['current_user_set'],
            'username': event['username'],
            'user_type': event['user_type'],
        }))

    # 나가기
    async def bye(self, event):
        message = f"""[{event['username']}] 님이 퇴장하셨습니다."""

        await self.send(text_data=json.dumps({
            'type': MESSAGE_TYPE[LEAVE_MSG],
            'message': message,
            'current_user_set': event['current_user_set'],
            'username': event['username'],
        }))
