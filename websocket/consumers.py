import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
import json

LEAVE_MSG = 0
GREET_MSG = 1
NORMAL_MSG = 2

MESSAGE_TYPE = {
    LEAVE_MSG: LEAVE_MSG,
    GREET_MSG: GREET_MSG,
    NORMAL_MSG: NORMAL_MSG,
}


class ChatConsumer(AsyncWebsocketConsumer):
    current_user_set = {}

    # websocket 연결 시 실행
    async def connect(self):
        # chat/routing.py 에 있는
        # path('ws/test/<str:username>/',consumers.ChatConsumer),
        self.groupname = self.scope['url_route']['kwargs']['room']

        # Join room group
        await self.channel_layer.group_add(
            self.groupname,
            self.channel_name
        )
        await self.accept()

        username = self.scope['user'].username if self.scope['user'].username else str(self.scope['headers'][10][1])[
                                                                                   2:7] + "익명"

        room_name = self.groupname
        await self.channel_layer.group_send(
            self.groupname, {'type': 'greet', 'username': username, 'room_name': room_name}
        )

    # websocket 연결 종료 시 실행
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.groupname,
            self.channel_name
        )

        username = self.scope['user'].username if self.scope['user'].username else str(self.scope['headers'][10][1])[
                                                                                   2:7] + "익명"
        await self.channel_layer.group_send(
            self.groupname, {'type': 'bye', 'username': username}
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        # {}가 chat_message event 매소드이다
        # type 키를 이용해 값을 함수 명으로 결정해 해당 메시지를 보내는 형식
        username = self.scope['user'].username if self.scope['user'].username else str(self.scope['headers'][10][1])[
                                                                                   2:7] + "익명"
        await self.channel_layer.group_send(
            self.groupname, {'type': 'get_messages', 'message': message, 'username': username}
        )

    async def get_messages(self, event):
        message = f"[{datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')}] {event['username']}: {event['message']}"
        await self.send(text_data=json.dumps({
            'message': message, 'message_type': MESSAGE_TYPE[NORMAL_MSG],
        }))

    # 환영
    async def greet(self, event):
        # 접속 했을 경우 누가 있는지 확인하기 위한 자료구조
        if self.current_user_set.get(self.groupname):
            self.current_user_set[self.groupname][event['username']] = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        else:
            self.current_user_set[self.groupname] = {}
            self.current_user_set[self.groupname][event['username']] = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        current_user_set = json.dumps(self.current_user_set[self.groupname])

        message = f"""[{event['username']}] 님이 입장하셨습니다."""

        await self.send(text_data=json.dumps({
            'message': message, 'message_type': MESSAGE_TYPE[GREET_MSG], 'current_user_set': current_user_set,
        }))

    # 나가기
    async def bye(self, event):
        if self.current_user_set.get(self.groupname) and self.current_user_set.get(self.groupname).get(event['username']):
            del self.current_user_set[self.groupname][event['username']]
        current_user_set = json.dumps(self.current_user_set[self.groupname])

        message = f"""[{event['username']}] 님이 퇴장하셨습니다."""

        await self.send(text_data=json.dumps({
            'message': message, 'message_type': MESSAGE_TYPE[LEAVE_MSG], 'current_user_set': current_user_set,
        }))
