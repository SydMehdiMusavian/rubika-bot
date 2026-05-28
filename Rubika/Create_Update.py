from dataclasses import dataclass
from Rubika.FinitState import state , StateInjection
from Rubika.Config_Logger import bot_logger


@dataclass
class Message:
    message_id: str | None = None
    reply_to_message_id: str | None = None
    text: str | None = None
    sender_id: str | None = None
    sender_type: str | None = None
    timestamp: str | None = None
    aux_data: dict | None = None
    sticker: dict | None = None
    stickerId: str | None = None
    sticker_emoji_character: str | None = None
    file: dict | None = None
    fileName: str | None = None
    fileId: str | None = None
    file_extension: str | None = None
    location: dict | None = None
    poll: dict | None = None
    contact_message: dict | None = None
    forwarded_from: dict | None = None

@dataclass
class RemoveMessage:
    removed_message_id:str = None

@dataclass
class Main_Update:
    """
    ## شیء اصلی آپدیت ارسالی به هندلرها

    #### این کلاس تمام اطلاعات مربوط به یک آپدیت (رویداد) دریافتی از سرورهای روبیکا را در بر می‌گیرد.  
    #### شیء ساخته شده از این کلاس به عنوان آرگومان اول به هر هندلر (تابع ثبت شده با دکوراتور `@bot_Object.message`) پاس داده می‌شود.

    - ### ویژگی ها :
        `chat_id` (**str | None**): شناسه چتی که رویداد در آن رخ داده است
        `chat_type` (**str | None**): نوع چت (`User`, `Bot`, `Group`, `Channel`) پس از فراخوانی `get_chat` پر می‌شود
        `type_update` (**str | None**): نوع آپدیت (`NewMessage`, `UpdatedMessage`, `RemovedMessage`, ...)
        `message` (**Message | RemoveMessage**): نوع آن بسته به شی مربوط به پیام متفاوت است و حاوی اطلاعات پیام میباشد.
        `UserState` (**state | None**): وضعیت فعلی کاربر در ماشین حالت (FSM) از `StateInjection.get_state()` گرفته می‌شود.
        `FsmContext` (**StateInjection | None**): شیء کمکی برای مدیریت وضعیت و داده‌های کاربر

    **نحوه استفاده در هندلرها:**
    ```python
    from Rubika import Main_Update
    from Rubika import StateInjection

    @app.message(Text("سلام"))
    async def hello(msg: Main_Update, fsm: StateInjection):
        # msg.chat_id => شناسه چت
        # msg.message.text => متن پیام
        # fsm همان msg.FsmContext است (به راحتی در دسترس)
        print(msg.message.sender_id)
    ```
    > ### _توجه_ :

    >> #### فیلد chat_type پس از اولین بار استفاده از get_chat ذخیره شده و بعداً در کش استفاده می‌شود.
    >> #### UserState و FsmContext به صورت خودکار از روی شناسه کاربر و چت ساخته می‌شوند.

    """
    chat_id: str | None = None
    chat_type: str | None = None
    type_update: str | None = None
    message: Message | RemoveMessage = None
    UserState: state | None = None
    FsmContext: StateInjection | None = None

    @classmethod
    async def get_raw_data(cls, update: dict):
        
        if not isinstance(update, dict):
            bot_logger.error(f"update is not a dict: {type(update)}")
            return None
        
        if update.get("type") == "RemovedMessage":
            msg = RemoveMessage(
                removed_message_id = update.get("removed_message_id",None),
            )
            return cls(
                        message=msg,
                        chat_id=update.get("chat_id",None),
                        type_update=update.get("type",None)
                    )
        else :
            message_obj = update.get("new_message",None) or update.get("updated_message",None)
            if not message_obj:
                bot_logger.error("message object is none")
                return None
            msg = Message(
                message_id=message_obj.get("message_id"),
                reply_to_message_id = message_obj.get("reply_to_message_id"),
                text=message_obj.get("text"),
                sender_id=message_obj.get("sender_id"),
                sender_type=message_obj.get("sender_type"),
                timestamp=message_obj.get("time"),
                aux_data=message_obj.get("aux_data"),
                contact_message=message_obj.get("contact_message"),
                forwarded_from=message_obj.get("forwarded_from"),
                location=message_obj.get("location"),
                poll=message_obj.get("poll")
            )
            if message_obj.get("file",None):
                fileObject = message_obj.get("file",None)
                msg.file = fileObject
                msg.fileId = fileObject.get("file_id",None)
                f_name = fileObject.get("file_name",None)
                msg.fileName = f_name
                ls_ex = f_name.split(r".")
                if len(ls_ex)>0:
                    msg.file_extension = ls_ex[len(ls_ex)-1]
            elif message_obj.get("sticker",None):
                stickerObject = message_obj.get("sticker")
                msg.sticker = stickerObject
                msg.stickerId = stickerObject.get("sticker_id",None)
                msg.sticker_emoji_character = stickerObject.get("emoji_character",None)
                fileObject = stickerObject.get("file")
                msg.file = fileObject
                msg.fileId = fileObject.get("file_id",None)
                f_name = fileObject.get("file_name",None)
                msg.fileName = f_name
                ls_ex = f_name.split(r".")
                if len(ls_ex)>0:
                    msg.file_extension = ls_ex[len(ls_ex)-1]

            Finit_help_state_object = StateInjection(chatID=update.get("chat_id",None),userID=msg.sender_id)
            user_state = await Finit_help_state_object.get_state()
            return cls(
                        message=msg,
                        chat_id=update.get("chat_id",None),
                        type_update=update.get("type",None),
                        FsmContext = Finit_help_state_object,
                        UserState= user_state
                    )