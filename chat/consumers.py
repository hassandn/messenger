from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.contrib.auth.models import AnonymousUser
from chat.models import Chat, Message
from accounts.models import User


# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.group_name = "mt5_data_group"
#         await self.channel_layer.group_add(self.group_name, self.channel_name)
#         print(f"this is group name{self.group_name}")
#         print(f"this is channel name{self.channel_name}")
#         await self.accept()
#         print("WebSocket connected!")
#     async def disconnect(self, close_code):
#             await self.channel_layer.group_discard(self.group_name, self.channel_name)
#             try:
#                 print(f"Disconnected with code {close_code}")
#             except Exception as e:
#                 print(f"Error during disconnect: {e}") 





# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_group_name = "chat_room"
#         await self.channel_layer.group_add(self.room_group_name, self.channel_name)
#         await self.accept()  # اتصال WebSocket را تأیید کن

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

#     async def receive(self, text_data):
#         try:
#             data = json.loads(text_data)  # بررسی اینکه آیا پیام JSON معتبر است
#             message = data.get("message", "")

#             if not message:
#                 return  # پیام خالی ارسال نشود

#             await self.channel_layer.group_send(
#                 self.room_group_name,
#                 {
#                     "type": "chat_message",
#                     "message": message,
#                 },
#             )
#         except Exception as e:
#             print(f"Error in receive: {e}")  # نمایش خطا در لاگ

#     async def chat_message(self, event):
#         await self.send(text_data=json.dumps({"message": event["message"]}))


# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # گرفتن توکن از کوئری پارامتر
#         query_string = self.scope["query_string"].decode()  # تبدیل بایت به رشته
#         token = None

#         if "token=" in query_string:
#             token = query_string.split("token=")[-1].split("&")[0]  # جدا کردن مقدار توکن

#         print(f"Received Token: {token}")  # پرینت توکن در لاگ سرور

#         await self.accept()  # قبول کردن اتصال WebSocket

#     async def disconnect(self, close_code):
#         print("WebSocket Disconnected.")

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data.get("message", "")

#         await self.send(text_data=json.dumps({"message": f"Received: {message}"}))

# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from accounts.models import User
# from rest_framework_simplejwt.tokens import AccessToken
# import urllib.parse

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         query_string = self.scope["query_string"].decode()
#         token = None
    
#         if "token=" in query_string:
#             token = query_string.split("token=")[-1].split("&")[0]  

#         if token:
#             try:
#                 print(token)
#                 access_token = AccessToken(token)  
#                 user_id = access_token["user_id"]  

#                 self.user = User.objects.get(id=user_id)  # گرفتن یوزر از مدل کاستوم
#                 print(f"User Connected: {self.user.username} (ID: {self.user.id})")

#                 await self.accept()
#             except Exception as e:
#                 print(f"JWT Authentication Failed: {e}")
#                 await self.close()
#         else:
#             print("No token provided.")
#             await self.close()

#     async def disconnect(self, close_code):
#         print(f"User Disconnected: {self.user.username if hasattr(self, 'user') else 'Unknown'}")

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data.get("message", "")

#         if hasattr(self, "user"):
#             await self.send(text_data=json.dumps({
#                 "message": f"{self.user.username}: {message}"
#             }))


# from channels.generic.websocket import AsyncWebsocketConsumer
# from rest_framework_simplejwt.tokens import AccessToken
# from accounts.models import User
# import json

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # دریافت توکن از URL
#         token = self.scope['query_string'].decode().split('=')[-1]  # فرض بر این است که توکن به صورت ?token=<your_token> ارسال می‌شود
#         print(token)
#         if not token:
#             await self.close()  # اگر توکن وجود نداشته باشد، اتصال را می‌بندیم
        
#         try:
#             # بررسی اعتبار توکن
#             access_token = AccessToken(token)  # بررسی و استخراج توکن
#             user_id = access_token["user_id"]  # گرفتن user_id از توکن
#             print(user_id)
#             # پیدا کردن یوزر از پایگاه داده
#             User = User.get_user_model()  # مدل یوزر سفارشی
#             user = User.objects.get(id=user_id)
#             print(f"thi is user = {user}")

#             # ذخیره اطلاعات یوزر برای استفاده در کانکشن
#             self.user = user
#             await self.accept()  # اتصال را تایید می‌کنیم
#         except Exception as e:
#             await self.close()  # اگر توکن یا یوزر معتبر نباشد، اتصال را می‌بندیم
    
#     async def disconnect(self, close_code):
#         # منطق زمانی که اتصال بسته می‌شود
#         pass

#     async def receive(self, text_data):
#         # دریافت پیام و ارسال به تمام کاربران یا مدیریت پیام‌ها
#         pass


# from channels.generic.websocket import AsyncWebsocketConsumer
# from rest_framework_simplejwt.tokens import AccessToken
# from django.contrib.auth import get_user_model
# from asgiref.sync import sync_to_async
# import json

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # دریافت توکن از URL
#         token = self.scope['query_string'].decode().split('=')[-1]  # فرض بر این است که توکن به صورت ?token=<your_token> ارسال می‌شود
#         print(token)
        
#         if not token:
#             await self.close()  # اگر توکن وجود نداشته باشد، اتصال را می‌بندیم
        
#         try:
#             # بررسی اعتبار توکن
#             access_token = AccessToken(token)  # بررسی و استخراج توکن
#             user_id = access_token["user_id"]  # گرفتن user_id از توکن
#             print(user_id)
            
#             # پیدا کردن یوزر از پایگاه داده
#             user = await self.get_user_by_id(user_id)  # فراخوانی تابع async برای دریافت یوزر
#             print(f"this is user = {user}")

#             # ذخیره اطلاعات یوزر برای استفاده در کانکشن
#             self.user = user
#             await self.accept()  # اتصال را تایید می‌کنیم
#         except Exception as e:
#             print(f"Error: {e}")  # برای دیباگ بهتر خطاها را چاپ می‌کنیم
#             await self.close()  # اگر توکن یا یوزر معتبر نباشد، اتصال را می‌بندیم
    
#     async def disconnect(self, close_code):
#         # منطق زمانی که اتصال بسته می‌شود
#         pass

#     async def receive(self, text_data):
#         # دریافت پیام و ارسال به تمام کاربران یا مدیریت پیام‌ها
#         pass

#     @sync_to_async
#     def get_user_by_id(self, user_id):
#         # پیدا کردن یوزر از پایگاه داده
#         User = get_user_model()  # مدل یوزر سفارشی
#         return User.objects.get(id=user_id)



from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
import json
from channels.db import database_sync_to_async
from .models import Chat
import threading
import queue


# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # دریافت توکن از URL
#         query_string = self.scope['query_string'].decode()  # گرفتن کوئری از URL

#         parts = query_string.split('&')
#         token = parts[0].split('=')[-1]  # استخراج توکن
#         chat_id = parts[1].split('=')[-1]  # استخراج chat_id

#         print(token)
#         print(f"this is chat id {chat_id}")
        
#         if not token:
#             await self.close()  # اگر توکن وجود نداشته باشد، اتصال را می‌بندیم
        
#         try:
#             # بررسی اعتبار توکن
#             access_token = AccessToken(token)  # بررسی و استخراج توکن
#             user_id = access_token["user_id"]  # گرفتن user_id از توکن
#             print(user_id)
            
#             result_queue = queue.Queue()
            
#             thread = threading.Thread(target=self.get_chat_id_by_id_and_get_user_by_id, args=(user_id, chat_id, result_queue))
#             thread.start()
#             thread.join()

#             chat, user = result_queue.get()
            
#             self.room_group_name = f"chat_room_{chat}"  # نام گروه ثابت
#             await self.channel_layer.group_add(
#                 self.room_group_name,
#                 self.channel_name
#             )
#             print(f"User {user.id} connected to room: {self.room_group_name}")
#             await self.accept()  # اتصال را تایید می‌کنیم
#         except Exception as e:
#             print(f"Error: {e}")  # برای دیباگ بهتر خطاها را چاپ می‌کنیم
#             await self.close()  # اگر توکن یا یوزر معتبر نباشد، اتصال را می‌بندیم
    
#     async def disconnect(self, close_code):
#         # فقط اگر room_group_name مقداردهی شده باشد، اقدام به خارج کردن کاربر از گروه کنیم
#         if hasattr(self, 'room_group_name'):
#             await self.channel_layer.group_discard(
#                 self.room_group_name,
#                 self.channel_name
#             )
#         # منطق زمانی که اتصال بسته می‌شود
#         pass

#     async def receive(self, text_data):
#         # دریافت پیام و ارسال به تمام کاربران گروه
#         text_data_json = json.loads(text_data)
#         message = text_data_json.get('message', '')

#         # ارسال پیام به گروه
#         await self.channel_layer.group_send(
#             self.room_group_name,  # ارسال به گروهی که کاربر در آن است
#             {
#                 'type': 'chat_message',
#                 'message': message,
#             }
#         )

#     async def chat_message(self, event):
#         # دریافت پیام از گروه و ارسال آن به کاربر
#         message = event['message']

#         # ارسال پیام به WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))
    
    
#     def get_chat_id_by_id_and_get_user_by_id(self, user_id, chat_id, result_queue):
#         chat = Chat.objects.get(id=chat_id)
#         user = User.objects.get(id=user_id)
#         print(chat)
#         print(user)
#         # return chat, user
#         result_queue.put((chat, user))
   


# from channels.generic.websocket import AsyncWebsocketConsumer
# from rest_framework_simplejwt.tokens import AccessToken
# from django.contrib.auth import get_user_model
# import json
# from channels.db import database_sync_to_async
# from channels.db import database_sync_to_async

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # دریافت کوئری از URL
#         query_string = self.scope['query_string'].decode()  # گرفتن کوئری از URL

#         parts = query_string.split('&')
#         token = parts[0].split('=')[-1]  # استخراج توکن
#         chat_id = parts[1].split('=')[-1]  # استخراج chat_id


#         print(token)
#         print(chat_id)
#         if not token or not chat_id:
#             await self.close()  # اگر توکن یا chat_id وجود نداشته باشد، اتصال را می‌بندیم

#         try:
#             # بررسی اعتبار توکن
#             access_token = AccessToken(token)  # بررسی و استخراج توکن
#             user_id = access_token["user_id"]  # گرفتن user_id از توکن

#             # پیدا کردن چت بر اساس chat_id
#             chat = await self.get_chat_by_id(chat_id)

#             # چک کردن که آیا کاربر جزو طرفین چت است یا نه
#             if chat.user1.id == user_id or chat.user2.id == user_id:
#                 self.user = await self.get_user_by_id(user_id)  # گرفتن کاربر از پایگاه داده
#                 self.room_group_name = f"chat_{chat_id}"  # نام روم به chat_id متصل می‌شود
#                 await self.accept()  # اتصال را تایید می‌کنیم
#             else:
#                 await self.close()  # اگر کاربر جزو طرفین چت نباشد، اتصال را می‌بندیم

#         except Exception as e:
#             print(f"Error: {e}")  # برای دیباگ بهتر خطاها را چاپ می‌کنیم
#             await self.close()  # اگر توکن یا چت یا یوزر معتبر نباشد، اتصال را می‌بندیم

#     async def disconnect(self, close_code):
#         # منطق زمانی که اتصال بسته می‌شود
#         pass

#     async def receive(self, text_data):
#         # دریافت پیام و ارسال به همه کاربران در روم مربوطه
#         pass

#     @database_sync_to_async
#     def get_user_by_id(self, user_id):
#         # پیدا کردن یوزر از پایگاه داده
#         return User.objects.get(id=user_id)

#     @database_sync_to_async
#     def get_chat_by_id(self, chat_id):
#         # پیدا کردن چت از پایگاه داده
#         return Chat.objects.get(id=chat_id)


from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from .models import Chat  # اطمینان حاصل کنید که مدل Chat به درستی وارد شده باشد

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # دریافت کوئری از URL
#         query_string = self.scope['query_string'].decode()  # گرفتن کوئری از URL

#         parts = query_string.split('&')
#         token = parts[0].split('=')[-1]  # استخراج توکن
#         chat_id = parts[1].split('=')[-1]  # استخراج chat_id


#         if not token or not chat_id:
#             await self.close()  # اگر توکن یا chat_id وجود نداشته باشد، اتصال را می‌بندیم

#         try:
#             # بررسی اعتبار توکن
#             access_token = AccessToken(token)  # بررسی و استخراج توکن
#             user_id = access_token["user_id"]  # گرفتن user_id از توکن

#             # پیدا کردن چت بر اساس chat_id
#             chat = await self.get_chat_by_id(chat_id)

#             # چک کردن که آیا کاربر جزو طرفین چت است یا نه
#             if chat.user1.id == user_id or chat.user2.id == user_id:
#                 self.user = await self.get_user_by_id(user_id)  # گرفتن کاربر از پایگاه داده
#                 self.room_group_name = f"chat_{chat_id}"  # نام روم به chat_id متصل می‌شود
#                 await self.accept()  # اتصال را تایید می‌کنیم
#             else:
#                 await self.close()  # اگر کاربر جزو طرفین چت نباشد، اتصال را می‌بندیم

#         except Exception as e:
#             print(f"Error: {e}")  # برای دیباگ بهتر خطاها را چاپ می‌کنیم
#             await self.close()  # اگر توکن یا چت یا یوزر معتبر نباشد، اتصال را می‌بندیم

#     async def disconnect(self, close_code):
#         # منطق زمانی که اتصال بسته می‌شود
#         pass

#     async def receive(self, text_data):
#         # دریافت پیام و ارسال به همه کاربران در روم مربوطه
#         pass

#     @database_sync_to_async
#     def get_user_by_id(self, user_id):
#         # پیدا کردن یوزر از پایگاه داده
#         User = get_user_model()  # اطمینان حاصل کنید که به مدل صحیح ارجاع داده می‌شود
#         return User.objects.get(id=user_id)

#     @database_sync_to_async
#     def get_chat_by_id(self, chat_id):
#         # پیدا کردن چت از پایگاه داده
#         return Chat.objects.get(id=chat_id)


import threading
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
import json

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         query_string = self.scope['query_string'].decode()  # گرفتن کوئری از URL

#         parts = query_string.split('&')
#         token = parts[0].split('=')[-1]  # استخراج توکن
#         chat_id = parts[1].split('=')[-1]  # استخراج chat_id

#         if not token or not chat_id:
#             await self.close()  # اگر توکن یا chat_id وجود نداشته باشد، اتصال را می‌بندیم

#         try:
#             # بررسی اعتبار توکن
#             access_token = AccessToken(token)
#             user_id = access_token["user_id"]  # گرفتن user_id از توکن

#             # استفاده از ترد برای فراخوانی تابع در ترد جداگانه
#             thread = threading.Thread(target=self.get_user_and_chat_by_ids, args=(user_id, chat_id))
#             thread.start()

#             # این قسمت به طور همزمان اجرا نمی‌شود، پس از اتمام ترد فراخوانی می‌شود
#             thread.join()  # تا زمانی که ترد تمام نشده است، اینجا متوقف می‌شود

#             # چک کردن که آیا کاربر جزو طرفین چت است یا نه
#             if self.chat.user1.id == user_id or self.chat.user2.id == user_id:
#                 self.room_group_name = f"chat_{chat_id}"
#                 await self.accept()  # اتصال را تایید می‌کنیم
#             else:
#                 await self.close()  # اگر کاربر جزو طرفین چت نباشد، اتصال را می‌بندیم

#         except Exception as e:
#             print(f"Error: {e}")  # برای دیباگ بهتر خطاها را چاپ می‌کنیم
#             await self.close()  # اگر توکن یا چت یا یوزر معتبر نباشد، اتصال را می‌بندیم

#     def get_user_and_chat_by_ids(self, user_id, chat_id):
#         # این تابع در ترد جداگانه اجرا می‌شود
#         User = get_user_model()  # اطمینان حاصل کنید که به مدل صحیح ارجاع داده می‌شود
#         user = User.objects.get(id=user_id)
#         chat = Chat.objects.get(id=chat_id)

#         # پس از دریافت کاربر و چت، آنها را به متغیرهای این کلاس ارجاع می‌دهیم
#         self.user = user
#         self.chat = chat


# import threading
# import queue
# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from rest_framework_simplejwt.tokens import AccessToken
# from django.contrib.auth import get_user_model
# from channels.db import database_sync_to_async
# from .models import Chat, User

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # دریافت توکن از URL
#         query_string = self.scope['query_string'].decode()  # گرفتن کوئری از URL

#         parts = query_string.split('&')
#         token = parts[0].split('=')[-1]  # استخراج توکن
#         chat_id = parts[1].split('=')[-1]  # استخراج chat_id

#         print(token)
#         print(f"this is chat id {chat_id}")
        
#         if not token:
#             await self.close()  # اگر توکن وجود نداشته باشد، اتصال را می‌بندیم
        
#         try:
#             # بررسی اعتبار توکن
#             access_token = AccessToken(token)  # بررسی و استخراج توکن
#             user_id = access_token["user_id"]  # گرفتن user_id از توکن
#             print(user_id)
            
#             result_queue = queue.Queue()
            
#             # فراخوانی تابع بررسی چت و کاربر
#             thread = threading.Thread(target=self.check_chat_exists_for_user, args=(user_id, chat_id, result_queue))
#             thread.start()
#             thread.join()

#             chat, user = result_queue.get()

#             # نام گروه بر اساس چت
#             self.room_group_name = f"chat_room_{chat.id}"  # استفاده از شناسه چت برای نام گروه
#             await self.channel_layer.group_add(
#                 self.room_group_name,
#                 self.channel_name
#             )
#             print(f"User {user.id} connected to room: {self.room_group_name}")
#             await self.accept()  # اتصال را تایید می‌کنیم
#         except Exception as e:
#             print(f"Error: {e}")  # برای دیباگ بهتر خطاها را چاپ می‌کنیم
#             await self.close()  # اگر توکن یا یوزر معتبر نباشد، اتصال را می‌بندیم
    
#     async def disconnect(self, close_code):
#         # فقط اگر room_group_name مقداردهی شده باشد، اقدام به خارج کردن کاربر از گروه کنیم
#         if hasattr(self, 'room_group_name'):
#             await self.channel_layer.group_discard(
#                 self.room_group_name,
#                 self.channel_name
#             )
#         # منطق زمانی که اتصال بسته می‌شود
#         pass

#     async def receive(self, text_data):
#         # دریافت پیام و ارسال به تمام کاربران گروه
#         text_data_json = json.loads(text_data)
#         message = text_data_json.get('message', '')

#         # ارسال پیام به گروه
#         await self.channel_layer.group_send(
#             self.room_group_name,  # ارسال به گروهی که کاربر در آن است
#             {
#                 'type': 'chat_message',
#                 'message': message,
#             }
#         )

#     async def chat_message(self, event):
#         # دریافت پیام از گروه و ارسال آن به کاربر
#         message = event['message']

#         # ارسال پیام به WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))
    
#     def get_chat_id_by_id_and_get_user_by_id(self, user_id, chat_id, result_queue):
#         chat = Chat.objects.get(id=chat_id)
#         user = User.objects.get(id=user_id)
#         print(chat)
#         print(user)
#         result_queue.put((chat, user))

#     def check_chat_exists_for_user(self, user_id, chat_id, result_queue):
#         try:
#             chat = Chat.objects.get(id=chat_id)
#             # بررسی اینکه آیا چت برای این کاربر وجود دارد
#             if chat.user1.id == user_id or chat.user2.id == user_id:
#                 user = User.objects.get(id=user_id)
#                 print(f"user {user} exist in chat  = {chat}")
#                 result_queue.put((chat, user))
#             else:
#                 result_queue.put((None, None))  # اگر چت برای کاربر نباشد، مقدار None قرار می‌دهیم
#         except Chat.DoesNotExist:
#             result_queue.put((None, None))  # اگر چت پیدا نشد، مقدار None قرار می‌دهیم



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # دریافت توکن از URL
        query_string = self.scope['query_string'].decode()  # گرفتن کوئری از URL

        parts = query_string.split('&')
        token = parts[0].split('=')[-1]  # استخراج توکن
        chat_id = parts[1].split('=')[-1]  # استخراج chat_id

        print(token)
        print(f"this is chat id {chat_id}")
        
        if not token:
            await self.close()  # اگر توکن وجود نداشته باشد، اتصال را می‌بندیم
        
        try:
            # بررسی اعتبار توکن
            access_token = AccessToken(token)  # بررسی و استخراج توکن
            user_id = access_token["user_id"]  # گرفتن user_id از توکن
            print(user_id)
            
            result_queue = queue.Queue()
            
            thread = threading.Thread(target=self.get_chat_id_by_id_and_get_user_by_id, args=(user_id, chat_id, result_queue))
            thread.start()
            thread.join()

            chat, user = result_queue.get()
            
            if chat is not None and user is not None:
                self.room_group_name = f"chat_room_{chat.id}"  # استفاده از شناسه چت برای نام گروه
                self.user = user  # ذخیره کاربر در شیء برای استفاده در آینده
                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )
                print(f"User {user.id} connected to room: {self.room_group_name}")
                await self.accept()  # اتصال را تایید می‌کنیم
            else:
                print(f"No chat found for user {user_id} and chat {chat_id}")
                await self.close()  # اگر چت یا کاربر پیدا نشد، اتصال را می‌بندیم
        except Exception as e:
            print(f"Error: {e}")  # برای دیباگ بهتر خطاها را چاپ می‌کنیم
            await self.close()  # اگر توکن یا یوزر معتبر نباشد، اتصال را می‌بندیم
    
    async def disconnect(self, close_code):
        # فقط اگر room_group_name مقداردهی شده باشد، اقدام به خارج کردن کاربر از گروه کنیم
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        # منطق زمانی که اتصال بسته می‌شود
        pass

    async def receive(self, text_data):
        # دریافت پیام و ارسال به تمام کاربران گروه
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '')
        sender_id = text_data_json.get('user_id')  # گرفتن شناسه کاربری که پیام را ارسال کرده

        # بررسی این که آیا این پیام قبلاً ارسال شده یا خیر
        if self.user.id != sender_id:
            # ذخیره پیام در دیتابیس با استفاده از ترد
            await self.save_message_in_thread(message)

            # ارسال پیام به گروه فقط اگر فرستنده خود کاربر نباشد
            await self.channel_layer.group_send(
                self.room_group_name,  # ارسال به گروهی که کاربر در آن است
                {
                    'type': 'chat_message',
                    'message': message,
                }
            )

    async def chat_message(self, event):
        # دریافت پیام از گروه و ارسال آن به کاربر
        message = event['message']

        # ارسال پیام به WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    def save_message(self, message_content, sender):
        chat = Chat.objects.get(id=self.room_group_name.split('_')[-1])  # استخراج chat_id از نام گروه
        message = Message.objects.create(
            chat=chat,
            sender=sender,
            content=message_content
        )
        return message

    async def save_message_in_thread(self, message_content):
        # اجرای ذخیره پیام در ترد جداگانه
        thread = threading.Thread(target=self.save_message, args=(message_content, self.user))
        thread.start()
        thread.join()

    def get_chat_id_by_id_and_get_user_by_id(self, user_id, chat_id, result_queue):
        chat = Chat.objects.get(id=chat_id)
        user = User.objects.get(id=user_id)
        result_queue.put((chat, user))
