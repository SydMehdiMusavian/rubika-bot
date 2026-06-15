import aiohttp , asyncio
from Rubika.Config_Logger import bot_logger

class Fn:
    def __init__(self,tk:str=None):
         self.url = f"https://botapi.rubika.ir/v3/{tk}/"
         self.mime_to_extensions_no_dot = {
            # تصاویر (Images)
            "image/jpeg": ["jpg", "jpeg", "jpe", "jfif"],
            "image/png": ["png"],
            "image/gif": ["gif"],
            "image/webp": ["webp"],
            "image/bmp": ["bmp", "dib"],
            "image/svg+xml": ["svg", "svgz"],
            "image/tiff": ["tiff", "tif"],
            "image/x-icon": ["ico"],
            "image/heic": ["heic"],
            "image/heif": ["heif"],

            # ویدئوها (Videos)
            "video/mp4": ["mp4", "m4v"],
            "video/x-matroska": ["mkv"],
            "video/webm": ["webm"],
            "video/avi": ["avi"],
            "video/mpeg": ["mpeg", "mpg"],
            "video/quicktime": ["mov", "qt"],
            "video/x-msvideo": ["avi"],
            "video/x-flv": ["flv"],
            "video/3gpp": ["3gp", "3gpp"],
            "video/x-ms-wmv": ["wmv"],

            # صداها (Audios)
            "audio/mpeg": ["mp3"],
            "audio/wav": ["wav"],
            "audio/ogg": ["ogg", "oga"],
            "audio/flac": ["flac"],
            "audio/aac": ["aac"],
            "audio/mp4": ["m4a", "mp4a"],
            "audio/webm": ["weba"],
            "audio/x-ms-wma": ["wma"],

            # اسناد متنی (Documents & Text)
            "application/pdf": ["pdf"],
            "application/msword": ["doc"],
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ["docx"],
            "application/vnd.ms-excel": ["xls"],
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ["xlsx"],
            "application/vnd.ms-powerpoint": ["ppt"],
            "application/vnd.openxmlformats-officedocument.presentationml.presentation": ["pptx"],
            "text/plain": ["txt"],
            "text/html": ["html", "htm"],
            "text/css": ["css"],
            "text/csv": ["csv"],
            "text/markdown": ["md"],
            "application/rtf": ["rtf"],
            "application/vnd.oasis.opendocument.text": ["odt"],
            "application/vnd.oasis.opendocument.spreadsheet": ["ods"],
            "application/vnd.oasis.opendocument.presentation": ["odp"],

            # آرشیوها (Archives)
            "application/zip": ["zip"],
            "application/x-rar-compressed": ["rar"],
            "application/x-7z-compressed": ["7z"],
            "application/x-tar": ["tar"],
            "application/gzip": ["gz"],
            "application/vnd.rar": ["rar"],

            # برنامه‌ها و فایل‌های اجرایی (Executables & Code)
            "application/json": ["json"],
            "application/xml": ["xml"],
            "application/javascript": ["js"],
            "application/python": ["py"],
            "application/x-httpd-php": ["php"],
            "application/x-sh": ["sh"],
            "application/x-executable": ["exe", "msi"],
            "application/java-archive": ["jar"],

            # فایل‌های سه بعدی و مدل (3D & Models)
            "model/gltf+json": ["gltf"],
            "model/gltf-binary": ["glb"],
            "application/octet-stream": ["bin", "dat"]
        }
    
    async def send_message_simple(self,ChatId:str,txt:str,
                            disableNotification:bool=False,MessageId_For_Replay:str=None,metadata_part:list=None):
        """

        ### ارسال متن ساده به چت

        - #### آرگومان ها :
          - `ChatId` (**str**) : شناسه چت موردنظر 
          - `txt` (**str**) : متن پیام
          - `disableNotification` (**bool,optional**) : غیرفعال کردن اعلان برای کاربران (پیشفرض: **False**)
          - `MessageId_For_Replay` (**str, optional**) : شناسه پیامی که می‌خواهید به آن ریپلای کنید
          - `metadata_part` (**list, optional**) : متادیتا برای فرمت‌بندی، منشن و لینک
            

        - #### پاسخ :
        ```python
        {'status': 'OK', 'data': {'message_id': 'رشته'}}
        ```

        - #### مثال :
        ```python
        mtd = [{
                "type": "Bold", # یکی از انواع متا دیتا ها
                "from_index" : 1,
                "length": 3,
                "link_url" : None, #فقط در صورتی که type برابر با Link باشد استفاده می‌شود.
                "mention_text_user_id": None #فقط در صورتی که type برابر با MentionText باشد استفاده می‌شود.
            }]
        await app.send_message_simple(ChatId=msg.chat_id ,txt="Hello World" , metadata_part=mtd)
        ```
        > ***نکته⚠️*** <br>
        > `msg` :<br>
        > همان شی حاوی اطلاعات اپدیتی است که با تابع هندلر شما مطابقت دارد<br>
        > شما میتوانید با استفاده از آن به اطلاعات اپدیت دریافت شده از سرور<br>
        > دسترسی داشته باشید.<br>

        > ***⚠️نکته*** <br>
        > `metadata_part` :<br>
        > پارامتری است دلخواه , برای قالب بندی متن ارسالی <br>
        > شما میتوانید لیستی از دیکشنری های حاوی پارامترهایی که در لینک زیر هستند رو بهش پاس بدید :<hr>
        > [Meta_data-Rubika](https://rubika.ir/botapi/models#metadataPart)

        """
        
        url = f"{self.url}/sendMessage"
        data = {
            "chat_id" : ChatId,
            "text":txt,
            "disable_notification":disableNotification
        }

        if MessageId_For_Replay :
            data.update({"reply_to_message_id": MessageId_For_Replay})

        if metadata_part :
            MetaData = {
                "meta_data_parts":[]
            }
            MetaData.update({"meta_data_parts":metadata_part})
            data.update({"metadata":MetaData})
            
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                return await response.json()
    
    async def send_keypad(self,ChatId:str,txt:str,chatKeypad:dict,
                    disableNotification:bool=False,MessageId_For_Replay:str=None,metadata_part:list=None):
        
        """

        ### ارسال پیام با کیپد شناور

        > ##### دوست من یادت باشه این متد فقط توی چت های خصوصی عمل میکنه ☠️

        - #### آرگومان ها :
          - `ChatId` (**str**): شناسه چت
          - `txt` (**str**): متن پیام
          - `chatKeypad` (**dict**): ساختار کیپد شناور
          - `disableNotification` (**bool , optional**): غیرفعال کردن اعلان (پیشفرض: False)
          - `MessageId_For_Replay` (**str , optional**): شناسه پیام برای ریپلای
          - `metadata_part` (**list , optional**): متادیتا برای قالب‌بندی متن
        - #### پاسخ

        ```python
        {'status': 'OK', 'data': {'message_id': 'رشته'}}
        ```

        - #### مثال استفاده :
        ```python
        keypad = {
                "rows" : [
                    {
                        "buttons":[
                            {"id":"100",
                            "type":"Simple",
                            "button_text":"hi"},
                            {"id":"101",
                            "type":"Simple",
                            "button_text":"by"}
                        ]
                    }
                ],
                "resize_keyboard":False, #تغییر اندازه و ارتفاع دکمه‌ها
                "one_time_keyboard":False #بسته شدن خودکار کیبورد بعد از اولین انتخاب
            }
        mtd = [{
                    "type": "Bold", # یکی از انواع متا دیتا ها
                    "from_index" : 1,
                    "length": 3,
                    "link_url" : None, #فقط در صورتی که type برابر با Link باشد استفاده می‌شود.
                    "mention_text_user_id": None #فقط در صورتی که type برابر با MentionText باشد استفاده می‌شود.
            }]
        await app.send_keypad(ChatId=msg.chat_id , txt="Hello world" , chatKeypad=keypad , metadata_part=mtd)
        ```
        > ***نکته⚠️*** <br>
        > `msg` :<br>
        > همان شی حاوی اطلاعات اپدیتی است که با تابع هندلر شما مطابقت دارد<br>
        > شما میتوانید با استفاده از آن به اطلاعات اپدیت دریافت شده از سرور<br>
        > دسترسی داشته باشید.<br>

        > ***⚠️نکته*** <br>
        > `metadata_part` :<br>
        > پارامتری است دلخواه , برای قالب بندی متن ارسالی <br>
        > شما میتوانید لیستی از دیکشنری های حاوی پارامترهایی که در لینک زیر هستند رو بهش پاس بدید :<hr>
        > [Meta_data-Rubika](https://rubika.ir/botapi/models#metadataPart)

        - #### برای داشتن اطلاعات بیشتر در مورد اینکه چه جور دکمه هایی رو میتونیم استفاده کنیم
        >منظورم این قسمت از تعریفه:
        ```python
        {"id":"100",
        "type":"Simple",
        "button_text":"any word"}
        ```
        - #### میتونید به این لینک مراجعه کنید([Rubika](https://rubika.ir/botapi/models#button))

        """

        url = f"{self.url}/sendMessage"

        data = {
            "chat_id" : ChatId,
            "text":txt,
            "chat_keypad_type":"New",
            "chat_keypad":chatKeypad,
            "disable_notification":disableNotification
        }
        if MessageId_For_Replay :
            data.update({"reply_to_message_id": MessageId_For_Replay})

        if metadata_part :
            MetaData = {
                "meta_data_parts":[]
            }
            MetaData.update({"meta_data_parts":metadata_part})
            data.update({"metadata":MetaData})

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                return await response.json()
    
    async def send_inline_keypad(self,ChatId:str,txt:str,inlineKeypad:dict,
                    disableNotification=False,MessageId_For_Replay:str=None,metadata_part:list=None):
        
        """
        ### ارسال پیام با دکمه شیشه ای
        >> ***این متد هم توی چت های خصوصی و هم توی چت های عمومی مثل کانال یا گروه کاربرد دارد🤙🏻***

        - #### آرگومان ها :
          - `ChatId` (**str**): شناسه چت
          - `txt` (**str**): متن پیام
          - `inlineKeypad` (**dict**): ساختار دکمه‌های زیر پیام
          - `disableNotification` (**bool, optional**): غیرفعال کردن اعلان (پیشفرض: False)
          - `MessageId_For_Replay` (**str, optional**): شناسه پیام برای ریپلای
          - `metadata_part` (**list, optional**): متادیتا برای قالب‌بندی متن

        - #### پاسخ :
        ```python
        {'status': 'OK', 'data': {'message_id': 'رشته'}}
        ```

        - #### مثال :
        ```python

        keypad = {
            "rows" : [
                {
                    "buttons":[
                        {"id":"100",
                        "type":"Simple",
                        "button_text":"hi"},
                        {"id":"101",
                        "type":"Simple",
                        "button_text":"by"}
                    ]
                }
            ],
            "resize_keyboard":False, #تغییر اندازه و ارتفاع دکمه‌ها
            "one_time_keyboard":False #بسته شدن خودکار کیبورد بعد از اولین انتخاب
        }
        mtd = [{
                "type": "Bold", # یکی از انواع متا دیتا ها
                "from_index" : 1,
                "length": 3,
                "link_url" : None, #فقط در صورتی که type برابر با Link باشد استفاده می‌شود.
                "mention_text_user_id": None #فقط در صورتی که type برابر با MentionText باشد استفاده می‌شود.
            }]
        await app.send_inline_keypad(ChatId=msg.chat_id , txt="Hello World" , inlineKeypad=keypad , metadata_part=mtd)

        ```
        > ***نکته⚠️*** <br>
        > `msg` :<br>
        > همان شی حاوی اطلاعات اپدیتی است که با تابع هندلر شما مطابقت دارد<br>
        > شما میتوانید با استفاده از آن به اطلاعات اپدیت دریافت شده از سرور<br>
        > دسترسی داشته باشید.<br>

        > ***⚠️نکته*** <br>
        > `metadata_part` :<br>
        > پارامتری است دلخواه , برای قالب بندی متن ارسالی <br>
        > شما میتوانید لیستی از دیکشنری های حاوی پارامترهایی که در لینک زیر هستند رو بهش پاس بدید :<hr>
        > [Meta_data-Rubika](https://rubika.ir/botapi/models#metadataPart)

        - #### برای داشتن اطلاعات بیشتر در مورد اینکه چه جور دکمه هایی رو میتونیم استفاده کنیم
        >منظورم این قسمت از تعریفه:
        ```python
        {"id":"100",
        "type":"Simple",
        "button_text":"any word"}
        ```
        - #### میتونید به این لینک مرتجعه کنید([Rubika](https://rubika.ir/botapi/models#button))

        """

        url = f"{self.url}/sendMessage"

        data = {
            "chat_id" : ChatId,
            "text":txt,
            "inline_keypad":inlineKeypad,
            "disable_notification":disableNotification
        }
        if MessageId_For_Replay :
            data.update({"reply_to_message_id": MessageId_For_Replay})
        if metadata_part :
            MetaData = {
                "meta_data_parts":[]
            }
            MetaData.update({"meta_data_parts":metadata_part})
            data.update({"metadata":MetaData})
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                return await response.json()
    
    async def send_poll(self,ChatId:str,Question:str,Options:list):

        """
        ### متد ارسال نظر سنجی

        > ##### ***این متد در چت های خصوصی استفاده نمیشه⚠️***

        - #### آرگومان ها :
          - `ChatId` (**str**) : شناسه چت مورد نظر
          - `Question` (**str**) : سوال نظرسنجی
          - `Options` (**list**) : لیست گزینه های نظر سنجی
        
        - #### پاسخ :
        ```python
        {'status': 'OK', 'data': {'message_id': 'رشته'}}
        ```

        - #### مثال :
        ```python

        options = ["yes" , "no"]
        await app.send_poll(ChatId=msg.chat_id , Question="آیا این کتابخونه مفید خواهد بود؟" , Options=options)

        ```
        > ***نکته⚠️*** <br>
        > `msg` :<br>
        > همان شی حاوی اطلاعات اپدیتی است که با تابع هندلر شما مطابقت دارد<br>
        > شما میتوانید با استفاده از آن به اطلاعات اپدیت دریافت شده از سرور<br>
        > دسترسی داشته باشید.<br>

        """

        url = f"{self.url}/sendPoll"

        data = {
            "chat_id": ChatId,
            "question":Question,
            "options":Options
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                return await response.json()
    
    async def send_location(self,ChatId:str,Latitude:str,Longitude:str,
                            MessageId_For_Replay:str=None,disableNotification:bool=False,
                            chatKeypad:dict=None,chatKeypadType:str="New",inlineKeypad:dict=None):

        """
        ### متد ارسال موقعیت مکانی (مختصات جغرافیایی)

        - #### آرگومان ها :
          - `ChatId` (**str**): شناسه چت
          - `Latitude` (**str**): عرض جغرافیایی
          - `Longitude` (**str**): طول جغرافیایی
          - `MessageId_For_Replay` (**str, optional**): شناسه پیام برای ریپلای
          - `disableNotification` (**bool, optional**): غیرفعال کردن اعلان (پیشفرض: False)
          - `chatKeypad` (**dict, Optional**) : اضافه کردن کیپد شناور هنگام ارسال لوکیشن
          - `inlineKeypad` (**dict, Optional**) : اضافه کردن دکمه شیشه ای به پایین لوکیشن
          - `chatKeypadType` (**str, Optional**) : همراه با پارامتر  chatKeypad میاد و نوعش رو مشخص میکنه (None,New,Remove)
        
        - #### پاسخ :
        ```python
        {'status': 'OK', 'data': {'message_id': 'رشته'}}
        ```

        - #### مثال :
        ```python

            keypad = {
                "rows" : [
                    {
                        "buttons":[
                            {"id":"100",
                            "type":"Simple",
                            "button_text":"yes"},
                            {"id":"101",
                            "type":"Simple",
                            "button_text":"no"}
                        ]
                    }
                ],
                "resize_keyboard":False, #تغییر اندازه و ارتفاع دکمه‌ها
                "one_time_keyboard":False #بسته شدن خودکار کیبورد بعد از اولین انتخاب
            }

            await app.send_location(ChatId=msg.chat_id , Latitude=35.6892, Longitude=51.3890 , chatKeypad=keypad ,inlineKeypad=keypad)

        ```
        > ***نکته⚠️*** <br>
        > `msg` :<br>
        > همان شی حاوی اطلاعات اپدیتی است که با تابع هندلر شما مطابقت دارد<br>
        > شما میتوانید با استفاده از آن به اطلاعات اپدیت دریافت شده از سرور<br>
        > دسترسی داشته باشید.<br>

        - #### برای داشتن اطلاعات بیشتر در مورد اینکه چه جور دکمه هایی رو میتونیم استفاده کنیم
        >منظورم این قسمت از تعریفه:
        ```python
        {"id":"100",
        "type":"Simple",
        "button_text":"any word"}
        ```
        - #### میتونید به این لینک مرتجعه کنید([Rubika](https://rubika.ir/botapi/models#button))

        """

        url = f"{self.url}/sendLocation"

        data = {
            "chat_id": ChatId,
            "latitude":Latitude,
            "longitude":Longitude,
            "disable_notification":disableNotification
        }
        if chatKeypad and inlineKeypad:
            data = {
                "chat_id": ChatId,
                "latitude":Latitude,
                "longitude":Longitude,
                "disable_notification":disableNotification,
                "chat_keypad_type" : chatKeypadType,
                "chat_keypad" :chatKeypad,
                "inline_keypad" : inlineKeypad
            }
        elif chatKeypad :
            data = {
                "chat_id": ChatId,
                "latitude":Latitude,
                "longitude":Longitude,
                "disable_notification":disableNotification,
                "chat_keypad_type" : chatKeypadType,
                "chat_keypad" :chatKeypad
            }
        elif inlineKeypad :
            data = {
                "chat_id": ChatId,
                "latitude":Latitude,
                "longitude":Longitude,
                "disable_notification":disableNotification,
                "inline_keypad" : inlineKeypad
            }
        if MessageId_For_Replay :
            data.update({"reply_to_message_id": MessageId_For_Replay})
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                return await response.json()

    async def send_contact(self,ChatId:str,firstName:str,lastName:str,phoneNumber:str,
                    disableNotification=False,MessageId_For_Replay:str=None,
                    chatKeypad:dict=None,chatKeypadType:str="New",inlineKeypad:dict=None):
        
        """
        ### متد ارسال مخاطب

        > ##### ***این متد فقط در چت های خصوصی عمل میکنه⚠️***

        - #### آرگومان ها :
          - `ChatId` (**str**): شناسه چت
          - `firstName` (**str**): نام مخاطب
          - `lastName` (**str**): نام خانوادگی مخاطب
          - `phoneNumber` (**str**): شماره تلفن مخاطب
          - `MessageId_For_Replay` (**str, optional**): شناسه پیام برای ریپلای
          - `disableNotification` (**bool, Optional**): غیرفعال کردن اعلان (پیشفرض: False)
          - `chatKeypad` (**dict, Optional**) : اضافه کردن کیپد شناور هنگام ارسال مخاطب
          - `inlineKeypad` (**dict, Optional**) : اضافه کردن دکمه شیشه ای به پایین مخاطب
          - `chatKeypadType` (**str, Optional**) : همراه با پارامتر  chatKeypad میاد و نوعش رو مشخص میکنه (None,New,Remove)
        
        - #### پاسخ :
        ```python
        {'status': 'OK', 'data': {'message_id': 'رشته'}}
        ```

        - #### مثال :
        ```python

            keypad = {
                "rows" : [
                    {
                        "buttons":[
                            {"id":"100",
                            "type":"Simple",
                            "button_text":"Ok"},
                            {"id":"101",
                            "type":"Simple",
                            "button_text":"No"}
                        ]
                    }
                ],
                "resize_keyboard":False, #تغییر اندازه و ارتفاع دکمه‌ها
                "one_time_keyboard":False #بسته شدن خودکار کیبورد بعد از اولین انتخاب
            }

            await app.send_contact(ChatId=msg.chat_id, firstName="موسویان", lastName="مهدی", phoneNumber="09308...279" ,
            inlineKeypad=keypad,chatKeypad=keypad)

        ```
        > ***نکته⚠️*** <br>
        > `msg` :<br>
        > همان شی حاوی اطلاعات اپدیتی است که با تابع هندلر شما مطابقت دارد<br>
        > شما میتوانید با استفاده از آن به اطلاعات اپدیت دریافت شده از سرور<br>
        > دسترسی داشته باشید.<br>

        - #### برای داشتن اطلاعات بیشتر در مورد اینکه چه جور دکمه هایی رو میتونیم استفاده کنیم
        >منظورم این قسمت از تعریفه:
        ```python
        {"id":"100",
        "type":"Simple",
        "button_text":"any word"}
        ```
        - #### میتونید به این لینک مرتجعه کنید([Rubika](https://rubika.ir/botapi/models#button))

        """

        url = f"{self.url}/sendContact"

        data = {
            "chat_id": ChatId,
            "first_name":firstName,
            "last_name":lastName,
            "phone_number":phoneNumber,
            "disable_notification":disableNotification
        }
        if chatKeypad and inlineKeypad:
            data = {
                "chat_id": ChatId,
                "first_name":firstName,
                "last_name":lastName,
                "phone_number":phoneNumber,
                "disable_notification":disableNotification,
                "chat_keypad_type" : chatKeypadType,
                "chat_keypad" :chatKeypad,
                "inline_keypad" : inlineKeypad
            }
        elif chatKeypad :
            data = {
                "chat_id": ChatId,
                "first_name":firstName,
                "last_name":lastName,
                "phone_number":phoneNumber,
                "disable_notification":disableNotification,
                "chat_keypad_type" : chatKeypadType,
                "chat_keypad" :chatKeypad
            }
        elif inlineKeypad :
            data = {
                "chat_id": ChatId,
                "first_name":firstName,
                "last_name":lastName,
                "phone_number":phoneNumber,
                "disable_notification":disableNotification,
                "inline_keypad" : inlineKeypad
            }
        if MessageId_For_Replay :
            data.update({"reply_to_message_id": MessageId_For_Replay})
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                return await response.json()

    async def get_chat(self,ChatId:str):
        """
        ### دریافت اطلاعات کامل یک چت (گروه، کانال یا خصوصی)

        - #### آرگومان ها :

          - `ChatId` (**str**): شناسه چت
        
        - #### پاسخ :
        ```python
        {'status': 'OK',
        'data': {
            'chat': {'chat_id': '', #شناسه چت
                    'chat_type': '', #نوع چت (User,Group,Channel,Bot)
                    'user_id': '', #شناسه کاربر مقابل بات در چت‌های خصوصی است. (فقط در چت‌های خصوصی)
                    'first_name': '', #نام کاربر. (فقط در چت‌های خصوصی)
                    'last_name' : '', #نام خانوادگی کاربر
                    'username': '', #نام کاربری چت یا کاربر (در صورت تنظیم شدن)
                    'title': '' #عنوان گروه یا کانال (در چت‌های گروهی و کانال‌ها)
                    }
            }
        }
        ```

        - #### مثال :

            chat_info = await app.get_chat(msg.chat_id)

        > ***نکته⚠️*** <br>
        > `msg` :<br>
        > همان شی حاوی اطلاعات اپدیتی است که با تابع هندلر شما مطابقت دارد<br>
        > شما میتوانید با استفاده از آن به اطلاعات اپدیت دریافت شده از سرور<br>
        > دسترسی داشته باشید.<br>

        """
        url = f"{self.url}/getChat"

        data = {
            "chat_id": ChatId
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                return await response.json()
    
    async def forward_message(self,ChatId:str,MessageId:str,toChatId:str,disableNotification:bool=False):
        """
        ### متد فوروارد کردن پیام

        - #### آرگومان ها :
          - `ChatId` (**str**): شناسه چت مبدأ
          - `MessageId` (**str**): شناسه پیام مورد نظر برای فوروارد
          - `toChatId` (**str**): شناسه چت مقصد
          - `disableNotification` (**bool, Optional**): غیرفعال کردن اعلان (پیشفرض: False)
        
        - #### پاسخ :
        ```python
        {'status': 'OK', 'data': {'new_message_id': 'رشته'}}
        ```

        - #### مثال :
        ```python

        await app.forward_message(ChatId=msg.chat_id ,
        toChatId="چت آیدی مقصد" ,
        MessageId=msg.message.message_id

        ```
        > ***نکته⚠️*** <br>
        >> `msg` :<br>
        >> همان شی حاوی اطلاعات اپدیتی است که با تابع هندلر شما مطابقت دارد<br>
        >> شما میتوانید با استفاده از آن به اطلاعات اپدیت دریافت شده از سرور<br>
        >> دسترسی داشته باشید.<br>

        """
        url = f"{self.url}/forwardMessage"

        data = {
            "from_chat_id": ChatId,
            "message_id": MessageId,
            "to_chat_id":toChatId,
            "disable_notification":disableNotification
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                return await response.json()
    
    async def edit_message_text(self,ChatId:str,MessageId,txt,metadata_part:list=None):

        """
        ### ویرایش متن یک پیام قبلی ارسال شده توسط بات

        - #### آرگومان :
          - `ChatId` (**str**): شناسه چت
          - `MessageId` (**str**): شناسه پیام مورد نظر برای ویرایش
          - `txt` (**str**): متن جدید
          - `metadata_part` (**list, optional**): متادیتا یک لیست از دیکشنری ها برای قالب بندی متن و شامل ویژگی های زیر
            - `type` : نوع متادیتا(**Bold ,Italic ,Mono ,Underline ,Strike ,Spoiler ,Link ,MentionText ,Pre ,Quote**)
            - `from_index` : اندیس شروع در متن (بر اساس UTF-16) که مقدار آن میتواند بزرگتر یا برابر 0 باشد
            - `length` : طول بخش مورد نظر (بر اساس UTF-16) که باید حتما بزرگتر از 0 باشد
            - `link_url` : فقط در صورتی که type برابر با Link باشد استفاده می‌شود
            - `mention_text_user_id` : فقط در صورتی که type برابر با MentionText باشد استفاده می‌شود

        > ##### توجه⚠️ :
        >> مجموع from_index + length نباید از طول متن (بر اساس UTF-16) بیشتر شود. در غیر این صورت مقادیر نامعتبر بوده و درخواست با خطا مواجه می‌شود و پیام ارسال نخواهد شد

        > ##### توجه⚠️ :
        >> برخی کاراکترها (مانند emoji) دارای طول 2 هستند

        > ##### توجه⚠️ :
        >> در نوع MentionText پیام باید در چت گروهی ارسال شود در غیر این صورت درخواست با خطا مواجه خواهد شد

        > ##### توجه⚠️ :
        >> اعمال فرمت‌های Bold، Italic، Underline و Strike روی emoji تأثیر قابل مشاهده‌ای ندارد

        - #### پاسخ :
            ```python
            {'status': 'OK', 'data': {}}
            ```

        - #### مثال :
        ```python
            catch_messageId = []

            @app.message(Text("start") & ChatType("Channel"))
            async def test(msg:Main_Update,fsm:StateInjection):
                res = await app.send_message_simple(ChatId=msg.chat_id,txt="hello world")
                catch_messageId.append(res["data"]["message_id"])


            @app.message(Text("continue") & ChatType("Channel"))
            async def test(msg:Main_Update,fsm:StateInjection):
                if len(catch_messageId) > 0:
                    await app.edit_message_text(ChatId=msg.chat_id ,
                    MessageId=catch_messageId[len(catch_messageId)-1] ,
                    txt="message Edit")
        ```
        > ***نکته⚠️*** <br>
        >> `msg` :<br>
        >> همان شی حاوی اطلاعات اپدیتی است که با تابع هندلر شما مطابقت دارد<br>
        >> شما میتوانید با استفاده از آن به اطلاعات اپدیت دریافت شده از سرور<br>
        >> دسترسی داشته باشید.<br>

        """
        
        url = f"{self.url}/editMessageText"

        data = {
            "chat_id": ChatId,
            "message_id":MessageId,
            "text":txt
        }

        if metadata_part :
            MetaData = {
                "meta_data_parts":[]
            }
            MetaData.update({"meta_data_parts":metadata_part})
            data.update({"metadata":MetaData})

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                return await response.json()
    
    async def edit_message_inlineKeypad(self,ChatId:str,MessageId,inlineKeypad):

        """
        ### ویرایش دکمه شیشه ای

        - #### آرگومان :
          - `ChatId` (**str**): شناسه چت
          - `MessageId` (**str**): شناسه پیام مورد نظر برای ویرایش
          - `inlineKeypad` (**dict**): دکمه شیشه ای جدید
            - ##### در مورد پارامتر های مربوط به هر دکمه میتونید این صفحه رو بررسی کنید([Rubika](https://rubika.ir/botapi/models#button))

        - #### پاسخ :
            ```python
            {'status': 'OK', 'data': {}}
            ```

        - #### مثال :
            ```python
            catch_messageId = []

            @app.message(Text("start") & ChatType("User"))
            async def test(msg:Main_Update,fsm:StateInjection):
                keypad = {
                    "rows" : [
                        {
                            "buttons":[
                                {"id":"100",
                                "type":"Simple",
                                "button_text":"btn1"},
                                {"id":"101",
                                "type":"Simple",
                                "button_text":"btn2"}
                            ]
                        }
                    ],
                    "resize_keyboard":False, #تغییر اندازه و ارتفاع دکمه‌ها
                    "one_time_keyboard":False #بسته شدن خودکار کیبورد بعد از اولین انتخاب
                }
                res = await app.send_inline_keypad(ChatId=msg.chat_id,txt="u can choose",inlineKeypad=keypad)
                catch_messageId.append(res["data"]["message_id"])


            @app.message(Text("end") & ChatType("User"))
            async def test(msg:Main_Update,fsm:StateInjection):
                keypad = {
                    "rows" : [
                        {
                            "buttons":[
                                {"id":"100",
                                "type":"Simple",
                                "button_text":"edit 1"},
                                {"id":"101",
                                "type":"Simple",
                                "button_text":"edit 2"}
                            ]
                        }
                    ],
                    "resize_keyboard":False, #تغییر اندازه و ارتفاع دکمه‌ها
                    "one_time_keyboard":False #بسته شدن خودکار کیبورد بعد از اولین انتخاب
                }
                if len(catch_messageId) > 0:
                    await app.edit_message_inlineKeypad(ChatId=msg.chat_id,MessageId=catch_messageId[len(catch_messageId)-1],inlineKeypad=keypad)
            ```

        > ***نکته⚠️*** <br>
        >> `msg` :<br>
        >> همان شی حاوی اطلاعات اپدیتی است که با تابع هندلر شما مطابقت دارد<br>
        >> شما میتوانید با استفاده از آن به اطلاعات اپدیت دریافت شده از سرور<br>
        >> دسترسی داشته باشید.<br>

        """

        url = f"{self.url}/editMessageKeypad"

        data = {
            "chat_id": ChatId,
            "message_id":MessageId,
            "inline_keypad":inlineKeypad
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                return await response.json()
    
    async def delete_message(self,ChatId:str,MessageId):

        """
        ### حذف یک پیام از چت

        - #### آرگومان :
          - `ChatId` (**str**): شناسه چت
          - `MessageId` (**str**): شناسه پیام مورد نظر برای حذف
        > ##### توجه : برای حذف پیام دیگران باید مجوز لازم را داشته باشد(مثلا در گروه ها)⚠️

        - #### پاسخ :
            ```python
            {'status': 'OK', 'data': {}}
            ```
        
        - #### مثال :
            ```python
                catch_messageId = []

                @app.message(Text("Start") & ChatType("User"))
                async def test(msg:Main_Update,fsm:StateInjection):
                    keypad = {
                        "rows" : [
                            {
                                "buttons":[
                                    {"id":"100",
                                    "type":"Simple",
                                    "button_text":"btn 1"},
                                    {"id":"101",
                                    "type":"Simple",
                                    "button_text":"btn 2"}
                                ]
                            }
                        ],
                        "resize_keyboard":False, #تغییر اندازه و ارتفاع دکمه‌ها
                        "one_time_keyboard":False #بسته شدن خودکار کیبورد بعد از اولین انتخاب
                    }
                    res = await app.send_inline_keypad(ChatId=msg.chat_id,txt="u can choose",inlineKeypad=keypad)
                    catch_messageId.append(res["data"]["message_id"])


                @app.message(Text("End") & ChatType("User"))
                async def test(msg:Main_Update,fsm:StateInjection):
                    if len(catch_messageId) > 0:
                        print(await app.delete_message(ChatId=msg.chat_id,MessageId=catch_messageId[len(catch_messageId)-1]))

            ```
        
        > ***نکته⚠️*** <br>
        >> `msg` :<br>
        >> همان شی حاوی اطلاعات اپدیتی است که با تابع هندلر شما مطابقت دارد<br>
        >> شما میتوانید با استفاده از آن به اطلاعات اپدیت دریافت شده از سرور<br>
        >> دسترسی داشته باشید.<br>

        """

        url = f"{self.url}/deleteMessage"

        data = {
            "chat_id": ChatId,
            "message_id":MessageId
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                return await response.json()
    
    async def set_commands(self,botCommands:list):

        """
        ### دستور تنظیم لیست دستورات بات که به کاربر نمایش داده میشود

        - #### آرگومان ها :
          - `botCommands` (**List**) : <br>لیست شامل دستورات(هر درستور به صورت یک دیکشنری با مقادیر زیر در این لیست اضافه میشود)
            - `command` (**str**) : نام دستور بدون / (مثلاً start)
            - `description` (**str**) : توضیح کوتاه درباره عملکرد دستور
        
        - #### پاسخ :
            ```python
                {'status': 'OK', 'data': {}}
            ```
        
        - #### مثال :
            ```python
                bot_cmd = [
                    {
                        "command":"Go",
                        "description":"دستور جهت آزمون"
                    }
                ]
                await app.set_commands(botCommands=bot_cmd)
            ```
        """

        url = f"{self.url}/setCommands"
        data = {
            "bot_commands":botCommands
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                return await response.json()
    
    async def remove_chat_keypad(self,ChatId:str):
        """
        ### حذف کیپد شناور از یک چت(چت خصوصی)

        - #### آرگومان :
          - `ChatId` (**str**): شناسه چت

        - #### پاسخ :
            ```python
            {'status': 'OK', 'data': {}}
            ```
        
        - #### مثال :
            ```python
                await app.remove_chat_keypad(ChatId=msg.chat_id)
            ```
        > ***نکته⚠️*** <br>
        >> `msg` :<br>
        >> همان شی حاوی اطلاعات اپدیتی است که با تابع هندلر شما مطابقت دارد<br>
        >> شما میتوانید با استفاده از آن به اطلاعات اپدیت دریافت شده از سرور<br>
        >> دسترسی داشته باشید.<br>

        """
        url = f"{self.url}/editChatKeypad"

        data = {
            "chat_id": ChatId,
            "chat_keypad_type":"Remove"
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                return await response.json()
    
    async def edit_chat_keypad(self,ChatId:str,chatKeypad:dict):

        """
        ### ویرایش کیپد شناور (چت کیپد) موجود در چت

        - #### آرگومان ها :
          - `ChatId` (**str**) : شناسه چت مورد نظر
          - `chatKeypad` (**dict**) : یک دیکشنری شامل سطر ها و ستون ها و دکمه ها
            - `rows` (**List**) : یک لیست از دیکشنری هایی که حاوی دکمه ها هستند
              - `buttons` (**List**) : یک لیست از دیکشنری های حاوی ویژگی دکمه
                - `{"id":"","type":"","button_text":"",...}` : [جهت کسب اطلاعات بیشتر در مورد پارامترها و انواع دکمه ها کلیک کنید](https://rubika.ir/botapi/models#button)
        
        - #### پاسخ :
          ```python
            {'status': 'OK', 'data': {}}
          ```
        
        - ### مثال :
          ```python
            keypad = {
                "rows" : [
                    {
                        "buttons" : [
                            {"id":"101","type":"Simple","button_text":"btn1"},
                            {"id":"102","type":"Simple","button_text":"btn2"}
                        ]
                    },
                    {
                        "buttons" : [
                            {"id":"103","type":"Simple","button_text":"btn3"},
                            {"id":"104","type":"Simple","button_text":"btn4"}
                        ]
                    }
                ]
            }
            await app.edit_chat_keypad(ChatId=msg.chat_id,chatKeypad=keypad)
          ```
        
        > ***نکته⚠️*** <br>
        >> `msg` :<br>
        >> همان شی حاوی اطلاعات اپدیتی است که با تابع هندلر شما مطابقت دارد<br>
        >> شما میتوانید با استفاده از آن به اطلاعات اپدیت دریافت شده از سرور<br>
        >> دسترسی داشته باشید.<br>

        """
        url = f"{self.url}/editChatKeypad"

        data = {
            "chat_id" : ChatId,
            "chat_keypad" : chatKeypad,
            "chat_keypad_type" : "New"
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                return await response.json()
    
    async def get_file(self,fileId:str):

        """
        ### این متد مسیر دانلود یک فایل آپلود شده را بازمیگرداند، تا بات بتواند فایل را دریافت کند

        - #### آرگومان ها :
          - `fileId` (**str**) : شناسه فایل مورد نظر
        
        - #### پاسخ :
          ```python
            {"status":"OK","data":{"download_url":"لینک دانلود"}}
          ```
        
        - #### مثال :
          ```python
            await app.get_file(fileId="رشته")
          ```

        """

        url = f"{self.url}/getFile"
        data = {
            "file_id":fileId
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                return await response.json()
    
    async def _send_file_by_id(self,ChatId:str,fileId:str,MessageId_For_Replay:str=None,txt=None,disableNotification=False,
                  chatKeypad=None,inlineKeypad=None,chatKeypadType=None,
                  metadata_part:list=None):
        
        """
        ### ارسال فایل قبلاً آپلود شده با استفاده از شناسه فایل
        
        - #### آرگومان ها :
          - `ChatId` (**str**): شناسه چت
          - `fileId` (**str**): شناسه فایل آپلود شده
          - `MessageId_For_Replay` (**str, optional**): شناسه پیام برای ریپلای
          - `txt` (**str, optional**): متن همراه فایل
          - `disableNotification` (**bool**): غیرفعال کردن اعلان (پیشفرض: False)
          - `chatKeypad` (**dict, optional**): کیپد شناور
          - `inlineKeypad` (**dict, optional**): کیپد درون خطی
          - `chatKeypadType` (**str, optional**): نوع کیپد شناور ("New" یا "Remove")
          - `metadata_part` (**list, optional**): متادیتا برای قالب‌بندی متن

        - #### پاسخ :
          ```python
            {'status': 'OK', 'data': {'message_id': 'رشته'}}
          ```
          
        - #### مثال :
        ```python
            await app._send_file_by_id(ChatId=msg.chat_id,fileId="رشته")
        ```
        > ***نکته⚠️*** <br>
        >> `msg` :<br>
        >> همان شی حاوی اطلاعات اپدیتی است که با تابع هندلر شما مطابقت دارد<br>
        >> شما میتوانید با استفاده از آن به اطلاعات اپدیت دریافت شده از سرور<br>
        >> دسترسی داشته باشید.<br>
        """

        url = f"{self.url}/sendFile"
        if chatKeypad is None and inlineKeypad is None and chatKeypadType is None :
            data = {
                "chat_id": ChatId,
                "file_id": fileId,
                "text": txt,
                "disable_notification":disableNotification
            }
        else :
            data = {
                "chat_id": ChatId,
                "file_id": fileId,
                "text": txt,
                "disable_notification":disableNotification,
                "chat_keypad":chatKeypad,
                "inline_keypad":inlineKeypad,
                "chat_keypad_type":chatKeypadType
            }
        if MessageId_For_Replay :
            data.update({"reply_to_message_id": MessageId_For_Replay})
        if metadata_part :
            MetaData = {
                "meta_data_parts":[]
            }
            MetaData.update({"meta_data_parts":metadata_part})
            data.update({"metadata":MetaData})
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                return await response.json()
    
    async def _request_send_file(self,Type):
        """
        ## درخواست URL موقت برای آپلود فایل (مرحله اول آپلود)
        > #### این متد به بات امکان می‌دهد نوع فایل مورد نظر برای آپلود را مشخص کند و در پاسخ،<br> یک آدرس برای بارگذاری فایل دریافت می‌کند تا فایل مورد نظر از طریق آن آدرس به سرور ارسال شود<br>
        > #### آدرس دریافت شده در یک فیلد با نام upload_url برمی‌گردد<br> که برای آپلود فایل از طریق درخواست POST استفاده می‌شود. فایل باید در بدنه (Body) درخواست ارسال گردد<br>

        - ### آرگومان ها :
          - `Type` (**str**) : نوع فایل (**File**, **Image**, **Voice**, **Video**, **Music**, **Gif**)
        - ### پاسخ اول :
          ```python
            {'status': 'OK', 'data': {'upload_url':'رشته'}}
          ```
        > #### پس از دریافت پاسخ باید به آدرسی که دارید یک درخواست Post بزنید و فایل را در بدنه در خواست قرار دهید.
        - ### آرگومان ها :
          - `file` (**multipart/form-data**) : فایل مورد نظر
        - ### پاسخ دوم :
          ```python
            {'status': 'OK', 'data': {'file_id':'رشته'}}
          ```
        - ### مثال :
          ```python
            await app._request_send_file(Type="Image")
          ```
        """
        url = f"{self.url}/requestSendFile"
        data = {
            "type" : Type
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                return await response.json()
    
    async def ban_chat_member(self,ChatId:str,userID):
        """
        ## بن کردن یک کاربر در گروه یا کانال
        > #### این متد برای مسدود کردن یک کاربر در گروه یا کانال استفاده می‌شود. با اجرای این متد، کاربر از چت حذف می‌شود و تا زمان رفع مسدودی، امکان ورود مجدد او از طریق لینک دعوت وجود ندارد؛ با این حال، ادمین می‌تواند کاربر را به‌صورت دستی به چت اضافه کند. این متد روی مالک و ادمین‌ها اعمال نمی‌شود
        - ### آرگومان ها:
          - `ChatId` (**str**): شناسه چت (گروه یا کانال)
          - `userID` (**str**): شناسه کاربر مورد نظر برای بن
        - ### مثال :
          await app.ban_chat_member(ChatId="رشته",userID="رشته")
        """
        url = f"{self.url}/banChatMember"

        data = {
            "chat_id":ChatId,
            "user_id":userID
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                return await response.json()
    
    async def unban_chat_member(self,ChatId:str,userID):
        """
        ## رفع مسدودیت یک کاربر در گروه یا کانال
        > #### این متد برای رفع مسدودیت یک کاربر در گروه یا کانال استفاده می‌شود. با اجرای این متد، کاربر مجاز به ورود مجدد به چت می‌شود و می‌تواند از طریق لینک دعوت یا اضافه شدن دستی توسط ادمین به چت برگردد
        - ### آرگومان ها:
          - `ChatId` (**str**): شناسه چت (گروه یا کانال)
          - `userID` (**str**): شناسه کاربر مورد نظر برای رفع مسدودیت
        - ### مثال :
          await app.unban_chat_member(ChatId="رشته",userID="رشته")
        """
        url = f"{self.url}/unbanChatMember"

        data = {
            "chat_id": ChatId,
            "user_id":userID
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                return await response.json()
    
    def read_file_sync(self,Path):
        try:
            with open(Path, "rb") as f:
                return f.read()
        except Exception as e :
            raise ValueError(f"Error to read file : {e}")

    async def send_file(self, file_path: str, file_type: str, Chat_Id: str,
                    file_name:str = None,
                    text=None, MessageId_For_Replay: str = None,
                    disable_notification=False,
                    chat_keypad=None, inline_keypad=None, chat_keypad_type=None,
                    metadata_part: list = None):
        """
        ## آپلود و ارسال فایل به چت (مدیریت کامل فرآیند آپلود)
        #### این متد با بهره گیری از دو متد دیگر به نام های<br>(_request_send_file,_send_file_by_id)<br>عمل اپلود فایل روی سرور های روبیکا ,
        #### بدست آوردن شناسه فایل و ارسال آن به چت مورد نظر را مدیریت میکند
        >#### توجه :<br>
        >#### سرور های API روبیکا برای ارسال و دریافت فایل بسیار ضعیف کار میکنند
        >#### و احتمال دریافت خطای 502 یا هر خطای مربوط به سرور های روبیکا را دارید
        >#### لزا خواهش میکنم جهت استفاده ازین متدها که با فایل کار میکنند حتمن یک عملیات شروع مجدد در صورت شکست را تعبیه کنید
        >#### تا در صورت شکست درخواست دوباره متد فراخوانی شود

        - ### آرگومان ها :
          - `file_path` (**str**): مسیر فایل در سیستم
          - `file_type` (**str**): نوع فایل (**File**, **Image**, **Voice**, **Video**, **Music**, **Gif**)
          - `Chat_Id` (**str**): شناسه چت
          - `file_name` (**str**) : نام قابل نمایش فایل
          - `text` (**str, optional**): متن همراه فایل
          - `MessageId_For_Replay` (**str, optional**): شناسه پیام برای ریپلای
          - `disable_notification` (**bool, optional**): غیرفعال کردن اعلان (پیشفرض: False)
          - `chat_keypad_type` (**str, optional**): نوع کیپد شناور ("New" یا "Remove")
          - `chat_keypad` (**dict, optional**): کیپد شناور
          - `inline_keypad` (**dict, optional**): کیپد درون خطی
          - `metadata_part` (**list, optional**): متادیتا برای قالب‌بندی متن
        >> #### در مورد سه آرگومان آخر اگر احتیاج به راهنمایی دارید لطفا به توضیحات در متد های زیر مراجعه کنید
        >> #### (`send_keypad` , `send_inline_keypad`)
        - ### پاسخ :
        ```python 
          {'status': 'OK', 'data': {'message_id': 'رشته'}}
        ```

        - ### مثال :
        ```python
          await app.send_file(file_path="test.jpg",Chat_Id=msg.chat_id,file_type="Image")
        ```
        > ***نکته⚠️*** <br>
        >> `msg` :<br>
        >> همان شی حاوی اطلاعات اپدیتی است که با تابع هندلر شما مطابقت دارد<br>
        >> شما میتوانید با استفاده از آن به اطلاعات اپدیت دریافت شده از سرور<br>
        >> دسترسی داشته باشید.<br>

        """


        # """ file types ==> File , Image , Voice , Video , Music , Gif """
        try:
            response_url = await self._request_send_file(Type=file_type)
            if not response_url or response_url.get("status") != "OK":
                bot_logger.error(f"Failed to obtain upload URL for file_type={file_type}, chat_id={Chat_Id}: API response invalid")
                return None

            upload_url = response_url["data"]["upload_url"]
            async with aiohttp.ClientSession() as session:
                file_bytes = await asyncio.to_thread(self.read_file_sync, file_path)
                data_form = aiohttp.FormData()
                data_form.add_field('file', file_bytes,
                                    filename=file_name)
                try:
                    async with session.post(upload_url, data=data_form ) as response:
                        res = await response.json()
                        if res.get("status") == "OK":
                            file_id = res["data"]["file_id"]    
                            send_result = await self._send_file_by_id(
                                fileId=file_id,
                                ChatId=Chat_Id,
                                chatKeypad=chat_keypad,
                                disableNotification=disable_notification,
                                inlineKeypad=inline_keypad,
                                metadata_part=metadata_part,
                                txt=text,
                                MessageId_For_Replay=MessageId_For_Replay,
                                chatKeypadType=chat_keypad_type
                            )
                            if send_result and send_result.get("status") == "OK":
                                bot_logger.info(f"File sent successfully: type={file_type}, chat_id={Chat_Id}, file_path={file_path}")
                                return send_result
                            else:
                                bot_logger.error(f"Failed to send file by ID: file_id={file_id}, chat_id={Chat_Id}, reason={send_result}")
                                return None
                        else:
                            bot_logger.error(f"Upload to temporary URL failed: status={res.get('status')}, chat_id={Chat_Id}, file_type={file_type}")
                            return None
                except aiohttp.ClientResponseError as e:
                    bot_logger.error(f"HTTP error during file upload to {upload_url}: status={e.status}, message={e.message}, chat_id={Chat_Id}")
                    return None
                except Exception as e:
                    bot_logger.error(f"Unexpected exception while uploading file to Rubika servers: {e}, chat_id={Chat_Id}, file_path={file_path}")
                    return None
        except FileNotFoundError:
            bot_logger.error(f"File not found: {file_path}, chat_id={Chat_Id}")
            return None
        except Exception as e:
            bot_logger.error(f"Failed to initiate file upload (_request_send_file): {e}, chat_id={Chat_Id}, file_type={file_type}")
            return None