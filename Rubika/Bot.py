import aiohttp ,asyncio 
import Rubika.Filter as Filter
from Rubika.Create_Update import Main_Update
from Rubika.Router import router
from Rubika.Mining import Fetch_Data
from Rubika.FinitState import state
from Rubika.Functions import Fn
from Rubika.Config_Logger import bot_logger , bot_token_var

class dispatcher:
    """تابع توزیع کننده داده خام"""
    def __init__(self,tokenbot:str,routers:list,btName:str=None):
        self.url = f"https://botapi.rubika.ir/v3/{tokenbot}/"
        self.Router_Handlers = routers.copy()
        self.chat_cache = {}
        self.token = tokenbot
        self.btName = btName

    async def get_update(self, offset=None):
        payload = {}
        if offset:
            payload["offset_id"] = str(offset)
        if not self.session:
             raise ValueError("ClientSession not initialized. Please call start_polling first.")
        while True:
            try:
                async with self.session.post(f"{self.url}getUpdates", json=payload) as resp:
                    data = await resp.json()
                    return data
            except Exception as e:
                bot_logger.error(f"Failed to fetch updates from API (offset={offset}): {e}")
                await asyncio.sleep(0.5)
    
    async def get_chat_update(self,update:Main_Update):
        ChatId = update.chat_id
        if self.chat_cache.get(ChatId,None):
            update.chat_type = self.chat_cache.get(ChatId,None)
            return update
        payload = {
            "chat_id" : ChatId
        }
        try:
            async with self.session.post(f"{self.url}getChat", json=payload) as resp:
                res_js = await resp.json()
                if res_js.get("status",None) == "OK":
                    data = res_js.get("data",None)
                    if data:
                        update.chat_type = data["chat"].get("chat_type",None)
                        self.chat_cache.update({ChatId:data["chat"].get("chat_type",None)})
                else:
                    bot_logger.warning(f"getChat API returned non-OK status for chat_id={update.chat_id}: {res_js.get('status')}")
                return update
        except Exception as e :
            bot_logger.error(f"Failed to retrieve chat information for chat_id={update.chat_id}: {e}")

    async def safe_handler(self,handler, update):
        try:
            return await handler(update)
        except Exception as e:
            bot_logger.error(f"Exception in handler '{handler.__name__}' while processing update from user {update.message.sender_id if update.message else 'unknown'}: {e}")
            return None
        
    async def proccessor(self, updts):
        for update in updts:
            for handler in self.Router_Handlers:
                if await handler(update):
                    break
        

    async def Multi_proccess(self,user_locker):
        if user_locker == {} or self.Router_Handlers == []:
            return
        tasks = [self.proccessor(updates) for updates in user_locker.values()]
        await asyncio.gather(*tasks)

    async def start_polling(self):
        async with aiohttp.ClientSession() as session:
            self.session = session
            mainOffset = None
            while True:
                short_token = self.btName if self.btName else self.token[:8] if self.token else "None_Token"
                token_ctx = bot_token_var.set(short_token)
                try:
                    update = await self.get_update(offset=mainOffset)

                    if update and update.get("status") == "OK":

                        updates = update["data"]["updates"]

                        if updates:
                            mainOffset = update["data"]["next_offset_id"]
                            UserLocker = {}
                            for updt in updates:
                                update_obj = await Main_Update.get_raw_data(update=updt)
                                if update_obj is not None :
                                    if update_obj.type_update == "NewMessage" or update_obj.type_update == "UpdatedMessage":
                                        update_obj = await self.get_chat_update(update=update_obj)
                                        if update_obj.message.sender_id not in UserLocker:
                                            UserLocker[update_obj.message.sender_id] = []
                                        UserLocker[update_obj.message.sender_id].append(update_obj)
                                    elif update_obj.type_update == "RemovedMessage":
                                        update_obj = await self.get_chat_update(update=update_obj)
                                        if update_obj.type_update not in UserLocker:
                                            UserLocker[update_obj.type_update] = []
                                        UserLocker[update_obj.type_update].append(update_obj)

                            bot_logger.info(UserLocker)
                            await self.Multi_proccess(UserLocker)

                    else:
                        bot_logger.error("Polling request failed: API response status is not 'OK' or empty")
                        break

                except Exception as e:
                    bot_logger.critical(f"Unhandled exception in polling main loop: {e}")
                    break
                finally:
                    bot_token_var.reset(token_ctx)

                await asyncio.sleep(0.5)



class Bot(Fn):
    """
    ### کلاس ساخت  و تنظیم برنامه ربات ⚙️

    - #### آرگومان ها :
      - `Token` (**str**) : توکن ربات
    
    - #### پاسخ :
      - **Bot Object :** نمونه ربات که میتوانید در موارد زیر استفاده کنید
        - دسترسی به متد های مورد نیاز برای تعامل با روبیکا مثل :
          - _send_message_simple_ , _edit_message_text_ , _delete_message_ , _send_file_ , ...
        - تعریف توابعی برای کنترل بر روی ورودی آپدیت ها به ربات با کمک دکوراتور پیام
        ```python
        @Bot_Object.message(Text("/Start","/start") & ChatType("User"))
        async def SimpleHandler(msg:Main_Update,fsm:StateInjection):
            pass
        ```
      - **تعیین نام برای ربات**
        > ##### این کار به شما در مدیریت لاگ ها و یافتن خطا مربوط به ربات کمک میکند
            ```python
                Bot_Object(bot_name="Bot_1").Run()
            ```
    > #### ⚠️ نکته :
    >> این مورد در استفاده از `MultiRunner.Run(Bot_Object_1(bot_name="robot 1") , Bot_Object_2(bot_name="robot 2") , ...)` <br>
    >> بسیار مهم است چون باید بتوان تشخیص داد هر لاگ که ثبت میشود برای کدام ربات است

    > #### `msg` :
    >> یک نمونه از کلاس اپدیت هست که شامل شناسه چت , نوع چت , پیام رسیده که خودش شامل اطلاعات پیام هست و حالت کاربر میباشد<br>
    >> نوعش رو همیشه `Main_Update` بذارید تا پیش نمایش ویژگی ها رو ببینید.

    > #### `fsm` :
    >> یک نمونه تزریق شده از کلاس `StateInjection` هست که خودش شناسه کاربر و چت را به متد ها داده
    >> و شما تنها لازم است برای تعیین حالت کاربر یا ذخیره اطلاعات در حالت خاصی از کاربر یا دریافت اطلاعات حالت کاربر
    >> از متد های آن بدون تعیین پارامتر استفاده کنید
    >> البته این نمونه زمانی بدرد شما میخورد که شما میخواهید حالت کاربر را دستی مدیریت کنید

    """
    def __init__(self,Token=None):
        self.token = Token
        self.BotName:str = None
        self.ListOfRouterObject = []
        self.router_object = router()
        super().__init__(tk=Token)

    def Register_handler(self,Router_Object:router):
        """ثبت هندلر هایی که از کلاس روتر ساخته شدن"""
        self.ListOfRouterObject.append(Router_Object)

    def __call__(self, bot_name:str):
        self.BotName = bot_name
        return self
    
    async def Main(self):
        self.Register_handler(Router_Object=self.router_object)
        if self.token is None :
            raise TypeError("Bot token is missing. Please provide a valid token.")
        dp = dispatcher(tokenbot=self.token,btName=self.BotName,routers=self.ListOfRouterObject)
        bot_logger.info("===== Rubika bot started successfully in polling mode =====")
        await asyncio.gather(dp.start_polling(),Fetch_Data.monitor_and_save(f_name="user_state_data.json",interval=1))

    def Run(self):
        """
        ## تابع اجرا کننده تک ربات
        """
        asyncio.run(self.Main())

    def message(self,*arguments):
        def wrapper(fn):
            for arg in arguments:
                if isinstance(arg,str):
                    self.router_object.message_handler.append((Filter.Text(arg),fn))
                elif isinstance(arg,state):
                    self.router_object.message_handler.append((Filter.StateFilter(arg),fn))
                else:
                    self.router_object.message_handler.append((arg,fn))
            return fn
        return wrapper


class MultiRunner :
    """
    ## کلاس مدیریت اجرای چندین ربات
    > ### این کلاس برای کنترل جریان داده در چندین برنامه ربات تعریف شده
    > ### شما میتوانید با استفاده از متد `run` این کلاس و ارسال چندین نمونه ربات به آن به صورت همگام چندین ربات فعال داشته باشید.
    ## نحوه استفاده :
    ```python
    from Rubika import Bot , MultiRunner , Text , ChatType , Reg , Document_Object , Documents , F , StateFilter , state , state_group , StateInjection , Main_Update
    import os , re , asyncio

    token = os.getenv("bot_token1")
    token2 = os.getenv("bot_token2")

    app = Bot(Token=token)
    app2 = Bot(Token=token2)

    @app.message(Text("/Start","/start") & ChatType("User"))
    async def SimpleHandler(msg:Main_Update,fsm:StateInjection):
        pass
        
    @app2.message(Text("شروع","آغاز") & ChatType("User"))
    async def SimpleHandler(msg:Main_Update,fsm:StateInjection):
        pass

    MultiRunner.Run(app(bot_name="robot 1"),app2(bot_name="robot 2"))
    ```
    """
    @staticmethod
    async def main(args:tuple):
        tuple_apps = args
        tasks = []
        for i in tuple_apps:
            tasks.append(i.Main())
        await asyncio.gather(*tasks)

    @classmethod
    def Run(cls,*args:Bot):
        """
        ## تابع اجرا کننده چندین ربات <hr>

        - ### آرگومان :
          - `*args` (**Bot**): نمونه های ساخته شده از مدل ربات

        """
        asyncio.run(cls.main(args))
    
    


