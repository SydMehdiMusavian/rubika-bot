import json , asyncio
from Rubika.Config_Logger import bot_logger
from Rubika.FileLock import GlobalFileLock
class StateInjection :
    """
    ## رابط مدیریت وضعیت و داده‌های کاربر برای ماشین حالت.

    #### این کلاس برای هر جفت (چت، کاربر) نمونه‌سازی می‌شود و امکان خواندن، نوشتن
    #### و پاک کردن وضعیت و داده‌های جانبی را در حافظه (همراه با ذخیره دوره‌ای در فایل) فراهم می‌کند.

    > #### ⚠️ نکته :
    > #### شما میتوانید به نمونه ساخته شده ازین مدل با شناسه کاربر و شناسه چت داده شده در تابع
    > #### هندلر خود تحت عنوان `fsm` یا `Fsm` یا `State` دسترسی داشته باشد.
    > #### *به مثال گفته شده دقت کنید*

    - ### ویژگی ها:
      - `chat_id` (str): شناسه چت (الزاماً استفاده نمی‌شود)
      - `user_id` (str): شناسه کاربر – کلید اصلی ذخیره‌سازی

    - ### توابع :
      - `get_state()` -> state:          وضعیت فعلی کاربر را برمی‌گرداند
      - `set_state(**State, data=None**)` :   وضعیت کاربر را تغییر می‌دهد و داده‌های جانبی را ذخیره می‌کند
      - `get_state_Data()` -> dict :      داده‌های جانبی کاربر را برمی‌گرداند
      - `clear_state()` :                 وضعیت و داده‌های کاربر را پاک می‌کند

    - ### مثال :
    ```python
    from Rubika import Bot , MultiRunner , Text , ChatType , Reg ,
    Document_Object , Documents , F , StateFilter , state , state_group , StateInjection , Main_Update
    import os , re , asyncio

    app = Bot(Token=token)

    class MyStates(state_group):
        start = state()
        confirm = state()
        end = state()
    # print(MyStates.start.next_name) خروجی : confirm
    # print(MyStates.end.previous_name) خروجی : confirm

    @app.message(Text("Start") & ChatType("User"))  
    async def doc_handler(msg: Main_Update, fsm: StateInjection):
        fsm.set_state(State=MyStates.start)
        print("now user go to start state !!!")

    @app.message(StateFilter(State=MyStates.start) & ChatType("User"))  
    async def newhandler(msg: Main_Update, fsm: StateInjection):
        print("user in start state")
        MyStates.start.next(fsm)
        print("now user go to next state (confirm)!!!")

    @app.message(StateFilter(State=MyStates.confirm) & ChatType("User"))  
    async def newhandler2(msg: Main_Update, fsm: StateInjection):
        print("user in confirm state")
        MyStates.confirm.next(fsm)
        print("now user go to next state (end)!!!")

    @app.message(StateFilter(State=MyStates.end) & ChatType("User"))  
    async def newhandler3(msg: Main_Update, fsm: StateInjection):
        print("user in end state")
        MyStates.end.next(fsm)
        print("now user go to next state (...)!!!")
        fsm.clear_state()
        print("and now clear state and data of user")

    app(bot_name="TestBot").Run()
    ```

    """
    def __init__(self,chatID,userID):
        self.chat_id = chatID
        self.user_id = userID

    user_state = {}
    @staticmethod
    async def catch_up_from_json(filename):

        async with GlobalFileLock.get_lock():
            try:
                def _sync_read():
                    with open(filename, "r", encoding="utf-8") as f:
                        return json.load(f)
                _data = await asyncio.to_thread(_sync_read)
                for i in _data.keys():
                    fake_dict = _data[i]["state"]
                    _data[i]["state"] = state()
                    _data[i]["state"].name = fake_dict["name"]
                    _data[i]["state"].next_name = fake_dict["next"]
                    _data[i]["state"].previous_name = fake_dict["previus"]
                return _data
            except FileNotFoundError:
                return {}
            except Exception as e:
                bot_logger.error(f"error to read file == : {e}")
                return {}
        
    @staticmethod
    def is_json_serializable(obj):
        if isinstance(obj, (str, int, float, bool, type(None))):
            return True
        if isinstance(obj, dict):
            return all(StateInjection.is_json_serializable(k) and StateInjection.is_json_serializable(v) for k, v in obj.items())
        if isinstance(obj, (list, tuple, set)):
            if isinstance(obj, tuple) or isinstance(obj, set):
                return False
            return all(StateInjection.is_json_serializable(item) for item in obj)
        return False


    async def get_state(self):
        if StateInjection.user_state == {}:
            StateInjection.user_state = await StateInjection.catch_up_from_json(filename="user_state_data.json")
        property_user = StateInjection.user_state.get(self.user_id, None)
        return (property_user.get("state", None) if property_user is not None else state())
    
    async def get_state_Data(self):
        if StateInjection.user_state == {}:
            StateInjection.user_state = await StateInjection.catch_up_from_json(filename="user_state_data.json")
        property_user = StateInjection.user_state.get(self.user_id, None)
        return (property_user.get("user_data", None) if property_user is not None else None)

    def set_state(self,State:'state',data:dict=None):
        if not isinstance(State, state):
            raise TypeError("State must be an instance of state class")

        if self.user_id not in StateInjection.user_state:
            StateInjection.user_state[self.user_id] = {}
        StateInjection.user_state[self.user_id]["state"] = State
        if data:
            if not StateInjection.is_json_serializable(obj=data):
                raise ValueError("داده شامل نوع‌های غیرمجاز مثل tuple, set, datetime و ... است")
            if "user_data" not in StateInjection.user_state[self.user_id]:
                StateInjection.user_state[self.user_id]["user_data"] = {}
            StateInjection.user_state[self.user_id]["user_data"].update(data)

    def clear_state(self):
        StateInjection.user_state[self.user_id].update({"state" : state() , "user_data" : {}})



class state:
    """
    ## مدل یک وضعیت (**State**) در ماشین حالت محدود.

    #### هر وضعیت دارای نام و اشاره‌گرهایی به وضعیت بعدی و قبلی است.
    #### معمولاً نمونه‌های این کلاس درون `state_group` تعریف می‌شوند تا زنجیره وضعیت‌ها به صورت خودکار تنظیم شود.

    - ### ویژگی ها:
      - `name` (**str | None**): نام وضعیت
      - `next_name` (**str | None**): نام وضعیت بعدی
      - `previous_name` (**str | None**): نام وضعیت قبلی

    - ### توابع :
      - `next`(**StateContext**): انتقال به وضعیت بعدی (در صورت وجود)
      - `previous`(**StateContext**): بازگشت به وضعیت قبلی (در صورت وجود)
      - `single_state`(**statename**): ساخت یک وضعیت بدون زنجیره

    - ### مثال :
    ```python
    @app.message(Text("ایجاد حالت شروع") & ChatType("User"))  
    async def doc_handler(msg: Main_Update, fsm: StateInjection):
        start_state = state.single_state(statename="start")
        print(start_state.name) # خروجی : start
    ```
    """
    def __init__(self):
        self.name = None
        self.next_name = None
        self.previous_name = None
        self.dict_state = {}

    def __repr__(self):
        return f"state name -> {self.name} next -> {self.next_name} previous -> {self.previous_name}"
    
    def __eq__(self, other):
        if not isinstance(other, state):
            return False
        return self.name == other.name 
    
    def __and__(self,other):
        raise ValueError("pleas use from Filter state....")
    

    @classmethod
    def single_state(cls,statename:str):
        full_object = cls()
        full_object.name = statename
        return full_object
    
    def next(self,FSM:StateInjection):
        if self.next_name :
            NewState = self.dict_state.get(self.next_name,None)
            if NewState :
                FSM.set_state(State=NewState)
        else:
            bot_logger.warning("no next state")

    def previous(self,FSM:StateInjection):
        if self.previous_name :
            NewState = self.dict_state.get(self.previous_name,None)
            if NewState :
                FSM.set_state(State=NewState)
        else:
            bot_logger.warning("no previous state")
    
    
    
class metastate(type):
    def __new__(cls,name,bases,dct:dict):
        d = {key:value for key , value in dct.items() if isinstance(value,state)}
        state_names = list(d.keys())
        for i, name in enumerate(state_names):
            state_obj = d[name]
            state_obj.name = name
            if i > 0:
                state_obj.previous_name = state_names[i-1]
            if i < len(state_names) - 1:
                state_obj.next_name = state_names[i+1]
            state_obj.dict_state = d
        return super().__new__(cls,name,bases,dct)
    
class state_group(metaclass=metastate):
    """
    ## کلاس پایه برای گروه‌بندی وضعیت‌ها با ترتیب خودکار.

    ### با تعریف attribute‌های از نوع `state` در زیرکلاس، به ترتیب معرفی آن‌ها،<br>
    ### فیلدهای `next_name` و `previous_name` به صورت خودکار مقداردهی می‌شوند.

    - ### مثال :
    ```python
    from Rubika import Bot , MultiRunner , Text , ChatType , Reg ,
    Document_Object , Documents , F , StateFilter , state , state_group , StateInjection , Main_Update
    import os , re , asyncio

    app = Bot(Token=token)

    class MyStates(state_group):
        start = state()
        confirm = state()
        end = state()
    # print(MyStates.start.next_name) خروجی : confirm
    # print(MyStates.end.previous_name) خروجی : confirm

    @app.message(Text("Start") & ChatType("User"))  
    async def doc_handler(msg: Main_Update, fsm: StateInjection):
        fsm.set_state(State=MyStates.start)
        print("now user go to start state !!!")

    @app.message(StateFilter(State=MyStates.start) & ChatType("User"))  
    async def newhandler(msg: Main_Update, fsm: StateInjection):
        print("user in start state")
        MyStates.start.next(fsm)
        print("now user go to next state (confirm)!!!")

    @app.message(StateFilter(State=MyStates.confirm) & ChatType("User"))  
    async def newhandler2(msg: Main_Update, fsm: StateInjection):
        print("user in confirm state")
        MyStates.confirm.next(fsm)
        print("now user go to next state (end)!!!")

    @app.message(StateFilter(State=MyStates.end) & ChatType("User"))  
    async def newhandler3(msg: Main_Update, fsm: StateInjection):
        print("user in end state")
        MyStates.end.next(fsm)
        print("now user go to next state (...)!!!")
        fsm.clear_state()
        print("and now clear state and data of user")

    app(bot_name="TestBot").Run()
    ```
    """
    pass

