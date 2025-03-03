from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework_simplejwt.tokens import AccessToken
from chat.models import Chat, Message
from accounts.models import User
import threading
import queue
import json


class ChatConsumer(AsyncWebsocketConsumer):
    """
    یک مصرف‌کننده WebSocket برای مدیریت پیام‌های چت در زمان واقعی.
    این مصرف‌کننده به کاربران این امکان را می‌دهد که بر اساس chat_id و توکن JWT به اتاق چت متصل شوند.

    ویژگی‌های مصرف‌کننده:
    - اتصال WebSocket را برای کاربران احراز هویت‌شده بر اساس توکن JWT برقرار می‌کند.
    - پیام‌های ورودی را دریافت و در صورت نیاز در پایگاه داده ذخیره کرده و به سایر اعضای گروه ارسال می‌کند.
    - پیام‌ها را به همه کاربران متصل به اتاق چت ارسال می‌کند.

    نکات کلیدی:
    - از chat_id و توکن JWT برای احراز هویت و مجوز دادن به کاربران استفاده می‌شود.
    - پیام‌ها به صورت زنده از طریق WebSocket ارسال و دریافت می‌شوند.
    - پیام‌ها در پایگاه داده در یک رشته جداگانه ذخیره می‌شوند.
    نمونه درسخواست:

    ws://127.0.0.1:8000/ws/chat/?token=توکن کاربرc&chat_id=شماره ای دی چت کاربر به اینت
    """

    async def connect(self):

        query_string = self.scope["query_string"].decode()  # get query string
        parts = query_string.split("&")
        token = parts[0].split("=")[-1]  #  extract token
        chat_id = parts[1].split("=")[-1]  # extract chat_id

        if not token:
            await self.close()  # close connection if token is not provided
        try:
            access_token = AccessToken(token)  # get access token
            user_id = access_token["user_id"]  # get user id from token
            result_queue = queue.Queue()  # create a queue to store the result
            thread = threading.Thread(
                target=self.get_chat_id_by_id_and_get_user_by_id,
                args=(user_id, chat_id, result_queue),
            )  # create a thread to get chat and user
            thread.start()
            thread.join()
            chat, user = result_queue.get()  # get chat and user from queue

            if chat is not None and user is not None:
                self.room_group_name = f"chat_room_{chat.id}"
                self.user = user
                await self.channel_layer.group_add(
                    self.room_group_name, self.channel_name
                )  # add user to chat
                await self.accept()
            else:
                await self.close()
        except Exception as e:
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )  # remove user from chat
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message", "")
        sender_id = text_data_json.get("user_id")

        if self.user.id != sender_id:
            await self.save_message_in_thread(message)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                },
            )  # send message to chat

    async def chat_message(self, event):  # send message to chat
        message = event["message"]

        await self.send(text_data=json.dumps({"message": message}))

    def save_message(self, message_content, sender):  # save message in database
        chat = Chat.objects.get(id=self.room_group_name.split("_")[-1])
        message = Message.objects.create(
            chat=chat, sender=sender, content=message_content
        )
        return message

    async def save_message_in_thread(self, message_content):  # save message in thread
        thread = threading.Thread(
            target=self.save_message, args=(message_content, self.user)
        )
        thread.start()
        thread.join()

    def get_chat_id_by_id_and_get_user_by_id(
        self, user_id, chat_id, result_queue
    ):  # get chat and user by id
        chat = Chat.objects.get(id=chat_id)
        user = User.objects.get(id=user_id)
        result_queue.put((chat, user))
